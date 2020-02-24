#!/usr/bin/python
# -*- coding: utf-8 -*-

import API
import random
import BotData
import MESSAGES_TYPES


def connect_vk():
    vk = API.create_session()
    BotData.session = vk['session']
    BotData.longpoll = vk['longpoll']


def get_event_info(event):
    print('in')
    info = {'type': API.get_event_type(event),
            'user': API.get_user(event.obj['from_id'])[0],
            'peer': event.obj['peer_id'],
            'text': event.obj['text']}
    return info


def check_event_type(event, needed_event_type):
    if API.get_event_type(event) == needed_event_type:
        return True
    else:
        return False


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
    for msg in MESSAGES_TYPES.MSG_GET_ACTION:
        if msg_text.lower().find(msg) == 0:
            return {'type': 'MSG_GET_ACTION'}
    return {'type': 'Message'}


def generate(msg_text, command, event):
    send_text = msg_text[len(command):]
    API.save_last_msg(event, send_text, BotData.saveBotMsg)

    BotData.lastBotMsgText = API.send_request(send_text)

    API.save_last_msg(event, BotData.lastBotMsgText, BotData.lastBotMsg)

    BotData.lastBotMsgID = API.write_msg(event, BotData.lastBotMsgText)
    BotData.lastCmdType = 'MSG_GENERATE'


def witless_generate(msg_text, event):
    rand_generate = random.randint(1, 100)
    if rand_generate <= 10:
        API.write_msg(event, API.send_request(msg_text))


def next_generate(event):
    API.save_last_msg(event, BotData.lastBotMsgText, BotData.saveBotMsg)
    BotData.lastBotMsgText = API.edit_msg(event, BotData.lastBotMsgID, BotData.lastBotMsg)
    API.save_last_msg(event, BotData.lastBotMsgText, BotData.lastBotMsg)
    BotData.lastCmdType = 'MSG_NEXT_GENERATE'


def change(event):
    BotData.lastBotMsgText = API.edit_msg(event, BotData.lastBotMsgID, BotData.saveBotMsg)
    API.save_last_msg(event, BotData.lastBotMsgText, BotData.lastBotMsg)
    BotData.lastCmdType = 'MSG_CHANGE'


def get_activity(event):
    print(BotData.conversation_statistics)
    act_list = BotData.conversation_statistics[event.obj['peer_id']]['message_count']
    msg = ''
    print(act_list)
    for user in act_list.keys():
        msg = msg + user + '   ' + act_list[user]
    API.write_msg(event, msg)


def easter_egg_request(session_event):
    if session_event.obj['text']:
        msg = session_event.obj['text'].lower()
        if msg == u'ты живой?':
            API.write_msg(session_event, u'ПНХ')
        elif msg.find(u'запутин') >= 0 or msg.find(u'коз') >= 0:
            API.write_msg(session_event, u'МЫ ЗА ЗАПУТИНА! СЛАВА ГЕНСЕКУ! СМЕРТЬ ЕДРОСАМ!')
        elif msg.find(u'кажат') >= 0 or msg.find(u'кжч') >= 0:
            smsg = API.send_request(u'Кажат встал, кинул зигу и гордо произнес Параглоштовцам:')
            API.write_msg(session_event, smsg, picture='images/pitivo.jpg')
        else:
            pass
    if len(session_event.obj['attachments']):
        print(session_event.obj['attachments'][0])
        if session_event.obj['attachments'][0]['type'] == 'sticker' and\
                session_event.obj['attachments'][0]['sticker']['sticker_id'] == 163:
            API.write_msg(session_event, '', sticker_id=163)


def wipe_conversation_activity(peer_id):
    user_list = API.get_conversation_members(peer_id)
    print(user_list)
    for user in user_list:
        BotData.conversation_statistic['message_count'] = {user['last_name'] + ' ' + user['first_name']: 0}
    print(BotData.conversation_statistic)
    BotData.conversation_statistics[peer_id] = BotData.conversation_statistic


def user_add_msg_count(user, peer_id):
    count = BotData.conversation_statistic['message_count'][user['last_name'] + ' ' + user['first_name']]
    BotData.conversation_statistic['message_count'][user['last_name'] + ' ' + user['first_name']] = count + 1
    BotData.conversation_statistics[peer_id] = BotData.conversation_statistic


def stop_bot(event):
    API.write_msg(event, "CLOSING...")
    exit('Closed by user')
