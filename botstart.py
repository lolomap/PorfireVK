# -*- coding: utf-8 -*-

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import requests
import json

def WriteMsg(session, event, text):
    session.messages.send(
        peer_id = event.obj['peer_id'],
        random_id = event.obj['random_id'],
        message = text
    )


def SendRequest(send_text, session, event):
    url = 'https://models.dobro.ai/gpt2/medium/'
    header = {'Content-Type': 'application/json',
               'User_Agent': 'Chrome'}
    payload = {'prompt':send_text, 'length':30, 'num_samples':4}
    res = requests.post(url, data=json.dumps(payload), headers=header)
    sub_res = res.json()['replies'][0]
    print(sub_res)
    WriteMsg(session, event, send_text+sub_res)

group_token = ''
group_id = 192176246

while True:
    try:
        vk_session = vk_api.VkApi(token=group_token)
        longpoll = VkBotLongPoll(vk_session, group_id)
        vkK = vk_session.get_api()
        print('STARTED')

        msg_text = ''
        send_text = ''
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                msg_text = event.obj['text']
                if msg_text.find('Прф, ') == 0 or msg_text.find('прф, ') == 0:
                    send_text = msg_text[5:]

                    SendRequest(send_text, vkK, event)
    except:
        continue

