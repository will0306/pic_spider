# -*- coding: utf-8 -*-
import re
import requests
import os.path
import sys

def getHtml(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3018.3 Safari/537.36', 'Accept-Encoding': 'gzip, deflate, br'}
    html = ''
    try:
        html = requests.get(url = url,headers = headers).content
    except Exception, e:
        print(e)
    return html

def getImg(html):
    #reg = r'https://image.flaticon.com[\S]*png'
    reg = r'<div.*?style="background(.+)".*?>'
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3018.3 Safari/537.36', 'Accept-Encoding': 'gzip, deflate, br'}
    for key, val in enumerate(imglist):
        filename = re.sub(r'._', "m_", val.split('(')[1].split(')')[0].replace('jpg', 'svg'))
        path_info = filename.split('/')
        img_url = 'http://bg-patterns.com/' + filename
        print("download {0}... ...".format(key))
        try:
            req=requests.get(url = img_url,headers = headers)
            imagename=os.path.join('pic2',path_info[1] + '_' + path_info[2])
            with open(imagename,'wb') as fp:
                fp.write(req.content)
        except Exception, e:
            print(e)

if __name__ == '__main__' :
    first = int(sys.argv[1])
    last = int(sys.argv[2])
    for i in range (first, last + 1 ):
        pages = str(i)
        url = "http://bg-patterns.com/?paged=" + pages
        print('download page ' + pages + ' start')
        html = getHtml(url)
        if(len(html)):
            getImg(html)
        print("\n")
