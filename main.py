from codecs import escape_encode
from operator import truediv
import random
import re
from telnetlib import BINARY
import nltk
import json

# https://colab.research.google.com/drive/1ZlF2Q9_jwE_KgMDcU3VlhoHfsTykoIvT?usp=sharing#scrollTo=hSSID1qhTRst - skillbox demo

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
        if intent == "stop" :
            return 1
        else:
            return 0


with open("big_bot_config.json","r") as config_file:
    BIG_INTENTS = json.load(config_file)
# print(BIG_INTENTS.keys())
# задача: научить модель опрелять интент по тексту - это называется классификацией текстов
# строчка на вход - модель предсказывает класс текста (интент фразы)
# 1) входные данные Х
# 2) выходные данные - У
# модель учится на наших примерах и может предсказывать интенты по фразе

INTENTS_JSON = BIG_INTENTS['intents']
x = [] # фразы 
y = [] # интенты
for name, intent in INTENTS_JSON.items():
    # print (name)
    for phrase in intent['examples']: # смотрим все фразы для интента и записываем
        x.append(phrase)
        y.append(name)
    for phrase in intent['responses']:
        x.append(phrase)
        y.append(phrase)
    
# print(len(x),"Y :",len(y))

# векторизация текстов - превратить текст в набор чисел (вектор) - можно понять, что написано в тексте = sklearn library
import sklearn

# сначала просто проверка, как работает библиотека и как иницициализируется простейший векторайзер

# Задача Векторизации текста
#"текст" => [1,2,3]
#Большой набор текстов
#Векторайзер обучается
#Векторайзер готов работать с новыми текстами
#Пример
#
#1. Набор текстов = {
#  "мама мыла раму", 
#  "мыла раму мама",
#  "раму мама мыла",
#}
#2. Обучение
#мама = 1, мыла = 2, раму = 3
#  "мама мыла раму" = [1,2,3]
#  "мыла раму мама" = [2,3,1]
#  "раму мама мыла" = [3,1,2]
#3. Векторизация
#"мама мама мама" = [1,1,1]
# "как мама мыла раму" = [0,1,2,3]

from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer()
vectorizer.fit(x) # обучением векторайзер

# dense = [0,0,0,0,0,00,0,0, 2, 0,0,0,0,0,00,0,0,0,6, 0,0,0,1]
# sparse = [ ... 2, ...6,..1]

# for i in vectorizer.transform(["как дела чем занят"]).toarray()[0]:
#    if i!= 0:
#        print(i,end=',')

# используем классификатор на основе нейронных сетей
#from sklearn.neural_network import MLPClassifier
#mlp_model = MLPClassifier() # создаем модель
vecX = vectorizer.transform(x) # преобразуем тексты в вектора
#mlp_model.fit(vecX,y) # обучаем модель

# качество на тренировочной выборе = accuracy модели / больше = лучше
#mlp_model.score(vecX, y)

# модель Random Forest
from sklearn.ensemble import RandomForestClassifier
rf_model = RandomForestClassifier()
rf_model.fit(vecX, y)
rf_model.score(vecX, y)

MODEL = rf_model

def get_intent_ml(text):
    vec_text = vectorizer.transform([text])
    intent = MODEL.predict(vec_text)[0]


# bot("чем занят")

# непрерывный цикл по вводу с ботом
# text = ""
#while True:
#    text = input()
#    if bot(text):
#        break

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
