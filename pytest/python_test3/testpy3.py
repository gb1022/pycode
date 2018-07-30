# -*- coding: utf-8 -*-
import sys
import json
import os

def read_dbfile(path):
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
    num = 0
    for line in lines:
        # if line.find("uuid") != -1:
        #     continue
        # data = line.split(",")
        # str = "%s|%s|%s" % (data[2][1:-1],data[5],data[8])
        # print str
        # id = int(data[5])
        # value = 0 - int(data[8])
        # data_list[data[2][1:-1]] = (id,value)
        uuid = line.split("|")[0]
        reward_str = line.split("|")[1]
        reward = json.loads(reward_str)
        if reward['1']['rinfos']['1']['pro'] == 1 and reward['1']['rinfos']['1']['state'] == 2:
            # print "reward:",reward
            num += 1
            data_list.append(uuid)
            # print "uuid:",uuid
    return data_list

def read_logfile(path):
    # data = {"date": "", "teamId": "", "zoneId": "", "num": -1}
    file_object = open(path,'r')
    if file_object == None:
        print "file_object is None"
        return None
    lines = file_object.readlines()
    if lines == None or 0 == len(lines):
        print "lines is None"
        return None
    # data_dict = {}
    # num = 0
    dlist = []
    # zone1 = ""
    for line in lines:
        if line.find("newVActivity") < 0 :
            continue
        # print line.split("/")[3]
        # zone2 = line.split("/")[3].split("_")[1]
        # print "zone:",zone
        uuid = line.split("uuid:")[1][0:-1]
        # if zone1 == "":
        #     zone1 = zone2
        # if zone1 != zone2:
        #     data_dict[zone1] = dlist
        #     dlist = []
        dlist.append(uuid)

        # zone1 = zone2
    print dlist
    return dlist


def listfile(ch):
    filelist = os.listdir('./')
    flist = []
    for file in filelist:
        if file.find(ch) < 0:
            continue
        flist.append(file)
    return flist

def filter_uuid(dict,list):
    newdict = {}
    for zone,us in dict.iteritems():
        newlist =[]
        for uuid in us:
            if uuid not in list:
                newlist.append(uuid)
        newdict[zone]=newlist
    return newdict

def write_file(path,newdict):
    for zone,list in newdict.iteritems():
        fpath = path+"hgnewdata"+"_"+zone+ "/"
        if not os.path.exists(fpath) == None:
            os.makedirs(fpath)
        filepath = fpath+"newdata"+".txt"
        f = open(filepath,"w")
        lines = ""
        num = 0
        for line in list:
            lines += line + "\n"
            num += 1
        print zone,":",num
        f.write(lines)



if __name__ == "__main__":
    s = "newVactivitydata"
    c = "hgamelog"
    dbfilelist = listfile(s)
    logfilelist = listfile(c)
    # print "dbfile:",dbfilelist
    # print "logfile:",logfilelist
    # dataDict = {}
    dbdict = {}
    logdatalist = []
    # path = "newVactivitydata_1036.log"
    for path in dbfilelist:
        zone = path.split("_")[1].split(".")[0]
        # print "zone:",zone
        datalist = read_dbfile(path)
        dbdict[zone] = datalist
    # dataDict['db'] = dbdict
    # print dataDict
    for path in logfilelist:
        logdatalist = read_logfile(path)
    newdatas = filter_uuid(dbdict,logdatalist)
    print "newdatas:",newdatas
    path = "./newdata/"
    write_file(path,newdatas)




