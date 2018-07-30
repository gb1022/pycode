# -*- coding: utf-8 -*-


import os
import string
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
config_path = u"F:\\打包文件夹\\config.txt"



class data:
    def __init__(self):
        self.datapath = ""
        self.frontend=""
        self.zipname = ""
        self.winrarpath =""

    def init(self):
        f = open(config_path, 'r')
        config_data = f.readlines()
        print config_data
        self.datapath=string.split(config_data[0],"datapath=")[1][:-1]
        print "%s"%self.datapath
        self.frontend = string.split(config_data[1],"frontend=")[1][:-1]
        self.zipname = string.split(config_data[2],"zipname=")[1][:-1]
        self.winrarpath = string.split(config_data[3], "winrarpath=")[1][:-1]
        print self.frontend
        print self.zipname
        print self.winrarpath

    def zip(self):
        command = self.winrarpath+" a "+self.zipname+" "+self.datapath+" "+self.frontend
        print command
        f = os.popen(command)
        print f.readlines()
        print "finish!  "



if __name__ == "__main__":
    # command1 = u'f:'
    # command2 = u'cd F:\打包文件夹\越南'
    # os.popen(command1)
    # os.popen(command2)
    d = data()
    d.init()
    d.zip()


