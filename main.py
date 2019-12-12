import pandas as pd
import random
import json

def save_data():
    with open('save.json', 'w') as json_file:
        json.dump(user_data, json_file)

def load_data():
    with open('save.json') as json_file:
        data = json.load(json_file)
        return data


df = pd.read_csv("data.csv")
data = {}
user_data = load_data()
for line in df[[";;;;"]].to_numpy():
    country = line[0].split(";")[0]
    capital= line[0].split(";")[1]
    data[country] = capital




def answer(mes, user_id):
    user_id = str(user_id)
    if not user_id in user_data.keys():
        user_data[user_id] = {}
        user_data[user_id]["country"] = random.choice(list(data.keys()))
        user_data[user_id]["i"] = 0
        save_data()
        return "Страна: "+user_data[user_id]["country"]
    i = user_data[user_id]["i"]
    country = user_data[user_id]["country"]
    inp = mes

    if inp == "0":
        user_data[user_id]["country"] = random.choice(list(data.keys()))
        user_data[user_id]["i"] = 0
        next_country = user_data[user_id]["country"]
        save_data()
        return "Ответ: "+data[country]+"\n\nСледующая страна: "+next_country

    if inp.lower().replace("(","").replace(")","").replace("-","").replace(" ","") == data[country].lower().replace("(","").replace(")","").replace("-","").replace(" ",""):
        user_data[user_id]["country"] = random.choice(list(data.keys()))
        user_data[user_id]["i"] = 0
        next_country = user_data[user_id]["country"]
        save_data()
        return "Правильно!\n\nСледующая страна: "+next_country
    
    if i+1 < len(data[country]):
        out = "Неверно!\nПодсказка: "+data[country][:i+1]
        i+=1
        user_data[user_id]["i"] = i
        save_data()
        return out

    user_data[user_id]["country"] = random.choice(list(data.keys()))
    user_data[user_id]["i"] = 0
    next_country = user_data[user_id]["country"]
    save_data()
    return "Неверно!\nОтвет: "+data[country]+"\n\nСледующая страна: "+next_country

    
