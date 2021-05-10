# QuizBot
QuizBot is a bot made with Python 3.8, discord.py 1.7
Currently targeting a single-server-specialized bot for education purpose.
This bot is created to automate quiz system on discord. It supports asking questions, explain answers for questions, and checking student(discord user)'s answers on quiz.

## Setting up your own QuizBot :
### config.json
When setting up your QuizBot, you must manually create `config.json` on QuizBot's root directory.
`config.json` contains bot's configuration values. Currently, `token` is the only value in config.
```json
{
  "token": "YOUR_BOT_TOKEN"
}
```

### quiz_tracking_data.json
This file is a json storage of quiz data.
Currently it is used to manage discord object (message, channel, guild)'s ids to check student's answers.
When setting up your QuizBot, you must manually create `quiz_tracking_data.json` on QuizBot's root directory.

## How to create my own quiz data?
Quiz data has own structure:
```json5
{
  "meta": {
    // Metadata of this quiz file.
    "name": "quiz_d1",
    // quiz's name. This is used on bot's commands to indicate specific quiz.
    "date": "2021-05-09",
    // quiz's date info. It means when the quiz is created.
    "version": 1
    // quiz file format version. It is '1' for now.
  },
  "questions": [
    // Array of question object
    {
      "question": "Choose either A or B.",
      // Question to display.
      "options": [
        // Options which students can choose on this question.
        {
          "text": "A",
          "comment": "It's A."
        },
        {
          "text": "B",
          "comment": "It's B."
        }
      ],
      "answer": 2
      // answer can be either integer(single answer) or array of integer(multiple answers)
    }
  ]
}
```
This json file must be saved in `(QuizBot's Root)/quizs` directory, with name `(name).quizjson`.
You can manually write the `.quizjson` file, or parse from Markdown content.

### md_parse
`md_parse` is a python script parsing special Markdown syntax into `.quizjson` structure.
First, these are Markdown Syntaxn that can be parsed in `md_parse` module.
#### Markdown content must be like this:
```md
### (index: int). (question: string) : (answer: int | Array<int>)
(option: Array<Sytanx:SingleLineOption | Syntax:MultiLineOption>)
(solution: Optional<string>)
```
data parsed in upper syntax:
> - index : Question's index.\
> - question : Question's text. This is used in `.quizjson` structure.\
> - answer : Question's answer.\
> - option : Either SingleLineOption syntax or MultiLineOption syntax. This is sed in `.quizjson` structure to form question's options.\
> - solution : Solution of this question. Solution must start with a string '//s ' (must contain blank after //s). This contains a single explanation of this question, while comment means explanation of each option.\

#### SingleLineOption Syntax:
```md
(number emoji: string) (text: string)
(comment: Optional<string>)
```
data parsed in upper syntax:
> - number emoji : emojis like 1️⃣. You must indicate index of options by these emojis (Sorry for bad parser..)\
> - text : option's text. This is used in `.quizjson` structure.
> - comment : option's comment. Comment must start with a string '//c '(single blank must be included right after //c). This is used in `.quizjson` structure.

#### MultiLineOption Syntax:
```md
(number emoji: string)
(text: string)
(comment: Optional<string>)
```
data parsed in upper syntax:
> - number emoji : emojis like 1️⃣. You must indicate index of options by these emojis (Sorry for bad parser..)\
> - text : option's text. This is used in `.quizjson` structure.
> - comment : option's comment. Comment must start with a string '//c '(single blank must be included right after //c). This is used in `.quizjson` structure.

#### Example markdown quiz:
```md
### 1. `1 2 3` 이라고 콘솔에 출력하려면 어떤 코드를 사용해야 하는가? : 1
1️⃣
```py
print(1, 2, 3)
```
//c print 함수에 ,로 여러 객체를 전달하면, 각 객체 사이에 공백을 두고 출력한다.

2️⃣
```py
print(123)
```
//c 이 경우, `123` 이 출력된다.

3️⃣
```py
print(1+2+3)
```
//c 이 경우, `6` 이 출력된다.
### 2.  Python에서 컨테이너 자료형이 아닌 것은? : 4
1️⃣ `dict`
//c dict는 컨테이너 자료형 중 하나로, 내부에 다른 객체를 보관할 수 있다.

2️⃣ `tuple`
//c tuple 컨테이너 자료형 중 하나로, 내부에 다른 객체를 보관할 수 있다.

3️⃣ `list`
//c list 컨테이너 자료형 중 하나로, 내부에 다른 객체를 보관할 수 있다.

4️⃣ `str`
//c str은 문자열으로, 내부에 다른 객체를 보관할 수 없다.
### 12. Python에서 문자열을 표현하는 방법으로 옳은 것을 모두 고르시오. : 1, 2, 3, 4
1️⃣
```py
var = 'Hello World!'
```
//c Python에서는 작은따옴표(`'`)또는 큰따옴표(`"`)로 감싸 문자열을 표현할 수 있다. 

2️⃣
```py
var = "Hello World!"
```
//c Python에서는 작은따옴표(`'`)또는 큰따옴표(`"`)로 감싸 문자열을 표현할 수 있다.

3️⃣
```py
var = """
Hello World!
"""
```
//c Python에서는 작은따옴표(`'`)또는 큰따옴표(`"`)를 3개씩 사용하면, 다중행 문자열(multiline string)을 만들 수 있다. 다중행 문자열은 엔터를 사용해 개행해서 쓸 수 있으며, 이는 문자열 내에서 `\n`으로 표현된다.

4️⃣
```py
var = '''
Hello World!
'''
```
//c Python에서는 작은따옴표(`'`)또는 큰따옴표(`"`)를 3개씩 사용하면, 다중행 문자열(multiline string)을 만들 수 있다. 다중행 문자열은 엔터를 사용해 개행해서 쓸 수 있으며, 이는 문자열 내에서 `\n`으로 표현된다.
```