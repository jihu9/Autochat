# coding: utf-8
# !/bin/user/python
# Author:physics

import requests
import re
import pyqrcode
import base64
import time


def getShadow():
    url = 'https://github.com/Alvin9999/new-pac/wiki/ss免费账号'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) \
        AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/45.0.2454.101 Safari/537.36'}
    html = requests.get(url, headers=headers)
    lst = re.findall(r'<p>服务器.*?：(.*?)</p>', html.text)
    shadows_lst = []
    for i in lst:
        dic = {
            'method': i.split('加密方式：')[-1].split(' ')[0].split('（')[0],
            'password': i.split('密码：')[-1].split(' ')[0],
            'hostname': i.split(' ')[0],
            'port': i.split('端口：')[-1].split(' ')[0]
        }
        if (dic['method'] and dic['password']
                and dic['port'] and dic['hostname']):
            shadows_lst.append(dic)
    return shadows_lst


def outQR(Num=10):
    lst = getShadow()
    N = min(Num, len(lst))
    for i in range(0, N):
        ss = lst[i]['method'] + ':' + lst[i]['password'] + \
            '@' + lst[i]['hostname'] + ':' + lst[i]['port']
        s = base64.b64encode(str(ss).encode('utf8')).decode('utf8')
        s = 'ss://' + s
        url = pyqrcode.create(s)
        print('正在输出第 ', i + 1, ' 张二维码！')
        url.png(time.strftime('%y-%m-%d') + '_' + str(i + 1) + '.png', scale=4)


if __name__ == '__main__':
    num = input('请输入需要的二维码数量（1-40）：')
    # print(type(num))
    try:
        # num = input('请输入需要的二维码数量（1-40）：')
        num = int(num)
        outQR(num)
        time.sleep(2)
    except Exception:
        print('输入错误，退出程序！')
        time.sleep(2)
