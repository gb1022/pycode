# -*- coding: utf-8 -*-
import sys
import urllib2
import json



url = "http://192.168.1.32/xianmu/Index/report/plug_log"
headers = {}
headers['Content-Type'] = 'application/json; charset=utf-8'

def read_file(path):
    # data = {"date": "", "teamId": "", "zoneId": "", "num": -1}
    file_object = open(path,'r')
    if file_object == None:
        print "file_object is None"
        return None
    lines = file_object.readlines()
    if lines == None or 0 == len(lines):
        print "lines is None"
        return None
    data_list = []
    for line in lines:
        data ={}
        n = line.count("怀疑加速")
        if n == 1:
            datas = line.split("]")
            # print "datas:", datas
            date = datas[0][10:-5]
            others = datas[2].split("-")
            teamId = others[0][13:]
            zoneId = others[1]
            if 0 == others[2].count(","):
                num = int(others[2][:-2])
            else:
                num = int(others[2][:-4])
            data["date"] = date
            data["teamId"] = teamId
            if zoneId == '0':
                continue
            data["zoneId"] = zoneId
            data["num"] = num
            # print data
            data_list.append(data)
    return data_list


def post_data(data_list):
    if data_list == None:
        print "data_list is None"
        return
    jdata = json.dumps(data_list)
    req = urllib2.Request(url=url, headers=headers,data=jdata)
    try:
        response = urllib2.urlopen(req)
        print "response:%s"% response.read()
        response.close()
    except urllib2.HTTPError,e:
        print e.code
        print e.read()

class test:
    a= 1
    b= 2



if __name__ == "__main__":
    # arg = sys.argv[1]
    # path = "%s"%arg
    path = u"worldlog.txt"
    print path
    data_list = read_file(path)
    print data_list
    # a = 123
    # b = str(a)
    # c = u'1234'
    # d = b+c
    # print d
    # print type(c)
    # bb = test()
    # s = getattr(bb,"a")
    # print s
    # print type(s)
    # from urllib import urlopen
    # req = urllib2.Request("http://www.baidu.com")
    # doc = urlopen(req).read()
    # print doc


    # post_data(data_list)
