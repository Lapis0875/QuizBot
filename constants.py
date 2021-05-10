from typing import Final

NUMBER_EMOJIS = {
    0: '0️⃣',
    1: '1️⃣',
    2: '2️⃣',
    3: '3️⃣',
    4: '4️⃣',
    5: '5️⃣',
    6: '6️⃣',
    7: '7️⃣',
    8: '8️⃣',
    9: '9️⃣',
    10: '🔟',
}

NUMBER_EMOJI_LENGTH = len(NUMBER_EMOJIS[0])


class QuizDataKeys:
    META: Final[str] = 'meta'
    QUESTIONS: Final[str] = 'questions'


class QuizMetaKeys:
    NAME: Final[str] = 'name'
    DATE: Final[str] = 'date'
    VERSION: Final[str] = 'version'


class QuizKeys:
    QUESTION: Final[str] = 'question'
    OPTIONS: Final[str] = 'options'
    ANSWER: Final[str] = 'answer'


class QuizOptionKeys:
    TEXT: Final[str] = 'text'
    COMMENT: Final[str] = 'comment'

