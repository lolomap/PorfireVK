import requests
import json


def write_msg(session, session_event, text, sticker_id=None):
    if sticker_id is None:
        bot_msg = session.messages.send(
            peer_id=session_event.obj['peer_id'],
            random_id=session_event.obj['random_id'],
            message=text
        )
    else:
        bot_msg = session.messages.send(
            peer_id=session_event.obj['peer_id'],
            random_id=session_event.obj['random_id'],
            sticker_id=sticker_id
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

