#!/usr/bin/python
# -*-coding:utf-8-*-
#!/usr/bin/env python
#coding=utf-8

import sys
import os
import time
import MySQLdb
import shutil
# from enum import Enum, unique

reload(sys)
sys.setdefaultencoding('utf8')

VN_SnapshotReFields = ['dLogTime', 'vAccountName', 'vRoleID', 'iServerID', 'iTopupCoinEnd', 'iCouponEnd']
VN_SnapshotFields = ['ts',          'account',       'team_id', 'zone',       'diamond',        'coupons']

ZONE = 1  #如果区服不同 ，这里一定要改！！！！！！
DBINFO={"charset":"utf8","host":"192.168.1.229", "user":"basketball", "passwd":'qvMxQRRfn5Wx', "db":"basketball_record_%s" % (ZONE)}
VN_LOGS_LOCAL_DIR = "/data/game/vnlog/"

# MAXSIZE = 2*1024*1024






class DB(object):
    """docstring for DB"""
    def __init__(self):
        super(DB, self).__init__()
        # self.zone = zone
        self.__gameconn = None#MySQLdb.connect(**DBCONF[zone])
        #self.__localConn =None # MySQLdb.connect(**DBLOCAL)

    def initDB(self):
        self.__gameconn = MySQLdb.connect(**DBINFO)
        #self.__localConn = MySQLdb.connect(**DBLOCAL)

    @property
    def gameConn(self):
        return self.__gameconn

class YnResourceData(object):
    def __init__(self):
        self.db = DB()
        self.data = {}
    def getData(self,zone=ZONE):
        self.db.initDB()
        conn = self.db.gameConn
        cursor = conn.cursor()
        n = cursor.execute("show tables")
        print n
        tables = []
        for t in cursor.fetchall():
            print t[0]
            if t[0].find("Resource") == -1:
                continue
            tables.append(t[0])
        rows = {}
        for t in tables:
            n = cursor.execute("select reason from %s"%t)
            for r in cursor.fetchall():
                if r[0] not in rows:
                    print "reason:",r[0]
                    rows[r[0]]=r
                else:
                    continue

        # for i in range(10,50):
        #
        #     n = cursor.execute("SELECT * from Resource_2018%s limit 5" % i)
    # def writeFile(self,datas,filename):
    #     with open(filename, "a") as this_file:
    #         for data in datas:
    #             s = str(data[0])
    #             this_file.write(s)





if __name__ == "__main__":
    # info = {}
    # result = platformVerify_yn(info)
    # ss = json.loads(result)
    # print "%s" % result
    # print result['returnCode'],result['message']

    resource = YnResourceData()
    datas = resource.getData()
    resource.writeFile(datas,"sqldata")