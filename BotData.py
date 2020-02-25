#!/usr/bin/python
# -*- coding: utf-8 -*-
group_token = None
group_id = None
close_pass = None

session = None
longpoll = None

lastBotMsgID = 0

lastBotMsg = {}
lastBotMsgText = ''
saveBotMsg = {}

lastCmdType = ''

conversation_statistics = {}
conversation_statistic = {'message_count': {}}

peer_list = []
