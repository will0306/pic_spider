# -*- coding: utf-8 -*-
import re
import requests
import os
import os.path
import sys
import BeautifulSoup

def getHtml(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3018.3 Safari/537.36', 'Accept-Encoding': 'gzip, deflate, br'}
    html = ''
    try:
        html = requests.get(url = url,headers = headers).content
    except:
        print("network error")
    return html

def getImg(html, dir):
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
            try:
                print("download {0}... ...".format(key))
                req=requests.get(url = img_url)
                dirPath=sys.path[0]+'/'+dir
                if not os.path.exists(dirPath):
                    os.makedirs(dirPath)
                imagename=os.path.join(dirPath,filename)
                with open(imagename,'wb') as fp:
                    fp.write(req.content)
            except:
                print("error")
            
            #print(img_url)

if __name__ == '__main__' :
    paramLen = len(sys.argv)
    catstr = sys.argv[1]
    first = int(sys.argv[2])
    last = int(sys.argv[3])
    for i in range (first, last + 1 ):
        catstr = sys.argv[1]
        pages = str(i)
        url = "https://www.flaticon.com/categories/" +catstr+"/" + pages
        print('download page ' + pages + ' start')
        if (paramLen == 4):
         html = getHtml(url)
         print("\n")
         getImg(html,catstr)
        elif (paramLen == 5):
          colorType=int(sys.argv[4])
          if(colorType==1):
            url="https://www.flaticon.com/categories/" +catstr+"/" + pages+'?color=1'
            catstr=catstr+'-singleColor'
          else:
            url="https://www.flaticon.com/categories/" +catstr+"/" + pages+'?color=2'
            catstr=catstr+'-multiColor'
        html = getHtml(url)
        print("\n")
        if(len(html) > 0):
            getImg(html,catstr)
