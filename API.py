# -*- coding: utf-8 -*-

import requests
import json
from Bot import BotData

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


def create_session():
    print(BotData.group_token, BotData.group_id)
    api = vk_api.VkApi(token=BotData.group_token)
    longpoll = VkBotLongPoll(api, BotData.group_id)
    session = api.get_api()
    print('session created')
    return {'session': session, 'longpoll': longpoll}


def get_user(user_id):
    print('ug')
    return BotData.session.users.get(user_ids=user_id)


def get_conversation(peer_id):
    return BotData.session.messages.getConversationsById(peer_id=peer_id)['items']


def get_conversation_members(peer_id):
    return BotData.session.messages.getConversationMembers(peer_id=peer_id)['profiles']


def get_event_type(event):
    print('etg')
    if event.type == VkBotEventType.MESSAGE_NEW:
        return 'MESSAGE_NEW'


def write_msg(session_event, text, sticker_id=None, picture=None):
    bot_msg = None
    if text and picture is None:
        bot_msg = BotData.session.messages.send(
            peer_id=session_event.obj['peer_id'],
            random_id=session_event.obj['random_id'],
            message=text
        )
    if sticker_id is not None:
        bot_msg = BotData.session.messages.send(
            peer_id=session_event.obj['peer_id'],
            random_id=session_event.obj['random_id'],
            sticker_id=sticker_id
        )
    if picture is not None:
        photo_file = BotData.session.photos.getMessagesUploadServer(
            peer_id=session_event.obj['peer_id'])
        r_data = {'photo': open('images/pitivo.jpg', 'rb')}
        photo_data = requests.post(photo_file['upload_url'], files=r_data).json()
        photo = BotData.session.photos.saveMessagesPhoto(server=photo_data['server'],
                                                         photo=photo_data['photo'],
                                                         hash=photo_data['hash'])[0]
        bot_msg = BotData.session.messages.send(
            peer_id=session_event.obj['peer_id'],
            random_id=session_event.obj['random_id'],
            message=text,
            attachment='photo{0}_{1}'.format(photo['owner_id'], photo['id'])
        )
    return bot_msg


def edit_msg(session_event, msg_id, last_msg):
    last_msg_text = last_msg[session_event.obj['peer_id']]
    edit_text = send_request(last_msg_text)
    try:
        BotData.session.messages.edit(
            peer_id=session_event.obj['peer_id'],
            message=edit_text,
            message_id=msg_id
        )
    except Exception as ee:
        print(ee)
        write_msg(session_event, edit_text)
    return edit_text


def send_request(text):
    url = 'https://models.dobro.ai/gpt2/medium/'
    header = {'Content-Type': 'application/json', 'User_Agent': 'Chrome'}
    payload = {'prompt': text, 'length': 30, 'num_samples': 4}
    res = requests.post(url, data=json.dumps(payload), headers=header)
    sub_res = res.json()['replies'][2]
    return text+sub_res


def save_last_msg(session_event, text, dictionary):
    peer_id = session_event.obj['peer_id']
    dictionary[peer_id] = text

