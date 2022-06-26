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
   "how-are-you": {         
        "examples": ['Как дела', "Чем занят", "Че по чем"], 
        "response": ["Вроде ничего", "На чиле, на расслабоне"],
    },
    "unknown": {
        "examples": ['не знаю'],
        "response": ['не понимаю'],
    },
    "stop": {
        "examples": ["выход", "stop", "exit"],
        "response": ["понял, выхожу", "очень жаль, пока!", "до свидания!"],
    }
#    "time": {
#        "examples": [],
#        "response": # ответ на запрос времени - какая-то уже функция, просто фик.вариант не подойдет
#    }
} # можно поместить в файл или в БД

def get_intent(text): # определить намерение по тексту : Чем занят => how-are-you
    # проверить все существующие интенты - один из них может иметь example похожий на text
    for intent_name in INTENTS.keys():
        examples = INTENTS[intent_name]["examples"]
        for example in examples:
            if text_match(text, example):
                return intent_name
    return "unknown"

def get_response(intent): # вернуть по интенту один из ответов : hello => Йоу
    return random.choice(INTENTS[intent]["response"])

def bot(text): # найти намерение по тексту
    intent = get_intent(text)
    if not intent:
        print("ничего не понял")
    else: # если намерение найдено
        print(get_response(intent))

# bot("чем занят")

# непрерывный цикл по вводу с ботом
text = ""
while text != "stop":
    text = input()
    bot(text)

# первоначальная фильтрация
# text = filter_text(input())
# text = ""
#if text in ['hi', "hello"]:
#    print(random.choice(["hello", "heyo"]))
#elif text in ["buy", "poki"]:
#    print(random.choice(["wait for our cita", "bao"]))
#else:
#    print("did not get it")

# пример определения похожести слов
# print(nltk.edit_distance("превет", "привет!"))
