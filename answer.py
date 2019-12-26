import pandas as pd
import random
import json
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

def load_data():
    with open('data/save.json') as json_file:
        data = json.load(json_file)
        return data

def get_default_keys():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Пропустить', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('Подсказка', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button("Список заучиваемых стран", color=VkKeyboardColor.DEFAULT)
    keyboard.add_button("Добавить "+str(n)+" новых стран", color=VkKeyboardColor.POSITIVE)


    return keyboard

def save_data():
    with open('data/save.json', 'w') as json_file:
        json.dump(user_data, json_file)

def skip_country(user_id):
    user_data[user_id]["country"] = random.choice(list(user_data[user_id]["set"]))
    user_data[user_id]["i"] = 0

def init():
    df = pd.read_csv("data/data.csv")
    for line in df[["Страна;Столица;;;"]].to_numpy():
        country = line[0].split(";")[0]
        capital = line[0].split(";")[1]
        side = line[0].split(";")[4]
        data_capitals[country] = capital

def get_set(user_id):
    return "\n".join(user_data[user_id]["set"])

def answer(mes, user_id):
    user_id = str(user_id)
    if not user_id in user_data.keys():
        user_data[user_id] = {}
        user_data[user_id]["set"] = []
        for country in data_capitals:
            if len(user_data[user_id]["set"]) < n:
                user_data[user_id]["set"].append(country)
        skip_country(user_id)
        save_data()
        return "Стартовые страны: \n\n"+get_set(user_id)+"\n\nОтгадайте столицу страны: "+user_data[user_id]["country"], True, user_data[user_id]["country"], get_default_keys()
    i = user_data[user_id]["i"]
    country = user_data[user_id]["country"]
    inp = mes

    if inp == "пропустить":
        skip_country(user_id)
        next_country = user_data[user_id]["country"]
        save_data()
        return "Ответ: "+data_capitals[country]+"\n\nСледующая страна: "+next_country, True, next_country, get_default_keys()

    if inp.lower().replace("(","").replace(")","").replace("-","").replace(" ","") == data_capitals[country].lower().replace("(","").replace(")","").replace("-","").replace(" ",""):
        skip_country(user_id)
        next_country = user_data[user_id]["country"]
        save_data()
        return "Правильно!\n\nСледующая страна: "+next_country, True, next_country, get_default_keys()

    if i+1 < len(data_capitals[country]) and inp == "подсказка":
        out = "Подсказка: "+data_capitals[country][:i+1]
        i+=1
        user_data[user_id]["i"] = i
        save_data()
        return out, False, country, get_default_keys()
    
    if inp == "подсказка":
        skip_country(user_id)
        next_country = user_data[user_id]["country"]
        save_data()
        return "Ответ: "+data_capitals[country]+"\n\nСледующая страна: "+next_country, True, next_country, get_default_keys()

    if inp == "добавить "+str(n)+" новых стран":
        current_len = len(user_data[user_id]["set"])
        for country in list(data_capitals.keys())[current_len:current_len+n]:
            user_data[user_id]["set"].append(country)
        next_country = user_data[user_id]["country"]
        save_data()
        return "Страны добавлены. Заучиваемые страны: \n\n"+get_set(user_id)+"\n\nСледующая страна: "+next_country, True, next_country, get_default_keys()

    if inp == "список заучиваемых стран":
        next_country = user_data[user_id]["country"]
        return "Заучиваемые страны: \n\n"+get_set(user_id)+"\n\nСледующая страна: "+next_country, True, next_country, get_default_keys()
    
    if i+1 < len(data_capitals[country]):
        out = "Неверно!\nПодсказка: "+data_capitals[country][:i+1]
        i+=1
        user_data[user_id]["i"] = i
        save_data()
        return out, False, country, get_default_keys()

    skip_country(user_id)
    next_country = user_data[user_id]["country"]
    save_data()
    return "Неверно!\nОтвет: "+data_capitals[country]+"\n\nСледующая страна: "+next_country, True, next_country, get_default_keys()


n = 5
data_capitals = {}
data_sides = {}
user_data = load_data()
init()
