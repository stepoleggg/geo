"""
Функции отвечающие за отправку сообщений
"""
from vk_api.utils import get_random_id
from vk_api.upload import VkUpload
import vk_api
from time import sleep
from threading import Thread
import urllib
from random import choice
from string import ascii_lowercase
import os.path
from os import path
import requests
import re

def _send_message(vk, id, message, sleep_time=5, keyboard=None, attachment=None):
    """
    имитирует typing, отправляет сообщение через sleep_time
    Проверяет на блок
    """
    try:
        if id>0:
            vk.messages.setActivity(user_id=id, type="typing")
    
            sleep(sleep_time)
    
            vk.messages.send( 
                                user_id=id,
                                random_id=get_random_id(),
                                keyboard=keyboard,
                                message=message,
                                attachment=attachment
                                )

    except vk_api.exceptions.ApiError as e:
        print(e)


def load_image(url):
    random_name = "tmp/"+''.join(choice(ascii_lowercase) for i in range(12))+url[-4:]
    if not path.exists('tmp'):
        os.mkdir('tmp')
    urllib.request.urlretrieve(url, random_name)
    return random_name

def get_flag_url(country):
    result = requests.get('https://geo.koltyrin.ru/country.php?country='+country)
    s = result.content
    res = re.findall(r'img\/country\/\d+flag\.png"\s+alt=', s.decode("utf-8"))
    res = res[0][0:-6]
    return "https://geo.koltyrin.ru/"+res

def send_message(kwargs):
    """
    Обертка для _send_message, выполняется в потоке, не блогирует цикл
    send_message({"vk": vk, "id": vk_id, "message": "da", "sleep_time": 0, "keyboard": None, "attachment": None})
    """
    Thread(target=_send_message, kwargs=kwargs, name="Message sender").start()

def _send_photo_path(vk, id, text, photo_path, delete=True):
    upload = VkUpload(vk)
    uploaded = upload.photo_messages(photo_path)
    if path.exists(photo_path) and delete:
        os.remove(photo_path)
    photo = 'photo'+str(uploaded[0]['owner_id'])+'_'+str(uploaded[0]['id'])
    send_message({"vk": vk, "id": id, "message": text, "sleep_time": 0, "attachment": photo})

def _send_photo_url(vk, id, text, url, delete=True):
    path = load_image(url)
    send_photo_path(vk, id, text, path, delete)




def send_text(vk, id, text):
    send_message({"vk": vk, "id": id, "message": text, "sleep_time": 0})

def send_photo_path(vk, id, text, path, delete):
    kwargs = {"vk": vk, "id": id, "text": text, "photo_path": path, "delete": delete}
    Thread(target=_send_photo_path, kwargs=kwargs, name="Photo path sender").start()

def send_photo_url(vk, id, text, url, delete):
    kwargs = {"vk": vk, "id": id, "text": text, "url": url, "delete": delete}
    Thread(target=_send_photo_url, kwargs=kwargs, name="Photo url sender").start()