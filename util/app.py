import sys

import pymysql
from flask import Flask, request
import logging,time
import requests
from logging.handlers import RotatingFileHandler
import random
from datetime import datetime
from redis import StrictRedis
from urllib.parse import quote

from util.log_util import LoggerUtil

app = Flask('web', static_url_path='')
rs = StrictRedis(host="114.67.85.93", port=10000, db=0,password="Summer001")
cookies=str(rs.get("jd"))
cookies =cookies.replace("b'","'")
file_handler = RotatingFileHandler('web.log', 'a', 1 * 1024 * 1024, 10,encoding='utf-8')
logFormatter = logging.Formatter('%(asctime)s  %(levelname)-8s %(message)s')
file_handler.setFormatter(logFormatter)
app.logger.setLevel(logging.ERROR)
file_handler.setLevel(logging.ERROR)
app.logger.addHandler(file_handler)
def formatUrl(key,psort,lowPrice,highPrice):
    searchUrl = "https://search.jd.com/Search?keyword=%s&enc=utf-8&wq=%s&psort=%s"%(quote(key), quote(key), psort);
    if int(lowPrice) <= 0:
        if int(highPrice) > 0:
            searchUrl += "&ev=exprice_0-"+highPrice+""
    else:
        if int(highPrice) > 0:
            searchUrl += "&ev=exprice_"+lowPrice+"-"+highPrice+""
        else:
            searchUrl += "&ev=exprice_" + lowPrice + "gt"
    return searchUrl

@app.errorhandler(500)
def page_not_found(e):
    return '系统错误或您的ip地址不在允许的访问列表中!', 500
@app.errorhandler(404)
def page_not_found(e):
    return '您访问的页面不存在!', 404
@app.route('/pageoo',methods=['GET','POST'])
def pageoo():
    url,cookie = "",cookies
    if request.method == 'GET':
        url = request.args.get('url')
        if request.args.get('cookie') is not None:
            cookie = request.args.get('cookie')
    else:
        url = request.form["url"]
        if "cookie" in request.form:
            cookie = request.form['cookie']
    try:
        resp = requests.get(url, headers=randHeader(), cookies={"cookie": cookie})
        resp.encoding="utf-8"
        if resp.status_code==200:
            return resp.text
        else:
            print(resp.text)
            return ""
    except:
        return ""


@app.route('/oo',methods=['GET','POST'])
def oo():
    key,psort,lowPrice,highPrice,cookie="","","","",cookies
    if request.method == 'GET':
        key = request.args.get('key')
        psort = request.args.get('psort')
        lowPrice = request.args.get('lowPrice')
        highPrice = request.args.get('highPrice')
        if request.args.get('cookie') is not None:
            cookie = request.args.get('cookie')
    else:
        key = request.form['key']
        psort = request.form['psort']
        lowPrice = request.form['lowPrice']
        highPrice = request.form['highPrice']
        if "cookie" in request.form:
            cookie = request.form['cookie']
    url = formatUrl(key, psort, lowPrice, highPrice)
    try:
        resp = requests.get(url, headers=randHeader(), cookies={"cookie": cookie})
        if resp.status_code == 200:
            return resp.content.decode("utf-8", "ignore")
        else:
            print(resp.text)
            return ""
    except:
        return ""

@app.route('/hello',methods=['GET','POST'])
def hello():
    if request.method == 'GET':
        return "no" if request.args.get('cookie') is None else request.args.get('cookie')
    else:
        return request.form["cookie"] if "cookie" in request.form else "no"

@app.route('/xx',methods=['GET','POST'])
def xx():
    key, psort, lowPrice, highPrice,cookie = "", "", "", "",cookies
    if request.method == 'GET':
        key = request.args.get('key')
        psort = request.args.get('psort')
        lowPrice = request.args.get('lowPrice')
        highPrice = request.args.get('highPrice')
        if request.args.get('cookie') is not None:
            cookie = request.args.get('cookie')
    else:
        key = request.form['key']
        psort = request.form['psort']
        lowPrice = request.form['lowPrice']
        highPrice = request.form['highPrice']
        if "cookie" in request.form:
            cookie = request.form['cookie']
    url = formatUrl(key, psort, lowPrice, highPrice)
    loadUrl = url.replace("/Search", "/s_new.php");
    loadUrl = "%s&page=2&s=29&scrolling=y" % loadUrl
    try:
        resp = requests.get(loadUrl, headers=randHeader(url), cookies={"cookie": cookie})
        resp.encoding = "utf-8"
        content = resp.text
        if resp.status_code == 200:
            return content
        else:
            print(content)
            return ""
    except:
        return ""

@app.route('/pagexx', methods=['GET', 'POST'])
def pagexx():
    loadUrl, url, cookie =  "", "", cookies
    if request.method == 'GET':
        loadUrl = request.args.get('loadUrl')
        url = request.args.get('url')
        if request.args.get('cookie') is not None:
            cookie = request.args.get('cookie')
    else:
        loadUrl = request.form['loadUrl']
        url = request.form['url']
        if "cookie" in request.form:
            cookie = request.form['cookie']
    try:
        resp = requests.get(loadUrl, headers=randHeader(url), cookies={"cookie": cookie})
        resp.encoding = "utf-8"
        content = resp.text
        if resp.status_code == 200:
            return content
        else:
            print(content)
            return ""
    except:
        return ""


#获取随机的http request请求头
def randHeader(referer=None):
    head_connection = ['Keep-Alive', 'close']
    head_accept = ['text/html, application/xhtml+xml, */*']
    head_accept_language = ['zh-CN,fr-FR;q=0.5', 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3']
    head_user_agent = ['Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                           'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
                           'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
                           'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
                           'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
                           'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
                           'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
                           'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
                           'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
                           'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
                           'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
                           'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
                           'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
                           'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
                           'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
                           'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
                           'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
                           'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
                           'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11']
    header = {
        'Connection': head_connection[0],
        'Accept': head_accept[0],
        'Accept-Language': head_accept_language[1],
        'User-Agent': head_user_agent[random.randrange(0, len(head_user_agent))],
        'authority':"search.jd.com"
        }
    if referer is not None:
        header["Referer"] = referer
    return header
def auto_cookie():
    while True:
        try:
            resp = requests.get("https://www.jd.com",
                                 headers=randHeader(), cookies={"cookie": cookies})
            if resp.status_code != 200:
                print("cookie已失效...")
                break;
            else:
                print(str(datetime.now()))
            time.sleep(25)
        except:
            break;
#from threading import Thread
if __name__ == '__main__':
    #t = Thread(target=auto_cookie, args=())
    #t.start()
    app.run(debug=False, host='0.0.0.0',port=12000)

