from codecs import escape_encode
from doctest import Example
import random

# сравнивает строки
def text_match(user_text, example):
    # приводим к нужному регистру
    example = example.lower()
    user_text = user_text.lower()

    # теперь еще нужно в конце спец.символы убрать (Привет == Привет!!!)
    # можно сделать с помощью регулярных выражений - удалить в строке все сзнаки припинания
    
    return user_text == example

# фильтрация = очистка текста
def filter_text(text):
    text = text.lower()
    return text

text = input()
if text in ['Hi', "hello"]:
    print(random.choice(["hello", "heyo"]))
elif text in ["buy", "poki"]:
    print(random.choice(["wait for our cita", "bao"]))
else:
    print("did not get it")

