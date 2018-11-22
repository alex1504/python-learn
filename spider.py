# 抓取必应每日壁纸
import urllib.request
import re
import random
import time
import math
import os

pool = []
host = "https://cn.bing.com"

def getUrl(idx):
    url = "https://cn.bing.com/HPImageArchive.aspx?idx=%d&n=1" % (idx)
    return url


def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    return html.decode('utf-8')


def getSrc(html):
    reg = r"<url>(\S+)</url>"
    srcReg = re.compile(reg)
    imgPath = srcReg.findall(html)[0]
    src = host + imgPath
    return src

def getRandom():
    return str(math.floor(time.time())) + '-' + str(random.randint(0, 1000000))


def downloadImg(src):
    random = getRandom()
    dist = 'images'
    filename = dist + '/%s.jpg' % random
    if not os.path.exists(dist):
        os.mkdir(dist)
    urllib.request.urlretrieve(src, filename)

def getTodayImg(idx = 0):
    url = getUrl(idx)
    html = getHtml(url)
    src = getSrc(html)
    downloadImg(src)
    pool.append(src)
    print("抓取今日壁纸成功")

def getImg(idx=0):
    url = getUrl(idx)
    html = getHtml(url)
    src = getSrc(html)
    
    if(src in pool):
        print("已抓取过，终止抓取")
        return 

    downloadImg(src)
    pool.append(src)
    print("抓取第%d张图成功"%len(pool))
    idx += 1
    getImg(idx)

def main():
    getTodayImg()

if __name__ == "__main__":
    main()
