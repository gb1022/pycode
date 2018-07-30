# -*- coding: utf-8 -*-

import urllib2
# import cookielib
# import socket
# from bs4 import BeautifulSoup
import re
import os

class RootReptile:
    def __init__(self,url):
        self.url = url

    def getRootWeb(self,page_num):
        url = self.url + str(page_num)
        print url
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        # print response.read()
        return response.read()

    def getCountNum(self):
        web = self.getRootWeb(1)
        pattern = re.compile('<span class="red_text">(.*?)</span>',re.S)
        result = re.search(pattern,web)
        if result:
            return result.group(1).strip()
        else:
            return None

    def getTitleAndUrl(self,page):
        web = self.getRootWeb(page)
        pattern = re.compile('<a rel="noreferrer"  href="/p/(.*?)" title="(.*?)" target="_blank" class="j_th_tit ">',re.S)
        result = re.findall(pattern,web)
        if result:
            return result
        else:
            return None





class reptile:
    def __init__(self,url,title):
        self.url = url
        self.response = ""
        self.title = title


    def getweb(self,pageNum):
        page = pageNum
        url = self.url + str(page)
        # print "=======:",url
        user_agent = 'Mozilla/4.0(compatible; MSIE 5.5;Windows NT)'
        headers = {'User-Agent' : user_agent}
        request = urllib2.Request(url, headers = headers)
        response = urllib2.urlopen(request)
        # print response.read()
        return response



    def getTitile(self):
        page = self.getweb(1)
        pattern = re.compile('<meta name="keywords" content="(.*?)"/>',re.S)
        pp = re.compile('<script>(.*?)</script>',re.S)
        result = re.search(pattern,page.read())
        if result:
            print result.group(1).strip()
            return result.group(1).strip()
        else:
            print "aaaa"
            return None

    def getPageNum(self):
        web = self.getweb(1)
        pattern_tie = re.compile('<li class="l_reply_num" style="margin-left:8px" ><span class="red" style="margin-right:3px">(.*?)</span>回复贴，共<span class="red">(.*?)</span>页</li>',re.S)
        result_tie = re.findall(pattern_tie,web.read())
        tie = []
        if result_tie:
            # print result_tie
            tie = result_tie[0]
            # print tie
            num = int(tie[0])
            page = int(tie[1])
            # print result_tie.group(1).strip()
            # tie = result_tie.group(1).strip()
        else:
            print "bbb"
            num = -1
            page = -1
        # pattern_page = re.compile('<span class="red">(.*?)</span>',re.S)
        # result_page = re.search(pattern_page,web.read())
        # if result_page:
        #     print result_page.group(1).strip()
        #     page = result_page.group(1).strip()
        # else:
        #     print "ccc"
        #     page = None
        return num,page

    def getContent(self,page):
        web = self.getweb(page)
        pattern_con = re.compile('<div id="post_content_.*?>(.*?)</div>',re.S)
        result_con = re.findall(pattern_con,web.read())
        if result_con:
            # print result_con
            return result_con
        else:
            print "ddddd"
            return []

    def getImg(self,page):
        web = self.getweb(page)
        pattern = re.compile('class="BDE_Image".*?src="(.*?)"',re.S)
        result = re.findall(pattern,web.read())
        img = []
        if result:
            # print result
            for item in result:
                img.append(item)
        else:
            print "fffff"
        return img

    def saveImg(self,img_url,img_name):
        try:
            request = urllib2.Request(img_url)
            response = urllib2.urlopen(request)
            data = response.read()
            f = open(img_name,'wb')
            f.write(data)
            print 'img:',img_name
            f.close()
        except Exception,e:
            print "error:",e
    def saveContent(self,title,contents,filepath):
        try:
            f = open(filepath + "contents.txt",'w')
            num = 1
            title_ = "TITLE: "+title +"\n" + "============================================================\n"+"\n"+"Content:\n"
            f.write(title_)
            for content in contents:
                floor = "floor:" + str(num) + "\n"
                content =  content + "\n" + "******************************************************\n"
                # print floor
                f.write(floor)
                # print content
                f.write(content)
                num += 1
            f.close()
            print "contents.txt"
        except Exception,e:
            print "error:",e

    def Process(self,path):
        imgs = []
        title = self.title
        num,page = self.getPageNum()
        imgs = []
        contents = []
        if num == -1 or page == -1:
            print "no num or no page!"
        elif page >100:
            print "page number is too many!"
            return
        else:
            for i in range(1,page):
                img = rep.getImg(i)
                content = rep.getContent(i)
                imgs += img
                contents += content
        self.saveContent(title,contents, path)
        if len(imgs)>500:
            print "imgs number is too many!"
            return
        for i in range(0, len(imgs)-1):
            a = str(i).replace("?","_")
            img_name = a +".jpg"
            img_path = path + img_name
            rep.saveImg(imgs[i],img_path)





if __name__ == "__main__":
    url = 'https://tieba.baidu.com/'
    path = "E:\\pytest\\reptile_file\\"
    url2 = "https://tieba.baidu.com/p/5434086744?pn="
    url_root = "https://tieba.baidu.com/f?kw=%E7%BE%8E%E5%A5%B3&fr=index?pn="
    r_rep = RootReptile(url_root)
    page = 0
    while (page <= 10):
        result = r_rep.getTitleAndUrl(page)
        if not result:
            break
        for item,title in result:
            print "=-=-=-=-=-=-" , item, title
            a = str(item).replace("?", "_")
            son_url = url + "p/"+a+"?pn="
            filepath = path + str(item) +"\\"
            command = "mkdir " + filepath
            os.popen(command)
            rep = reptile(son_url,title)
            rep.Process(filepath)
        page += 50














