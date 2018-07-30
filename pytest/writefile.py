# -*- coding: utf-8 -*-
import sys
import json
import os



def write_log_file(data):
    log_name = "data1111.txt"
    with open(log_name, "a") as this_file:
        this_file.write(data)
    print("write snapshot log file success!")



if __name__ == '__main__':
    write_log_file("aaaaaaaaaaaaaaaa\n")
    write_log_file("bbbbbbbbbbbbbbbb\n")
    write_log_file("cccccccccccccccc\n")