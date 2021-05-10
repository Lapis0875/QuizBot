from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Tuple, Union, List

from discord import Embed

from constants import NUMBER_EMOJIS, QuizKeys, QuizDataKeys, QuizOptionKeys, QuizMetaKeys
from type_hints import JSON


class JsonObject(ABC):

    @classmethod
    @abstractmethod
    def from_json(cls, data: JSON) -> JsonObject:   ...

    @abstractmethod
    def to_json(self) -> JSON:  ...


class QuizOption(JsonObject):
    """
    Represents QuizOption object in quiz.json file.
    Example:
    ```json
    {
        "text": "`printf`",
        "comment": "c언어에서 사용하는 출력 함수"
    }
    ```
    """
    # property type hints
    text: str
    comment: Optional[str]

    @classmethod
    def from_json(cls, data: JSON) -> QuizOption:
        return cls(
            text=data[QuizOptionKeys.TEXT],
            comment=data.get(QuizOptionKeys.COMMENT)
        )

    def __init__(
            self,
            text: str,
            comment: Optional[str] = None
    ):
        self.text = text
        self.comment = comment

    def to_json(self) -> JSON:
        data = {
            QuizOptionKeys.TEXT: self.text
        }
        if self.comment:
            data[QuizOptionKeys.COMMENT] = self.comment
        return data


class Quiz(JsonObject):
    """
    Represents QuizOption object in quiz.json file.
    Example:
    ```json
    {
      "question": "다음 중 Python에서 콘솔에 값을 출력하기 위해 사용하는 함수는?",
      "options": [
        {
          "text": "`printf`",
          "comment": "c언어에서 사용하는 출력 함수"
        },
        {
          "text": "`println!`",
          "comment": "Rust언어에서 사용하는 출력 매크로"
        },
        {
          "text": "`cout`",
          "comment": "c++ 언어에서 사용하는 출력 키워드"
        },
        {
          "text": "`print`",
          "comment": "Python 언어에서 사용하는 출력 함수"
        }
      ],
      "answer": 3
    }
    ```
    """
    # property type hints
    question: str
    options: Tuple[QuizOption]
    answer: Union[int, List[int]]

    @classmethod
    def from_json(cls, data: JSON) -> Quiz:
        return cls(
            question=data[QuizKeys.QUESTION],
            options=tuple((
                QuizOption.from_json(data) for data in data[QuizKeys.OPTIONS]
            )),
            answer=data[QuizKeys.ANSWER]
        )

    def __init__(
            self,
            question: str,
            options: Tuple[QuizOption],
            answer: Union[int, List[int]]
    ):
        self.question = question
        self.options = options
        self.answer = answer

    @property
    def has_multi_answers(self) -> bool:
        return isinstance(self.answer, list)

    def to_json(self) -> JSON:
        return {
            QuizKeys.QUESTION: self.question,
            QuizKeys.OPTIONS: [
                opt.to_json() for opt in self.options
            ],
            QuizKeys.ANSWER: self.answer

        }

    def text(self, index: int) -> str:
        """
        Returns prettier text to send in discord channel.
        """
        text: str = f'> {index}. {self.question}\n'
        for index, option in enumerate(self.options):
            text += f'{NUMBER_EMOJIS[index+1]} {option.text}\n'
        return text

    def answer_embed(self, index: int, guild_id: int, quiz_channel_id: int, quiz_msg_id: int) -> Embed:
        embed = Embed(title=f'{index}. {self.question}')
        for i, option in enumerate(self.options):
            if not option.text.startswith('```'):
                embed.add_field(name=f'{NUMBER_EMOJIS[i + 1]} {option.text}', value=option.comment, inline=False)
            else:
                embed.add_field(
                    name=f'{NUMBER_EMOJIS[i+1]} (code below)',
                    value=option.comment + f'\n[보기 코드 바로가기](https://discord.com/channels/{guild_id}/{quiz_channel_id}/{quiz_msg_id})',
                    inline=False
                )
        return embed


class QuizData(JsonObject):
    @classmethod
    def from_json(cls, data: JSON) -> QuizData:
        return cls(
            meta=data[QuizDataKeys.META],
            quizs=tuple((
                Quiz.from_json(data) for data in data[QuizDataKeys.QUESTIONS]
            ))
        )

    def __init__(self, meta: JSON, quizs: Tuple[Quiz]):
        self._meta = meta
        self.questions = quizs

    def to_json(self) -> JSON:
        return {
            QuizDataKeys.META: self._meta,
            QuizDataKeys.QUESTIONS: [
                quiz.to_json() for quiz in self.questions
            ]
        }

    def __eq__(self, other) -> bool:
        if isinstance(other, QuizData):
            return (
                    self._meta[QuizMetaKeys.NAME] == other._meta[QuizMetaKeys.NAME]
                    and self._meta[QuizMetaKeys.DATE] == other._meta[QuizMetaKeys.DATE]
                    and self._meta[QuizMetaKeys.VERSION] >= other._meta[QuizMetaKeys.VERSION]
            )
        return False

