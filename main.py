"""
термометр
154fa7d48b23e0a839526061f3bb2591a289aee3e5dfe9e33deb15f45a2c1ef8711d061e61e0f72259d99

географ
2136beb30b1f745b0670dce6e1a222ff0e19594e732a59144b4fea671da7eb9c0e2ff254d1db5229572ad
"""


import vk_api
import message
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import answer

vk_session = vk_api.VkApi(token="131f746751891d088e9fcbe31dbbf8f092c88f1034226bf45271f3e109619423c748c68b7683599cca97d")
longpoll = VkBotLongPoll(vk_session, "189739538")
vk = vk_session.get_api()

print("Bot started")

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        text_message = event.obj.text.lower() 
        vk_id = event.obj.from_id
        response, flag, country = answer.answer(text_message, vk_id)
        if flag:
            message.send_photo_url(vk, vk_id, response, message.get_flag_url(country), True)
        else:
            message.send_text(vk, vk_id, response)