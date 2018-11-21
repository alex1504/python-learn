# 抓取必应每日壁纸
import urllib.request
import re
import random
import time
import math
import os
from http import cookiejar
import json
import binascii
import base64

import rsa
import requests


pool = []
host = "https://cn.bing.com"
cookie_file = 'cookie.txt'


def pre_login():
    pre_login_url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=MTUyNTUxMjY3OTY%3D&rsakt=mod&checkpin=1&client=ssologin.js%28v1.4.18%29&_=1458836718537'
    pre_response = requests.get(pre_login_url).text
    pre_content_regex = r'\((.*?)\)'
    patten = re.search(pre_content_regex, pre_response)
    nonce = None
    pubkey = None
    servertime = None
    rsakv = None
    if patten.groups():
        pre_content = patten.group(1)
        pre_result = json.loads(pre_content)
        nonce = pre_result.get("nonce")
        pubkey = pre_result.get('pubkey')
        servertime = pre_result.get('servertime')
        rsakv = pre_result.get("rsakv")
    return nonce, pubkey, servertime, rsakv


def login(form_data):
    url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
    headers = (
        'User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0')
    cookie = cookiejar.MozillaCookieJar(cookie_file)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    opener.addheaders.append(headers)
    req = opener.open(url, form_data)
    redirect_result = req.read().decode('GBK')
    login_pattern = r'location.replace\(\"(.*?)\"\)'
    login_url = re.search(login_pattern, redirect_result).group(1)
    opener.open(login_url).read()
    cookie.save(cookie_file, ignore_discard=True, ignore_expires=True)


def generate_form_data(nonce, pubkey, servertime, rsakv, username, password):
    rsa_public_key = int(pubkey, 16)
    key = rsa.PublicKey(rsa_public_key, 65537)
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)
    passwd = rsa.encrypt(message.encode(), key)
    passwd = binascii.b2a_hex(passwd)
    username = urllib.parse.quote(username)
    username = base64.b64encode(username.encode())
    form_data = {
        'entry': 'weibo',
        'gateway': '1',
        'from': '',
        'savestate': '7',
        'useticket': '1',
        'pagerefer': 'http://weibo.com/p/1005052679342531/home?from=page_100505&mod=TAB&pids=plc_main',
        'vsnf': '1',
        'su': username,
        'service': 'miniblog',
        'servertime': servertime,
        'nonce': nonce,
        'pwencode': 'rsa2',
        'rsakv': rsakv,
        'sp': passwd,
        'sr': '1366*768',
        'encoding': 'UTF-8',
        'prelt': '115',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'returntype': 'META'
    }
    form_data = urllib.parse.urlencode(form_data).encode('utf-8')
    return form_data


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
    urllib.request.urlretrieve(src, 'images/%s.jpg' % random)


def getImg(idx=0):
    url = getUrl(idx)
    html = getHtml(url)
    src = getSrc(html)

    if(src in pool):
        print("已抓取过，终止抓取")
        return

    downloadImg(src)
    pool.append(src)
    print("抓取第%d张图成功" % len(pool))
    idx += 1
    getImg(idx)


def upload():
    files = os.listdir('images')
    for file in files:
        with open(file, "rb") as f:
            base64_data = base64.b64encode(f.read())


def main():
    
    username = ''
    password = ''
    try:
        if not (username and password):
            username = input("输入新浪微博用户名：")
            password = input("输入新浪微博密码：")
        nonce, pubkey, servertime, rsakv = pre_login()
        form_data = generate_form_data(
            nonce, pubkey, servertime, rsakv, username, password)
        login(form_data)

        cookie = cookiejar.MozillaCookieJar()
        cookie.load(cookie_file, ignore_expires=True, ignore_discard=True)
        opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cookie))
        serviceApi = 'http://picupload.service.weibo.com/interface/pic_upload.php?mime=image%2Fjpeg&data=base64&url=0&markpos=1&logo=&nick=0&marks=1&app=miniblog'
        
        file = os.path.join(os.getcwd(), 'images',  os.listdir('images')[0])
        with open(file, "rb") as f:
            base64_data = base64.b64encode(f.read())
            data = urllib.parse.urlencode({'b64_data': base64_data}).encode()
            result = opener.open(serviceApi, data).read().decode('gbk')
            result = re.sub(r"<meta.*</script>", "", result, flags=re.S)
            image_result = json.loads(result)
            print(image_result)
            image_id = image_result.get('data').get('pics').get('pic_1').get('pid')
            print('http://ww3.sinaimg.cn/large/%s' % image_id)

    except Exception as e:
        print(e)
        print("登录失败,程序退出")
        exit()

    # getImg()


if __name__ == "__main__":
    main()
