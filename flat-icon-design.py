# -*- coding: utf-8 -*-
import re
import os
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
    reg = r'<img.*?src="(.+)".*?>'
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3018.3 Safari/537.36', 'Accept-Encoding': 'gzip, deflate, br'}
    file_type = ['0.svg','2nbg.svg','1nbg.svg','0nbg.svg','1bg.svg','0bg.svg','2bg.svg']
    for key, val in enumerate(imglist):
        if(val.find('f/f_') >= 0):
            path_info = val.split(' ')[0].split('/')
            file_png = re.sub(r'.{1,}_f', "svg_f",path_info[len(path_info) - 1]).replace('"','')
            file_path = 'flat-icon-design/' + path_info[1]
            dir_path = os.getcwd() + '/' + file_path
            if not os.path.exists(dir_path):
                try:
                    os.makedirs(dir_path)
                except Exception, e:
                    print(e)
                    print('error ; unable to create folder')
                    continue
            print("download {0}... ...".format(key))
            for i in file_type :
                filename = file_png.replace("0bg.png", i)
                img_url = 'http://flat-icon-design.com/' + path_info[0] + "/" + path_info[1] + "/" + filename
                print(img_url)
                try:
                    req=requests.get(url = img_url,headers = headers)
                    imagename=os.path.join(file_path, filename)
                    with open(imagename,'wb') as fp:
                        fp.write(req.content)
                except Exception, e:
                    print(e)
                    continue

if __name__ == '__main__' :
    first = int(sys.argv[1])
    last = int(sys.argv[2])
    for i in range (first, last + 1 ):
        pages = str(i)
        url = "http://flat-icon-design.com/?paged=" + pages
        print('download page ' + pages + ' start')
        html = getHtml(url)
        print("\n")
        getImg(html)
