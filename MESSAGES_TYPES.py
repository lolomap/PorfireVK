# -*- coding: utf-8 -*-

import API

MSG_GENERATE = [u'Прф, ', u'прф, ', u'прф,', u'Прф,', u'P, ', u'p, ', u'p,', u'P,']
MSG_NEXT_GENERATE = [u'Прф дальше', u'прф дальше', u'p n', u'P n', u'P N']


def easter_egg_request(session, session_event):
    if session_event.obj['text']:
        msg = session_event.obj['text'].lower()
        if msg == u'ты живой?':
            API.write_msg(session, session_event, u'ПНХ')
        elif msg.find(u'запутина') >= 0 or msg.find(u'коз') >= 0:
            API.write_msg(session, session_event, u'МЫ ЗА ЗАПУТИНА! СЛАВА ГЕНСЕКУ! СМЕРТЬ ЕДРОСАМ!')
        else:
            pass
    if len(session_event.obj['attachments']):
        print(session_event.obj['attachments'][0])
        if session_event.obj['attachments'][0]['type'] == 'sticker' and\
                session_event.obj['attachments'][0]['sticker']['sticker_id'] == 163:
            API.write_msg(session, session_event, '', 163)
