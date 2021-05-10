# QuizBot
QuizBot is a bot made with Python 3.8, discord.py 1.7
Currently targeting a single-server-specialized bot for education purpose.
This bot is created to automate quiz system on discord. It supports asking questions, explain answers for questions, and checking student(discord user)'s answers on quiz.

## config.json
When setting up your QuizBot, you must manually create `config.json` on QuizBot's root directory.
`config.json` contains bot's configuration values. Currently, `token` is the only value in config.
```json
{
  "token": "YOUR_BOT_TOKEN"
}
```

## quiz_tracking_data.json
This file is a json storage of quiz data.
Currently it is used to manage discord object (message, channel, guild)'s ids to check student's answers.
When setting up your QuizBot, you must manually create `quiz_tracking_data.json` on QuizBot's root directory.