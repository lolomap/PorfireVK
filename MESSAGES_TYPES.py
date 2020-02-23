# -*- coding: utf-8 -*-

import API

MSG_GENERATE = [u'прф, ', u'прф,', u'p, ', u'p,']
MSG_NEXT_GENERATE = [u'прф дальше', u'p n']
MSG_CHANGE = [u'прф другое', 'p ch']


def easter_egg_request(session, session_event):
    if session_event.obj['text']:
        msg = session_event.obj['text'].lower()
        if msg == u'ты живой?':
            API.write_msg(session, session_event, u'ПНХ')
        elif msg.find(u'запутин') >= 0 or msg.find(u'коз') >= 0:
            API.write_msg(session, session_event, u'МЫ ЗА ЗАПУТИНА! СЛАВА ГЕНСЕКУ! СМЕРТЬ ЕДРОСАМ!')
        elif msg.find(u'кажат') >= 0 or msg.find(u'кжч') >= 0:
            smsg = API.send_request(u'Кажат встал, кинул зигу и гордо произнес Параглоштовцам:')
            API.write_msg(session, session_event, smsg, picture='images/pitivo.jpg')
        else:
            pass
    if len(session_event.obj['attachments']):
        print(session_event.obj['attachments'][0])
        if session_event.obj['attachments'][0]['type'] == 'sticker' and\
                session_event.obj['attachments'][0]['sticker']['sticker_id'] == 163:
            API.write_msg(session, session_event, '', sticker_id=163)
