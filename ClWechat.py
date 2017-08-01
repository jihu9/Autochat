#!usr/bin/python
#-*-coding:utf8-*-
'''

名称：ClWechat--一个属于程序员的命令行聊天工具（Command Line Wechat）

使用前请导入itchat，pyreadline

pip instal itchat pyreadline

食用方法：
1、微信扫描commandline中生成的二维码登录
2、help 查看帮助
3、ls #最近的联系人列表
4、s 好友名称  #即（备注名）可以搜索好友信息
5、t 好友名称  #开始和对应的好友进行聊天
6、logout  #登出

目前只有这些简单的功能，注册一个tuling的api应该可以实现自动聊天回复。

欢迎小伙伴一起来python交流
WechatID：gaegle
QQ：306347485


'''
import itchat, time
import threading
import readline
import sys
from itchat.content import *

# 最近交谈
recent = set()
# UserName => NickName(RemarkName)
user_table = dict()

def get_name(info):
    if len(info['RemarkName']) == 0:
        return info['NickName']
    else:
        return info['RemarkName']

def get_cmd_args(s):
    args = s.split(' ')
    cmd = args[0]
    if len(args)>1:
        args.pop(0)
    return cmd, [ a.strip() for a in args if len(a.strip()) > 0 ]

@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    FromUserName = msg['FromUserName']
    recent.add(FromUserName)
    if FromUserName in user_table:
        name = user_table[FromUserName]
    else:
        u = itchat.search_friends(userName=FromUserName)
        user_table[u['UserName']] = get_name(u)
        name = u['RemarkName']
    print(name, '%s: %s' % (msg['Type'], msg['Text']))

itchat.auto_login(enableCmdQR=2,hotReload=True)#保持登录

# 开启记录消息
def run_itchat():
    itchat.run()

# 用另一个线程收取消息
recv_thread = threading.Thread(target=run_itchat, args=())
recv_thread.start()

me = itchat.search_friends()
user_table[me['UserName']] = '@me'

talking_to = None
promot="$ "

# cmd loop
while True:
    s = input(promot)
    s = s.strip()
    # print(s)
    if s == "":
        continue
    cmd,args = get_cmd_args(s)
    # print(args)

    if cmd=="help":
        print("Usage:")
        print("ls\tList recent users")
        print("s\tSearch User")
        print("t\tTalk to someone")
        print("logout\tLogOut")
    elif cmd == "ls" or cmd == "list": # list
        for u in recent:
            print(u,user_table[u])
    elif cmd == 's' or cmd=="search": # search
        if len(args) > 0:
            k = args[0]
            ul = itchat.search_friends(name=k)
            u = None
            # search at every possible
            if len(ul) == 0:
                ul = itchat.search_friends(wechatAccount=k)
                if len(ul)==0:
                    print("no user")
                else:
                    u = ul[0]
            else:
                u = ul[0]
            if u != None:
                print (u)
                UserName = u['UserName']
                user_table[UserName] = get_name(u)
                recent.add(UserName)
        else:
            print("Usage: s name")
    elif cmd == "t" or cmd=="talk": # talk
        if len(args) > 0:
            k = args[0]
            ul = itchat.search_friends(name=k)
            if len(ul)==0:
                print("no user")
            else:
                u = ul[0]
            talking_to = u['UserName']
            # print(user_table)
            # print(talking_to)
            promot = "> "+str(user_table[talking_to])+" $ "
            recent.add(talking_to)
        else:
            print("Usage: t @id")
    elif cmd == "logout":
        itchat.logout()
        sys.exit()
    else:
        if talking_to != None:
            itchat.send(s, toUserName=talking_to)

recv_thread.join()