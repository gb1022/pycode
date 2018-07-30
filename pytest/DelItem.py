# -*- coding: utf-8 -*-

import sys
import os
import time
import MySQLdb


reload(sys)
sys.setdefaultencoding('utf8')

ZONE = 1  #如果区服不同 ，这里一定要改！！！！！！
DBINFO={"charset":"utf8","host":"192.168.1.229", "user":"basketball", "passwd":'qvMxQRRfn5Wx', "db":"basketball_%s" % (ZONE)}
RECORDDBINFO={"charset":"utf8","host":"192.168.1.229", "user":"basketball", "passwd":'qvMxQRRfn5Wx', "db":"basketball_record_%s" % (ZONE)}

FILEPATH = "/data/game/resource_data/data.txt"
TEAMID = "7f1ec29a064d11e7942d525400954cac"
# MAXSIZE = 2*1024*1024






class DB(object):
    """docstring for DB"""
    def __init__(self):
        super(DB, self).__init__()
        # self.zone = zone
        self.__gameconn = None#MySQLdb.connect(**DBCONF[zone])
        #self.__localConn =None # MySQLdb.connect(**DBLOCAL)

    def initDB(self):
        self.__gameconn = MySQLdb.connect(**RECORDDBINFO)
        #self.__localConn = MySQLdb.connect(**DBLOCAL)

    @property
    def gameConn(self):
        return self.__gameconn

class DBInfo(object):
    def __init__(self):
        self.db = DB()
        self.data = {}

    def getData(self,zone):
        self.db.initDB()
        conn = self.db.gameConn
        cursor = conn.cursor()
        n = cursor.execute("show tables")

        try:
            tables = []
            for t in cursor.fetchall():
                table = str(t[0])
                if table.find("Resource_") < 0:
                    continue
                tables.append(table)
            print tables
            lines = ""
            for table in tables:
                sqlcmd = "select * from %s where teamId = '%s' and reason = '购买球员'" % (table,TEAMID)
                print "sql:",sqlcmd
                n = cursor.execute(sqlcmd)
                for l in cursor.fetchall():
                    line = "%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s\n"%(l[0],l[1],l[2],l[3],l[4],l[5],l[6],l[7],l[8],l[9],l[10],l[11],l[12],l[13],l[14])
                    lines += line
            print lines
            self.write_file(FILEPATH,lines)
        except Exception, e:
            print("getData error:%s\n" % e)


    def write_file(self,path,lines):
        with open(path, "a") as this_file:
            this_file.write(lines)
        print "write file ok,path:",path














if __name__ == "__main__":
    db_info = DBInfo()
    db_info.getData(ZONE)