import json
from typing import List

import discord
from discord.ext import commands
import aiofiles
import os

from models import QuizData
from type_hints import JSON
from utils import get_stream_logger, DEBUG


class QuizBot(commands.Bot):
    def __init__(self):
        super(QuizBot, self).__init__(command_prefix='quiz! ', help_command=None, description='퀴즈 출제용 디스코드 챗봇')
        self.quizs: List[QuizData] = []
        self.logger = get_stream_logger('QuizBot', DEBUG)
        self.load_extension('cogs.QuizCog')
        self.load_extension('cogs.MarkdownCog')

    async def on_ready(self):
        await self.load_quizs(path='./quizs')
        self.logger.info('QuizBot is now ready!')

    async def load_quizs(self, path: str):
        files: List[str] = os.listdir(path)
        quizs: List[QuizData] = []
        for quiz_file in filter(lambda f: os.path.splitext(f)[-1] == '.quizjson', files):
            async with aiofiles.open(os.path.join(path, quiz_file), mode='rt', encoding='utf-8') as f:
                json_text = await f.read()
                quiz = QuizData.from_json(json.loads(json_text))
                self.load_quiz(quiz)

    def load_quiz(self, quiz: QuizData):
        if isinstance(quiz, QuizData):
            self.quizs.append(quiz)
        else:
            raise TypeError('Not a QuizData object!')


bot = QuizBot()


@bot.group(
    name='admin',
    help='quiz! admin',
    alias=['관리']
)
async def admin(ctx: commands.Context):
    if ctx.author.id != bot.owner_id:
        return await ctx.send("You're not the owner of this bot.")
    else:
        pass


@admin.command(
    name='stop',
    help='quiz! admin stop',
    alias=['종료', 'close']
)
async def stop(ctx: commands.Context):
    await ctx.send('QuizBot을 종료합니다.')
    await bot.close()

with open('config.json', mode='rt', encoding='utf-8') as f:
    bot_config: JSON = json.load(f)

bot.run(bot_config['token'])
