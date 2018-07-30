# -*- coding: utf-8 -*-
import time



def fun1(func):
    print "1111111111111"
    func
    return func


@fun1
def fun2():
    print "222222222222222"

import re

def fun3():
    for line in open("123.txt"):
        print line
        temp = re.match("abc",line)
        if temp is None:
            print "--------------------------"
            continue
        print "temp type is ",type(temp)
        last = temp.span()
        print last
        print "--------------------------"


def getProgram():
    """查找program name"""
    keys=[]
    for line in open("supervisor.ini"):
        has=re.match("\[program:", line)
        print has
        if has is None:
            print "-----------------"
            continue
        last=has.span()
        print last
        print type(last)
        if last is not None:
            items=line.split(':')
            print "items = ",items
            if len(items)==2:
                strvalue=items[1]
                strnew=strvalue.strip()[0:-1]
                keys.append(strnew)
        print "-----------------"
    print keys
    return keys


import os
import signal
from time import sleep

#
# def onsignal_term(signum, b):
#     print '收到信号,signum: ',signum



#
#
# def onsignal_usr1(a, b):
#     print '收到SIGUSR1信号'
#
# def fun3(**args):
#     print "args:",args
#


def senddata():
    url = "http://192.168.1.221:9999/"
    url2 = "http://192.168.1.221/login"

    req_dict = {'userid': '111222333'}


    import urllib
    req_encode = urllib.urlencode(req_dict)
    req_post = req_encode.encode('utf-8')
    print(req_post)

    headers = {}
    import urllib
    req = urllib.request.Request(url=url, headers=headers, data=req_post)
    res = urllib.request.urlopen(req)
    res = res.read().decode('utf-8')
    print res

def usefor():
    fordata = {'1': {'ac': u'2345', 'u': '714a35f0d5a011e7b07c00155d01e205', 'n': u'PhongT', 'p': u'pc', 'le': 45, 'ct': '2017, 11, 30, 15, 31, 13, 28318', 'lt': 1512530646.40325, 'z': 1, 'pay': 125.0}}
    for item in fordata:
        print item
        print fordata[item]




# int8转换uint8
def uint8(num):
    from ctypes import c_uint8
    return c_uint8(num).value

# 畅游签名算法
def create_cyou_sign(param):
    import hashlib
    sign_md5 = hashlib.md5()
    sign_md5.update(param)
    info = sign_md5.digest()
    result = ""
    for c in info:
        x = ord(c) & 0xFF
        h = uint8(x) >> 4
        l = x & 0x0F
        c1 = h + (48 if h < 10 else 87)
        c2 = l + (48 if l < 10 else 87)
        result += (chr(c1) + chr(c2))
    return result[8:24]

# 搜狐畅游韩国
CYOU_APP_KEY = "1485156165996"
CYOU_SECRET_KEY = "b391db5089c640188dcb593b127ced68"
CYOU_BILLING_DOMAIN = "https://sdk.gaming.com"  # 正式环境
# CYOU_BILLING_DOMAIN = "https://tsdk.gaming.com"  # 测试环境
CYOU_BILLING_URL_ACCOUNT = "/account-api/cyou/user/token.json"
CYOU_BILLING_URL_ORDERVERIFY = "/billing/cyou/gameserver/orderVerify.json"
CYOU_BILLING_URL_ORDERCOMPLETE = "/billing/cyou/gameserver/orderComplet.json"
CYOU_LOGS_DIR = "/home/mrdTomcat/game/cylog/"

from tornado.escape import json_encode, json_decode
from tornado import web, gen, httpclient
def platformVerify_cyou_korea(token, channel_id):
    data = {"token": token}
    http_body = json_encode(data)
    print http_body
    sign = create_cyou_sign(CYOU_APP_KEY + CYOU_SECRET_KEY + http_body)
    print sign
    http_header = {
        "Content-type": "application/json",
        "app_key": CYOU_APP_KEY,
        "channel_id": channel_id,
        "tag": "123456",
        "sign": sign
    }
    http_client = httpclient.AsyncHTTPClient()
    login_url = CYOU_BILLING_DOMAIN + CYOU_BILLING_URL_ACCOUNT
    response = None
    try:
        response = http_client.fetch(login_url, method="POST", headers=http_header, body=http_body)
        print('login result:%s'% response.body)
    except Exception, e:
        print("platformVerify_cyou_korea error: %s"% e)
        http_client.close()
        return None
    http_client.close()

    # import urllib2
    # import urllib
    # req_encode = urllib.urlencode(http_body)
    # req_post = req_encode.encode('utf-8')
    # print(req_post)
    # req = urllib2.Request(url=login_url, headers=http_header, data=req_post)
    # res = urllib2.urlopen(req)
    # res = res.read().decode('utf-8')
    # print res

    return response.body

import socket

def checkIp():
    hostname = socket.gethostname()
    ip = socket.gethostbyname_ex(hostname)
    print ip




if __name__ == "__main__":
    # fun2
    # t = time.time()
    # nt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(1500689746)))
    # print t
    # print str(nt)
    # str = "abc___aaaaaaaa"
    # fun3()
    # getProgram()
    # 这里是绑定信号处理函数，将SIGTERM绑定在函数onsignal_term上面
    # signal.signal(signal.SIGTERM, onsignal_term)
    # 这里是绑定信号处理函数，将SIGUSR1绑定在函数onsignal_usr1上面
    # signal.signal(signal.SIGINT, onsignal_usr1)
    # while 1:
    #     print '我的进程id是', os.getpid()
    #     sleep(10)
    # REDIS = {
    #     'host': '127.0.0.1',
    #     'port': 6379,
    #     'db': 7
    # }
    # fun3(**REDIS)
    senddata()
    # usefor()
    # token = "5f8d656b4f024fbea12db40ad5058323992f32d8ab2f07ed95eab2c4a009e3ee8c6e16575c01d880872bcf15abdcbc85fad3d3db622bf3a1bc96f21d6b91b1528d19062eca520851f99061185d4c2b8d9e2e42f45fe4d523"
    # channel_id = "5001"
    # platformVerify_cyou_korea(token, channel_id)
    # checkIp()



