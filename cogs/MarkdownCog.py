import json

from discord.ext.commands import Cog, command, group, Context
import md_parse
from models import QuizData
from type_hints import JSON


class MarkdownCog(Cog):
    def __init__(self, bot):
        self.bot = bot


    @group(
        name='mdquiz',
        help='quiz! mdquiz (subcommand) (args)',
        alias=['마크다운퀴즈', '마크다운', 'mq']
    )
    async def mdquiz(self, ctx: Context):
        pass

    @mdquiz.command(
        name='parse',
        help='quiz! mdquiz parse (name) ```(text)```',
        alias=['파싱', 'p']
    )
    async def parse(self, ctx: Context, name: str, *, text: str):
        text = text.strip('```')
        quiz_json: JSON = md_parse.parse_md_quiz(name, text)
        quiz = QuizData.from_json(quiz_json)
        await ctx.author.send(text=json.dumps(quiz_json, ensure_ascii=False, indent=2))
        self.bot.load_quiz(quiz)
        await ctx.send('Parsed text without any errors. Loaded it in bot :D')


def setup(bot):
    """Function called when extension is loaded."""
    bot.logger.debug(
        'Registering extension "Markdown"'
    )
    bot.add_cog(MarkdownCog(bot))


def teardown(bot):
    """Function called when extension is unloaded."""
    bot.logger.debug(
        'Removing extension "Markdown"'
    )
    bot.remove_cog(bot.get_cog('Markdown'))