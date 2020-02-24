# -*- coding: utf-8 -*-
import sys

from Bot import BotData
from Bot import BotAPI

BotData.group_token = sys.argv[1]
BotData.group_id = sys.argv[2]
BotData.close_pass = sys.argv[3]

wiped = False

while True:
    try:
        BotAPI.connect_vk()
        print('Connected')

        msg_text = ''
        send_text = ''
        for event in BotData.longpoll.listen():
            if BotAPI.check_event_type(event, 'MESSAGE_NEW'):
                event_info = BotAPI.get_event_info(event)
                msg_text = event_info['text']
                user = event_info['user']
                peer_id = event_info['peer']

                try:
                    if not wiped:
                        BotAPI.wipe_conversation_activity(peer_id)
                        wiped = True

                    BotAPI.user_add_msg_count(user, peer_id)
                except:
                    pass

                if msg_text == BotData.close_pass:
                    BotAPI.stop_bot(event)

                BotAPI.easter_egg_request(event)

                process_res = BotAPI.msg_process(msg_text)

                if process_res['type'] == 'MSG_GENERATE':
                    BotAPI.generate(msg_text, process_res['command'], event)
                elif process_res['type'] == 'MSG_NEXT_GENERATE':
                    BotAPI.next_generate(event)
                elif process_res['type'] == 'MSG_CHANGE':
                    BotAPI.next_generate(event)
                elif process_res['type'] == 'MSG_GET_ACTION':
                    break
                else:
                    BotAPI.witless_generate(msg_text, event)
    except Exception as e:
        print(e)
