# -*- coding: utf-8 -*-

import requests
import json
import MESSAGES_TYPES


def msg_process(msg_text):
    for msg in MESSAGES_TYPES.MSG_GENERATE:
        if msg_text.lower().find(msg) == 0:
            return {'type': 'MSG_GENERATE', 'command': msg}
    for msg in MESSAGES_TYPES.MSG_NEXT_GENERATE:
        if msg_text.lower().find(msg) == 0:
            return {'type': 'MSG_NEXT_GENERATE'}
    for msg in MESSAGES_TYPES.MSG_CHANGE:
        if msg_text.lower().find(msg) == 0:
            return {'type': 'MSG_CHANGE'}
    return {'type': 'Message'}


def write_msg(session, session_event, text, sticker_id=None, picture=None):
    bot_msg = None
    if text and picture is None:
        bot_msg = session.messages.send(
            peer_id=session_event.obj['peer_id'],
            random_id=session_event.obj['random_id'],
            message=text
        )
    if sticker_id is not None:
        bot_msg = session.messages.send(
            peer_id=session_event.obj['peer_id'],
            random_id=session_event.obj['random_id'],
            sticker_id=sticker_id
        )
    if picture is not None:
        photo_file = session.photos.getMessagesUploadServer(
            peer_id=session_event.obj['peer_id'])
        r_data = {'photo': open('images/pitivo.jpg', 'rb')}
        photo_data = requests.post(photo_file['upload_url'], files=r_data).json()
        print(photo_data)
        photo = session.photos.saveMessagesPhoto(server=photo_data['server'],
                                                 photo=photo_data['photo'],
                                                 hash=photo_data['hash'])[0]
        print('PHOTO UPLOADED')
        bot_msg = session.messages.send(
            peer_id=session_event.obj['peer_id'],
            random_id=session_event.obj['random_id'],
            message=text,
            attachment='photo{0}_{1}'.format(photo['owner_id'], photo['id'])
        )
    print(bot_msg)
    return bot_msg


def edit_msg(session, session_event, msg_id, last_msg):
    last_msg_text = last_msg[session_event.obj['peer_id']]
    edit_text = send_request(last_msg_text)
    try:
        session.messages.edit(
            peer_id=session_event.obj['peer_id'],
            message=edit_text,
            message_id=msg_id
        )
    except Exception as ee:
        print(ee)
        write_msg(session, session_event, edit_text)
    return edit_text


def send_request(text):
    url = 'https://models.dobro.ai/gpt2/medium/'
    header = {'Content-Type': 'application/json', 'User_Agent': 'Chrome'}
    payload = {'prompt': text, 'length': 30, 'num_samples': 4}
    res = requests.post(url, data=json.dumps(payload), headers=header)
    sub_res = res.json()['replies'][2]
    print(sub_res)
    return text+sub_res


def save_last_msg(session_event, text, dictionary):
    peer_id = session_event.obj['peer_id']
    dictionary[peer_id] = text

