import json
from typing import Optional, Dict, List, Union

from discord import Embed, TextChannel, Message, Role, User, Guild, Member, Emoji, PartialEmoji, Reaction
from discord.ext.commands import Cog, command, group, Context
from discord.errors import NotFound, Forbidden

from constants import NUMBER_EMOJIS
from models import QuizData
from type_hints import JSON


class QuizCog(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.track_quizs: Dict[str, Dict[str, Union[int, List[int]]]] = {}
        self.load_tracking_data()

    @command(
        name='help',
        help='',
        alias=['도움말', '도움']
    )
    async def help(self, ctx: Context):
        help_embed = Embed(title='QuizBot > help', description='퀴즈봇의 도움말 명령어입니다.')
        await ctx.send(embed=help_embed)

    @command(
        name='list',
        help='quiz! list',
        alias=['목록', 'l']
    )
    async def quiz_list(self, ctx: Context):
        quiz_embed = Embed(title='QuizBot > Current quizs', description='현재 불러온 퀴즈 목록입니다.')
        for q_info in map(lambda q: (q._meta['date'], q._meta['name'], q._meta['version']), self.bot.quizs):
            quiz_embed.add_field(name=q_info[1], value=f'날짜 : {q_info[0]}, 버전 : {q_info[2]}', inline=False)

        return await ctx.send(embed=quiz_embed)
    
    @command(
        name='show',
        help='quiz! show quiz01 #channel',
        alias=['보기', '출제', 'display']
    )
    async def show(self, ctx: Context, quiz_name: str, quiz_channel: TextChannel):
        quiz_data: Optional[QuizData] = next(filter(lambda q: q._meta['name'] == quiz_name, self.bot.quizs), None)
        if quiz_data is not None:
            self.track_quizs[quiz_name] = {
                'quild': quiz_channel.guild.id,
                'channel': quiz_channel.id,
                'msgs': []
            }
            for index, quiz in enumerate(quiz_data.questions):
                quiz_msg: Message = await quiz_channel.send(quiz.text(index+1))
                for i in range(1, len(quiz.options)+1):
                    await quiz_msg.add_reaction(NUMBER_EMOJIS[i])
                self.track_quizs[quiz_name]['msgs'].append(quiz_msg.id)
            await ctx.send('퀴즈를 생성했습니다 :D')
        else:
            await ctx.send(f'"{quiz_name}" 퀴즈를 찾을 수 없습니다 :(')

    @command(
        name='answer',
        help='quiz! answer quiz01 #channel',
        alias=['정답', '해설', 'explanation']
    )
    async def answer(self, ctx: Context, quiz_name: str, answer_channel: TextChannel):
        quiz_data: Optional[QuizData] = next(filter(lambda q: q._meta['name'] == quiz_name, self.bot.quizs), None)
        if quiz_data is not None:
            data: Dict[str, Union[int, List[int]]] = self.track_quizs[quiz_name]
            for index, quiz in enumerate(quiz_data.questions):
                await answer_channel.send(embed=quiz.answer_embed(
                    index+1,
                    ctx.guild.id,
                    data['channel'],
                    data['msgs'][index]
                ))
            await ctx.send('해설을 생성했습니다 :D')
        else:
            await ctx.send(f'"{quiz_name}" 퀴즈를 찾을 수 없습니다 :(')

    @command(
        name='check',
        help='quiz! check quiz01 #channel (@username|@role)',
        alias=['정답', '해설', 'explanation']
    )
    async def check(self, ctx: Context, quiz_name: str, quiz_channel: TextChannel, target: Optional[Union[Role, User]]=None):
        # TODO: Implement answer display command.
        quiz_data: Optional[QuizData] = next(filter(lambda q: q._meta['name'] == quiz_name, self.bot.quizs), None)
        if quiz_data is not None:
            msg_ids: List[int] = self.track_quizs[quiz_name]
            reactions: List[List[Reaction]] = []
            for msg_id in msg_ids:
                msg: Optional[Message] = await quiz_channel.fetch_message(msg_id)
                if msg is None:
                    return await ctx.send('Invalid quiz message tracking data found. Stop checking :(')
                reactions.append(msg.reactions)

            if target is None:
                # All users who reacted in quiz:
                for user in quiz_channel.guild.member:
                    await self.__check_user(ctx, reactions, quiz_data, user)
            elif isinstance(target, Role):
                # Users who have target role and reacted in quiz:
                for user in target.members:
                    await self.__check_user(ctx, reactions, quiz_data, user)
            elif isinstance(target, User):
                # Specific user if the user reacted in quiz:
                await self.__check_user(ctx, reactions, quiz_data, target)
        else:
            await ctx.send(f'"{quiz_name}" 퀴즈를 찾을 수 없습니다 :(')

    async def __check_user(self, ctx: Context, reactions: List[List[Reaction]], quiz: QuizData, user: User) -> JSON:
        for index, q in enumerate(quiz.questions):
            if q.has_multi_answers:
                pass
            else:
                emoji = NUMBER_EMOJIS(q.answer)
                assert reactions[index][q.answer-1].emoji == emoji
                try:
                    await reactions[index][q.answer-1].remove(user)
                except NotFound as e:
                    pass

    @command(
        name='reload-quizs',
        help='quiz! reload-quizs',
        alias=['퀴즈리로드', 'quizreload', 'qr']
    )
    async def reload_quizs(self, ctx: Context):
        await ctx.send('QuizBot이 문제 데이터를 다시 불러옵니다...')
        await self.bot.load_quizs('./quizs')
        await ctx.send('QuizBot이 문제 데이터를 모두 불러왔습니다!')

    @command('track-data')
    async def show_tracking_data(self, ctx: Context):
        await ctx.author.send(
            json.dumps(self.track_quizs, ensure_ascii=False, indent=2)
        )

    def load_tracking_data(self):
        with open('quiz_tracking_data.json', mode='rt', encoding='utf-8') as f:
            self.track_quizs = json.load(f)

    def save_tracking_data(self):
        with open('quiz_tracking_data.json', mode='wt', encoding='utf-8') as f:
            json.dump(self.track_quizs, f, ensure_ascii=False, indent=4)

    def __delete__(self, instance):
        instance.save_tracking_data()


def setup(bot):
    """Function called when extension is loaded."""
    bot.logger.debug(
        'Registering extension "Quiz"'
    )
    bot.add_cog(QuizCog(bot))


def teardown(bot):
    """Function called when extension is unloaded."""
    bot.logger.debug(
        'Removing extension "Quiz"'
    )
    bot.get_cog('Quiz').save_traking_data()
    bot.remove_cog(bot.get_cog('Quiz'))
