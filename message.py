"""
Функции отвечающие за отправку сообщений
"""
from vk_api.utils import get_random_id
import vk_api
from time import sleep
from threading import Thread

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

def send_message(kwargs):
    """
    Обертка для _send_message, выполняется в потоке, не блогирует цикл
    send_message({"vk": vk, "id": vk_id, "message": "da", "sleep_time": 0, "keyboard": None, "attachment": None})
    """
    Thread(target=_send_message, kwargs=kwargs, name="Message sender").start()