# -*- coding: utf-8 -*-
# FTP操作
import ftplib
import os
host = '192.168.1.221'
username = 'lmd'
password = '123456'


f = ftplib.FTP(host)  # 实例化FTP对象
f.login(username, password)  # 登录

# 获取当前路径
pwd_path = f.pwd()
print("FTP file path:", pwd_path)

# 逐行读取ftp文本文件
def getfiles(path):

    str_path = str(path)
    print ("path:",str_path)
    files = os.listdir(str_path)
    print files
    return files



def ftp_upload():
    '''以二进制形式上传文件'''
    file_remote = 'ftp_upload.txt'
    file_local = 'D:\\test_data\\ftp_upload.txt'
    bufsize = 1024  # 设置缓冲器大小
    fp = open(file_local, 'rb')
    f.storbinary('STOR ' + file_remote, fp, bufsize)
    fp.close()

path = 'E:\\pytest2'
getfiles(path)
f.quit()