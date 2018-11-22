from urllib import request, parse
import json


def httpPost(url, data, headers={}):
    data = json.dumps(data)
    data = data.encode()
    req = request.Request(url, data=data, headers=headers)
    resp = request.urlopen(req)
    return resp


def httpGet(url, params={}, headers={}):
    params = parse.urlencode(params)
    req = request.Request(url + "?" + params, headers=headers)
    resp = request.urlopen(req)
    return resp


def testPost():
    url = "https://www.easy-mock.com/mock/5b2b67c175a11308f6accadb/example/upload"
    data = {
        'test': 1
    }
    resp = httpPost(url, data=data)
    resp = resp.read()
    resp = json.loads(resp)
    print(resp)


def testGet():
    url = "https://www.easy-mock.com/mock/5b2b67c175a11308f6accadb/example/query"
    params = {
        'test': 1
    }
    resp = httpGet(url, params=params)
    resp = resp.read()
    resp = json.loads(resp)
    print(resp)


def main():
    testGet()
    testPost()


if __name__ == "__main__":
    main()
