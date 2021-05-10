import json
from enum import Enum
from pprint import pprint
from typing import List, Tuple, Final

from constants import NUMBER_EMOJIS, NUMBER_EMOJI_LENGTH, QuizDataKeys
from type_hints import JSON


# Markdown Quiz Text Parsers
def parse_question(line: str) -> Tuple[str, int]:
    print(f'parse_question > {line}')
    question, answer = line[3:-4], int(line[-1])
    print(f'question={question}&answer={answer}')
    return question, answer


class MdOptionType(Enum):
    INVALID = 0
    SINGLE_LINE = 1
    MULTI_LINE = 2
    COMMENT = 3
    SOLUTION = 4


COMMENT_STR: Final[str] = '//c '
SOLUTION_STR: Final[str] = '//s\n'


def check_option_line(line: str) -> MdOptionType:
    if line[0].isdigit():
        emoji_num_char: str = NUMBER_EMOJIS[int(line[0])]
        if line.startswith(emoji_num_char):
            if line.endswith(emoji_num_char):
                return MdOptionType.MULTI_LINE
            return MdOptionType.SINGLE_LINE
    elif line.startswith(COMMENT_STR):
        return MdOptionType.COMMENT
    return MdOptionType.INVALID


def parse_single_line_option(line: str) -> str:
    print(f'parse_single_line_option > "{line}"')
    return line[NUMBER_EMOJI_LENGTH:]


def parse_multi_line_option(block: str) -> str:
    print(f'parse_multi_line_option > [{block}]')
    return block[NUMBER_EMOJI_LENGTH+1:]


def parse_comment(line: str) -> str:
    print(f'parse_comment > "{line}"')
    return line[len(COMMENT_STR):]


def parse_md_quiz(name: str, text: str) -> JSON:
    questions: List[JSON] = []
    blocks: List[str] = text.split('### ')
    for block in blocks[1:]:  # blocks[0] == '' (empty string)
        print(f'Parsing block :\n{block}\n---')
        lines = block.split('\n')
        # Parse (question, answer) value.
        question, answer = parse_question(lines[0])

        # Parse options[] value.
        options: List[JSON] = []
        consume = ''
        for line in lines[1:]:  # last line == '', because \n in last option.
            if line == '':
                continue  # Don't need this line. Continue parsing next lines...

            opt_type: MdOptionType = check_option_line(line)
            print(f'MdOptionType for line "{line}" : {opt_type}')
            if opt_type == MdOptionType.SINGLE_LINE:
                options.append({
                    'text': parse_single_line_option(line),
                    'comment': None  # Temporary
                })
            elif opt_type == MdOptionType.MULTI_LINE or consume:
                if opt_type in (MdOptionType.SINGLE_LINE, MdOptionType.MULTI_LINE, MdOptionType.COMMENT) and consume:
                    # Found Next option. Stop consuming...
                    print(f'Stop consuming and start parsing option...')
                    block = consume[:consume.rfind('\n')]
                    pprint(block)
                    text = parse_multi_line_option(block)
                    if opt_type == MdOptionType.COMMENT:
                        print(f'Parse comment below the option.')
                        options.append({
                            'text': text,
                            'comment': parse_comment(line)
                        })
                        consume = ''
                        print('Start consuming new option!')
                    else:
                        print(f'No comment found. Start consuming new option!')
                        consume = line + '\n'
                else:
                    print(f'Consuming line "{line}"')
                    consume += (line + '\n')
            elif opt_type == MdOptionType.COMMENT:
                comment = line[len(COMMENT_STR):]
                options[-1]['comment'] = comment  # Patch comment in last option
            elif opt_type == MdOptionType.INVALID:
                raise ValueError('Invalid Option Syntax!')

        # Push leftovers:
        if consume:
            print(f'Stop consuming and start parsing option...')
            block = consume[:consume.rfind('\n')]
            pprint(block)
            text = parse_multi_line_option(block)
            if opt_type == MdOptionType.COMMENT:
                print(f'Parse comment below the option.')
                options.append({
                    'text': text,
                    'comment': parse_comment(line)
                })
                consume = ''
                print('Finish Parsing!')
            else:
                print(f'No comment found. Finish parsing!')

        data: JSON = {
            'question': question,
            'options': options,
            'answer': answer
        }
        pprint(data, indent=2)
        questions.append(data)

    # pprint(questions)
    quiz_json: JSON = {
        QuizDataKeys.META: {
            'name': name,
            'date': '20XX-XX-XX',
            'version': 1
        },
        QuizDataKeys.QUESTIONS: questions
    }
    return quiz_json


def parse_md_quiz_file(name: str) -> JSON:
    with open(f'quizs/md/{name}.md', mode='rt', encoding='utf-8') as f:
        questions: List[JSON] = []

        text: str = f.read()
        return parse_md_quiz(name, text)


def save_quiz(name: str, quiz_json: JSON):
    with open(f'quizs/{name}.quizjson', mode='wt', encoding='utf-8') as f:
        json.dump(quiz_json, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    save_quiz('quiz_d1', parse_md_quiz_file('quiz_d1'))

