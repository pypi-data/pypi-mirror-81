import requests
import random


url = "https://api.npoint.io/48b5daffd44719ddc625"
data = requests.get(url).json()
types = ", ".join(list(data[0].values())[0])
catagory_list = list(data[0].values())[0]

welcome = f"""ברוך הבא לpyjokes-hebrew!
ביכולתכם לקבל בדיחה רנדומלית בעברית על ידי המתודה get_random_joke
או לקבל בדיחה רנדומלית מקטגוריה מסויימת על ידי המתודה catagory_joke שמקבלת קטגוריה כפרמטר
הקטגוריות השונות הן {types}
רוטמ רביד אוהב ממש לחדד
בברכה קובי שוצי
"""


catagory_error = f"בבקשה תכניס קטגוריה מהקטגוריות הבאות: {types}"

def get_random_joke():
    random_index = random.randint(1, 10)
    joke_list = list(data[random_index].values())
    joke_index = random.randint(0, len(joke_list[0])-1)
    return joke_list[0][joke_index]


def category_joke(catagory = None):
    if catagory is None or catagory == "" or catagory not in catagory_list:
        return catagory_error
    else:
        catagory_index = catagory_list.index(catagory)+1
        joke_list = list(data[catagory_index].values())
        joke_index = random.randint(0, len(joke_list[0]) - 1)
        # print(random_index, joke_index)
        return joke_list[0][joke_index]


def help():
    return welcome







