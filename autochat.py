#!usr/bin/python
# tulingKey:92ba000de18c40a2a5fe9e2c8c98ee3e

import itchat
from itchat.content import *

import requests


def tuling(st):  # tuling AI callback
    key = '92ba000de18c40a2a5fe9e2c8c98ee3e'
    url = 'http://www.tuling123.com/openapi/api'

    data = {
        'key': key,
        'info': st,
        'userid': 'jihu9'
    }

    html = requests.post(url, data=data)
    return eval(html.content)['text']


# @itchat.msg_register(TEXT,isFriendChat=True)
def text_reply(msg):
    cont = tuling(msg['Text'])
    print('YOU:' + msg['Text'])
    print('ME:' + cont)
    return '%s' % cont


'''
@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO],isFriendChat=True)
def download_files(msg):
    msg['Text'](msg['FileName'])
    itchat.send('@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.\
    get(msg['Type'], 'fil'), msg['FileName']),msg['FromUserName'])
'''

Num = 0


@itchat.msg_register(TEXT, isFriendChat=True, isGroupChat=True)
def auto_reply(msg):
    print(Num)
    if msg['Text'] == 'start' or (Num == 1 and (msg['Text'] != 'over')):
        global Num
        Num = 1
        return text_reply(msg)
    elif msg['Text'] == 'over' or Num == 0:
        Num = 0
        print(Num)
        print(msg['Text'])  # new add
        pass


if __name__ == '__main__':

    itchat.auto_login(True)
    itchat.run()
