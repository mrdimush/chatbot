from codecs import escape_encode
from operator import truediv
import random
import re
import nltk

# сравнивает строки
def text_match(user_text, example):
    # приводим к нужному регистру
    example = filter_text(example)
    user_text = filter_text(user_text)
    # теперь еще нужно в конце спец.символы убрать (Привет == Привет!!!)
    # можно сделать с помощью регулярных выражений - удалить в строке все сзнаки припинания

    if user_text.find(example) != -1: # нашли подстроку : Привет, как дела == Привет
        return True

    if example.find(user_text) != -1: # 
        return True

    # опечатки : Превет == привет (метод levenstein = nltk library) = расстояние левенштейна - похожесть языков
    distance = nltk.edit_distance(user_text, example)
    # она не отработает на "привет, как дела?" != "привет", хотя смысл как бы тот же самый

    example_len = len(example)
    difference = distance / example_len # на сколько в % отличаются фразы

    # 40% - норм (пока так считаем)
    return difference < 0.4

# фильтрация = очистка текста
def filter_text(text):
    text = text.lower()
    my_expression = r'[^\w\s]' # все, что не слово и не пробел
    text = re.sub(my_expression, '', text) # заменить по выражению все на пустую строку = удалить все лишнее | Привет!!! =>  привет
    return text


# определение намерения пользователя - это функция бота
#  {вопрос на входе} => {алгоритм ответа} => {ответ на выходе}
# база вопросов => выбирался нужны вопрос с помощью функции text_match => выдать вариант ответа
INTENTS = {
    "hello": {          # зачем пользователь написал слово = угадать намерение
        "examples": ['Привет', "Хеллоу", "Хай"], 
        "response": ["Здрасьте", "Йоу"],
    },
#    "time": {
#        "examples": [],
#        "response": # ответ на запрос времени - какая-то уже функция, просто фик.вариант не подойдет
#    }
}

# text = filter_text(input())
text = ""
if text in ['hi', "hello"]:
    print(random.choice(["hello", "heyo"]))
elif text in ["buy", "poki"]:
    print(random.choice(["wait for our cita", "bao"]))
else:
    print("did not get it")


# print(nltk.edit_distance("превет", "привет!"))
