# -*- coding: utf-8 -*-

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import requests
import json

group_token = ''
group_id = 192176246
lastBotMsgID = 0


def write_msg(session, session_event, text):
    bot_msg = session.messages.send(
        peer_id=session_event.obj['peer_id'],
        random_id=session_event.obj['random_id'],
        message=text
    )
    print(bot_msg['message_id'])
    return bot_msg['message_id']


def edit_msg(session, session_event, msg_id):
    last_msg = session.messages.getById(message_ids=lastBotMsgID)
    print(last_msg)
    edit_text = send_request(last_msg['items'][0]['text'])
    session.messages.edit(
        peer_id=session_event.obj['peer_id'],
        message=edit_text,
        message_id=msg_id
    )


def send_request(text):
    url = 'https://models.dobro.ai/gpt2/medium/'
    header = {'Content-Type': 'application/json', 'User_Agent': 'Chrome'}
    payload = {'prompt': send_text, 'length': 30, 'num_samples': 4}
    res = requests.post(url, data=json.dumps(payload), headers=header)
    sub_res = res.json()['replies'][0]
    print(sub_res)
    return text+sub_res


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
                    lastBotMsgID = write_msg(vkK, event, send_request(send_text))
                    print(lastBotMsgID)
                elif msg_text.find('Прф дальше') == 0 or msg_text.find('прф дальше') == 0:
                    print('Continue')
                    edit_msg(vkK, event, lastBotMsgID)

    except Exception as e:
        print(e.__class__)
