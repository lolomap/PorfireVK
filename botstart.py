# -*- coding: utf-8 -*-

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import sys

import API
import MESSAGES_TYPES

group_token = sys.argv[1]
group_id = sys.argv[2]
close_pass = sys.argv[3]

lastBotMsgID = 0

lastBotMsg = {}
lastBotMsgText = ''
saveBotMsg = {}

lastCmdType = ''


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

                if msg_text == close_pass:
                    API.write_msg(vkK, event, "CLOSING...")
                    exit('Closed by user')

                MESSAGES_TYPES.easter_egg_request(vkK, event)

                process_res = API.msg_process(msg_text)

                if process_res['type'] == 'MSG_GENERATE':

                    send_text = msg_text[len(process_res['command']):]
                    API.save_last_msg(event, send_text, saveBotMsg)
                    print('MSG SEPARATED', send_text)

                    lastBotMsgText = API.send_request(send_text)
                    print('MSG REQUESTED')

                    API.save_last_msg(event, lastBotMsgText, lastBotMsg)
                    print('MSG SAVED')

                    lastBotMsgID = API.write_msg(vkK, event, lastBotMsgText)
                    print('MSG WAS WRITEN')

                    print(lastBotMsgID)
                    lastCmdType = process_res['type']
                elif process_res['type'] == 'MSG_NEXT_GENERATE':
                    print('Continue')
                    API.save_last_msg(event, lastBotMsgText, saveBotMsg)
                    lastBotMsgText = API.edit_msg(vkK, event, lastBotMsgID, lastBotMsg)
                    API.save_last_msg(event, lastBotMsgText, lastBotMsg)
                    lastCmdType = process_res['type']
                elif process_res['type'] == 'MSG_CHANGE':
                    lastBotMsgText = API.edit_msg(vkK, event, lastBotMsgID, saveBotMsg)
                    API.save_last_msg(event, lastBotMsgText, lastBotMsg)
                    lastCmdType = process_res['type']
    except Exception as e:
        print(e)
