# -*- coding: utf-8 -*-


import xlrd
import xlwt
import time
import csv
import codecs


def open_excel(file= '1111.xls'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception,e:
        print str(e)


#根据索引获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_index：表的索引
def excel_table_byindex(file= '33.xlsx',colnameindex=0,by_index=0):
    data = xlrd.open_workbook(file)
    table = data.sheets()[by_index]
    nrows = table.nrows #行数
    ncols = table.ncols #列数
    colnames =  table.col_values(4) #某一行数据
    list =[]
    for rownum in range(0,nrows):
        temp = eval(colnames[rownum])
        rowvalue = table.row_values(rownum)
        if "vip" in temp:
            vip = temp["vip"]
            svip = temp["svip"]
            # nowsec = int(time.time())
            if vip == 0:
                vipday = 0
            else:
                vipday = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(vip)))
            if svip == 0:
                svipday = 0
            else:
                svipday = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(svip)))
            rowvalue.append(str(vipday))
            rowvalue.append(str(svipday))
        list.append(rowvalue)
    return list

def excel_write(list):
    workbook = xlwt.Workbook(encoding='utf-8')
    # 创建sheet
    data_sheet = workbook.add_sheet('2222')
    row0 = [ u'uuid',u'account',u'玩家名字',u'当前等级','json',u'充值金额',u'VIP天数',u'SVIP天数']


    # 生成第一行和第二行
    for i in range(len(row0)):
        data_sheet.write(0, i, row0[i])
    for j in range(len(list)):
        for x in range(len(row0)):
            if 8==len(list[j]):
                data_sheet.write(j+1,x,list[j][x])


        # 保存文件
    workbook.save('test3.xls')

#根据名称获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_name：Sheet1名称
def excel_table_byname(file= 'file.xls',colnameindex=0,by_name=u'Sheet1'):
    data = open_excel(file)
    table = data.sheet_by_name(by_name)
    nrows = table.nrows #行数
    colnames =  table.row_values(colnameindex) #某一行数据
    list =[]
    for rownum in range(1,nrows):
         row = table.row_values(rownum)
         if row:
             app = {}
             for i in range(len(colnames)):
                app[colnames[i]] = row[i]
             list.append(app)
    return list


def excel_read(file= 'item_base.xlsx'):
    data = xlrd.open_workbook(file)
    table = data.sheets()[0]
    # nrows = table.nrows #行数
    # ncols = table.ncols #列数
    rownames =  table.row_values(0) #某一行数据
    newrows=[]
    for i in range(len(rownames)):
        print "%s"%rownames[i]
        print "type:%s" % type(rownames[i])
        c = rownames[i].encode("utf-8")
        newrows.append(c)

    return newrows

def excel_write_ex(rownames):
    workbook = xlwt.Workbook(encoding='utf-8')
    data_sheet = workbook.add_sheet('2222')
    for i in range(len(rownames)):
        data_sheet.write(0, i, rownames[i])
    workbook.save('item_base.csv')

def csv_write(data):
    # 从列表写入csv文件
    csvFile2 = open('item_base2.csv', 'wb')  # 设置newline，否则两行之间会空一行
    csvFile2.write(codecs.BOM_UTF8) #解决中文乱码问题
    writer = csv.writer(csvFile2)
    m = len(data)
    # for i in range(m):
    #
    #     print data[i]
    #     c = data[i].encode("utf-8")
    writer.writerow(data)
    csvFile2.close()


if __name__ == "__main__":
    # list = excel_table_byindex()
    # excel_write(list)
    rownames = excel_read()
    # excel_write_ex(rownames)
    csv_write(rownames)

