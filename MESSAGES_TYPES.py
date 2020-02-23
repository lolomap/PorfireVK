# -*- coding: utf-8 -*-

import API

MSG_GENERATE = ['Прф, ', 'прф, ', 'прф,', 'Прф,', 'P ', 'p ', 'P, ', 'p, ', 'p,', 'P,']
MSG_NEXT_GENERATE = ['Прф дальше', 'прф дальше', 'p n', 'P n', 'P N']


def easter_egg_request(session, session_event):
    if session_event.obj['text']:
        msg = session_event.obj['text'].lower()
        if msg == 'ты живой?':
            API.write_msg(session, session_event, 'ПНХ')
        elif msg.find('запутина') >= 0 or msg.find('коз') >= 0:
            API.write_msg(session, session_event, 'МЫ ЗА ЗАПУТИНА! СЛАВА ГЕНСЕКУ! СМЕРТЬ ЕДРОСАМ!')
        else:
            pass
    if len(session_event.obj['attachments']):
        print(session_event.obj['attachments'][0])
        if session_event.obj['attachments'][0]['type'] == 'sticker' and\
                session_event.obj['attachments'][0]['sticker']['sticker_id'] == 163:
            API.write_msg(session, session_event, '', 163)
