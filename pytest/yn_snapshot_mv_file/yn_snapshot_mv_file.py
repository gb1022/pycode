#!/usr/bin/env python
#coding=utf-8

import sys
import os
import time
import MySQLdb
import shutil
from enum import Enum, unique

reload(sys)
sys.setdefaultencoding('utf8')

VN_SnapshotReFields = ['dLogTime', 'vAccountName', 'vRoleID', 'iServerID', 'iTopupCoinEnd', 'iCouponEnd']
VN_SnapshotFields = ['ts',          'account',       'team_id', 'zone',       'diamond',        'coupons']

ZONE = 2  #如果区服不同 ，这里一定要改！！！！！！
DBINFO={"charset":"utf8","host":"192.168.1.229", "user":"basketball", "passwd":'qvMxQRRfn5Wx', "db":"basketball_%s" % (ZONE)}
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

class DBInfo(object):
    def __init__(self):
        self.db = DB()
        self.data = {}

    def getData(self,zone):

        yfct = int(time.time()) - 60 * 60 * 24
        day = time.strftime("%Y%m%d", time.localtime(yfct))
        self.db.initDB()
        conn = self.db.gameConn
        # begin = self.db.begin
        # end = self.db.end
        cursor = conn.cursor()
        n = cursor.execute("SELECT * from appbasketball_team limit 5")
        print("record_login_user_data is begin ! zone:%s,day:%s\n"% (zone, day))
        try:
            # filename = VN_LOGS_LOCAL_DIR + "snapshot_" + day + ".log"
            # if os.path.exists(filename):
            #     print("the snapshot is exists!filename:%s\n" % filename)
            #     return
            limit = 500
            teamid = None
            ctime_str = day + " 00:00:00"
            ytime = time.mktime(time.strptime(ctime_str, "%Y%m%d %H:%M:%S"))
            lines = ""
            while True:
                if teamid:
                    sql_qq = "SELECT uuid,account,zone,diamond,coupons,loginTime FROM basketball_%s.appbasketball_team WHERE uuid > '%s' LIMIT %s" % (ZONE,teamid, limit)
                else:
                    sql_qq = "SELECT uuid,account,zone,diamond,coupons,loginTime FROM basketball_%s.appbasketball_team LIMIT %s" % (ZONE,limit)
                print("sql_qq:%s" % sql_qq)
                # print("111111111111111111111\n")
                n = cursor.execute(sql_qq)
                if n == 0:
                    print("n is 0")
                    continue
                # print("22222222222222222222222222222222222\n")
                load_row = 0
                # print("666666666666666666666666666\n")
                for t in cursor.fetchall():
                    # print("77777777777777777777777777777777\n")
                    load_row += 1
                    # print("555555555555555555555555555555555555555555,t:\n" , t)
                    if (int(t[5]) - int(ytime)) > 60 * 60 * 24 or (int(ytime) - int(t[5])) > 0:  # 不是昨天登陆的 就不计入统计
                        print("---------t:" ,t)
                        continue
                    data = {'ts': int(time.time()), 'account': t[1], 'team_id': t[0], 'zone': int(t[2]),
                            'diamond': t[3], 'coupons': t[4]}
                    print("---------data:%s" % data)
                    # print("333333333333333333333333333333333333\n")


                    line = get_fields_line(VN_SnapshotReFields, VN_SnapshotFields, data)
                    if len(line) == 0:
                        print("record_login_user_data,line is none!\n")
                        continue
                    lines = lines + line
                    teamid = t[0]
                # print("444444444444444444444444444444444444444444\n")
                write_log_file('snapshot', day, lines)
                if load_row < limit:
                    break
            print("record_login_user_data is success ! zone:%s,day:%s\n"% ( zone, day))
            nday = time.strftime("%Y%m%d", time.localtime(time.time()))
            # print("111111111111111111111\n")
            self.mv_vnlogfile_to_backpath(zone, nday)
            # print("2222222222222222222222\n")
        except Exception, e:
            print("record_login_user_data error:%s\n" % e)

    def mv_vnlogfile_to_backpath(self,zone, day):
        '''移动前一天的文件到backup文件夹'''
        print("mv files to backup dir then time is out !\n")
        files = os.listdir(VN_LOGS_LOCAL_DIR)
        # print("33333333333333333333333333333\n")
        backup_dir = VN_LOGS_LOCAL_DIR + "backup/" + str(zone)
        # print("444444444444444444444444444\n")
        for item in files:
            # print("55555555555555555555555555555555\n")
            fname = os.path.join(VN_LOGS_LOCAL_DIR, item)
            # print("6666666666666666666666666666666\n")
            if os.path.isfile(fname):
                infos = fname.split('.')[0]
                filetime = infos.split("_")[1]
                if day != filetime:
                    f_path = backup_dir + "/" + filetime
                    if not os.path.isdir(f_path):
                        os.makedirs(f_path)
                    back_name = os.path.join(f_path, os.path.basename(fname))
                    shutil.move(fname, back_name)
        print("mv files success!!!\n")

@unique
class FieldType(Enum):
    Unknown = 0
    Integer = 1
    String = 2
    DateTime = 3


# merge two dict into one dict
def merge_msg(msg_l, msg_r):
    context = msg_l.copy()
    context.update(msg_r)
    return context


def get_field_typ(fieldname):
    if len(fieldname) == 0:
        return FieldType.Unknown
    if fieldname[0] == 'i':
        return FieldType.Integer
    if fieldname[0] == 'v':
        return FieldType.String
    if fieldname[0] == 'd':
        return FieldType.DateTime
    return FieldType.Unknown


def get_one_null_field(typ, field_name):
    if field_name == 'iResult':
        str = '%d' % 0
        return str

    if typ == FieldType.Integer:
        str = '%d' % 0
    else:
        str = '%s' % 'null'
    return str


def get_one_field(field, msg, typ):
    str1 = ""
    # print("get_one_field,field:%s,msg:%s,typ:%s\n" % (field,msg,typ))
    try:
        if typ == FieldType.Integer:
            str1 = str(msg.get(field, 0))
        elif typ == FieldType.String:
            str1 = str(msg.get(field, 'null'))
        elif typ == FieldType.DateTime:
            str1 = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg.get(field, "0"))))
        else:
            str1 = 'null'
        return str1
    except Exception, e:
        print("get_one_field error:%s\n" % (e))
        return str1

def get_fields_line(ref_list, local_list, msg):
    line = ""
    if len(msg)==0 or msg == None:
        return line
    if len(ref_list) != len(local_list):
        return line
    for index, item in enumerate(ref_list):
        typ = get_field_typ(item)
        field = local_list[index]
        # print ("refField:%s localField:%s\n" % (item, field))
        if field == 'null':
            str = '%s\t' % get_one_null_field(typ, item)
            line += str
        else:
            str = '%s\t' % get_one_field(field, msg, typ)
            line += str

    if len(line) > 0:
        line = line[0:len(line) - 1]
    line += '\n'
    return line

def write_log_file(prefix, day, data):
    log_name = '%s%s_%s.log' % (VN_LOGS_LOCAL_DIR, prefix, day)
    with open(log_name, "a") as this_file:
        this_file.write(data)
    # print("write snapshot log file success!")



if __name__ == '__main__':
    db_info = DBInfo()
    db_info.getData(ZONE)

