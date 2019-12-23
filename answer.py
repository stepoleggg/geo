import pandas as pd
import random
import json
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

def get_default_keys():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Пропустить', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('Подсказка', color=VkKeyboardColor.POSITIVE)
    return keyboard

def save_data():
    with open('data/save.json', 'w') as json_file:
        json.dump(user_data, json_file)

def load_data():
    with open('data/save.json') as json_file:
        data = json.load(json_file)
        return data

df = pd.read_csv("data/data.csv")
data = {}
user_data = load_data()
for line in df[[";;;;"]].to_numpy():
    country = line[0].split(";")[0]
    capital= line[0].split(";")[1]
    side = line[0].split(";")[4]
    data[country] = capital

def answer(mes, user_id):
    user_id = str(user_id)
    if not user_id in user_data.keys():
        user_data[user_id] = {}
        user_data[user_id]["country"] = random.choice(list(data.keys()))
        user_data[user_id]["i"] = 0
        save_data()
        return "Страна: "+user_data[user_id]["country"], True, user_data[user_id]["country"], get_default_keys()
    i = user_data[user_id]["i"]
    country = user_data[user_id]["country"]
    inp = mes


    if inp == "пропустить":
        user_data[user_id]["country"] = random.choice(list(data.keys()))
        user_data[user_id]["i"] = 0
        next_country = user_data[user_id]["country"]
        save_data()
        return "Ответ: "+data[country]+"\n\nСледующая страна: "+next_country, True, next_country, get_default_keys()

    if inp.lower().replace("(","").replace(")","").replace("-","").replace(" ","") == data[country].lower().replace("(","").replace(")","").replace("-","").replace(" ",""):
        user_data[user_id]["country"] = random.choice(list(data.keys()))
        user_data[user_id]["i"] = 0
        next_country = user_data[user_id]["country"]
        save_data()
        return "Правильно!\n\nСледующая страна: "+next_country, True, next_country, get_default_keys()

    if i+1 < len(data[country]) and inp == "подсказка":
        out = "Подсказка: "+data[country][:i+1]
        i+=1
        user_data[user_id]["i"] = i
        save_data()
        return out, False, country, get_default_keys()
    
    if inp == "подсказка":
        user_data[user_id]["country"] = random.choice(list(data.keys()))
        user_data[user_id]["i"] = 0
        next_country = user_data[user_id]["country"]
        save_data()
        return "Ответ: "+data[country]+"\n\nСледующая страна: "+next_country, True, next_country, get_default_keys()
    
    if i+1 < len(data[country]):
        out = "Неверно!\nПодсказка: "+data[country][:i+1]
        i+=1
        user_data[user_id]["i"] = i
        save_data()
        return out, False, country, get_default_keys()

    

    user_data[user_id]["country"] = random.choice(list(data.keys()))
    user_data[user_id]["i"] = 0
    next_country = user_data[user_id]["country"]
    save_data()
    return "Неверно!\nОтвет: "+data[country]+"\n\nСледующая страна: "+next_country, True, next_country, get_default_keys()

    
