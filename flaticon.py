# -*- coding: utf-8 -*-
import re
import requests
import os.path
import sys

def getHtml(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3018.3 Safari/537.36', 'Accept-Encoding': 'gzip, deflate, br'}
    html = requests.get(url = url,headers = headers).content
    return html

def getImg(html):
    #reg = r'https://image.flaticon.com[\S]*png'
    reg = r'<img.*?src="(.+)".*?>'
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    for key, val in enumerate(imglist):
        if(val.find('image.flaticon.com') >= 0):
            name = ''
            if(val.find('alt') >= 0):
                name = val.split('alt')[1].split('"')[1]
            elif(val.find('title') >= 0):
                name = val.split('title')[1].split('"')[1]
            path_info = val.split('"')[0].split('/')
            filename =  path_info[len(path_info) - 2] + '_' +  path_info[len(path_info) - 1].split('.')[0] + '_' + name + ".svg"
            img_url = "https://image.flaticon.com/icons/svg/"+ path_info[len(path_info) - 2] + "/" + path_info[len(path_info) - 1].split('.')[0] +".svg"
            print("download {0}... ...".format(key))
            try:
                req=requests.get(url = img_url)
            except:
                print("error")
            imagename=os.path.join('pic',filename)
            with open(imagename,'wb') as fp:
                fp.write(req.content)
            #print(img_url)

if __name__ == '__main__' :
    first = int(sys.argv[1])
    last = int(sys.argv[2])
    for i in range (first, last + 1 ):
        pages = str(i)
        url = "https://www.flaticon.com/categories/art-and-design/" + pages
        print('download page ' + pages + ' start')
        html = getHtml(url)
        print("\n")
        getImg(html)
