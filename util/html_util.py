#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : html_util.py
@Author: 孟凡不凡
@Date  : 2019/7/9 11.json:55
@Desc  :  抓取链接
'''
import json
import random
import sys

import requests


class Html():
    def __init__(self, w=None):
        self.w = w


    def get_headers(self, host=None, referer=None, cookies=None, t=0):
        head_user_agent = ['Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.json.0) like Gecko',
                           'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
                           'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.json.0) like Gecko)',
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
                           'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11.json (KHTML, like Geckio) Chrome/20.0.1132.11.json TaoBrowser/3.0 Safari/536.11.json']
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "max-age=0",
            "upgrade-insecure-requests": "1",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded",
            "Connection": "keep-alive",
            "user-agent": head_user_agent[random.randrange(0, len(head_user_agent))]
        }
        if host is not None:
            headers["Host"] = host
        if referer is not None:
            headers["Referer"] = referer
        if cookies is not None:
            headers["Cookie"] = cookies
        if t == 1:
            headers["Content-Type"] = "application/json;charset=UTF-8"
        return headers

    def get_html(self, url, referer=None, host=None,
                 cookies=None, count=0, encoding="utf-8", t=0):

        if count > 5:
            if self.w is None:
                print("url: %s， 连续5次抓取失败，放弃抓取" % url)
            else:
                self.w.log_thread.run_("url: %s， 连续5次抓取失败，放弃抓取" % url)
            return

        try:
            resp = requests.get(
                url,
                headers=self.get_headers(t=t,
                                         referer=referer,
                                         host=host,
                                         cookies=cookies),timeout=2*60)
        except BaseException:
            if self.w is None:
                print(
                "url: %s, [%s] -- [%s]" %
                (url, sys.exc_info()[0], sys.exc_info()[1]))

            else:
                self.w.log_thread.run_(
                    "url: %s, [%s] -- [%s]" %
                    (url, sys.exc_info()[0], sys.exc_info()[1]))
            return self.get_html(url, referer=referer, host=host,
                             cookies=cookies, count=count + 1, encoding=encoding, t=t)

        if resp.status_code == 200:
            resp.encoding = encoding
            return resp.text
        else:
            if self.w is None:
                print("url: %s, status: %s" %
                (url, resp.status_code))
            else:
                self.w.log_thread.run_(
                    "url: %s, status: %s" %
                    (url, resp.status_code))
            return self.get_html(url, referer=referer, host=host,
                                 cookies=cookies, count=count + 1, encoding=encoding, t=t)

    def post_html(self, url, referer=None, host=None, cookies=None,
                  count=0, encoding="utf-8", data={}, json={}, t=0):
        if count > 5:
            if self.w is None:
                print("url: %s， 连续5次抓取失败，放弃抓取" % url)
            else:
                self.w.log_thread.run_("url: %s， 连续5次抓取失败，放弃抓取" % url)
            return

        try:
            resp = requests.post(
                url,
                headers=self.get_headers(
                    referer=referer,
                    host=host,
                    cookies=cookies, t=t),
                data=data,
                json=json,timeout=2*60)
        except BaseException:
            if self.w is None:
                print("url: %s, [%s] -- [%s]" %
                                   (url, sys.exc_info()[0], sys.exc_info()[1]))
            else:
                self.w.log_thread.run_("url: %s, [%s] -- [%s]" %
                                   (url, sys.exc_info()[0], sys.exc_info()[1]))
            return self.post_html(url, referer=referer, host=host, cookies=cookies,
                                  count=count + 1, encoding=encoding, data=data, json=json, t=t)

        if resp.status_code == 200:
            resp.encoding = encoding
            return resp.text
        else:
            if self.w is None:
                print("url: %s, status: %s" %
                (url, resp.status_code))
            else:
                self.w.log_thread.run_(
                    "url: %s, status: %s" %
                    (url, resp.status_code))
            return self.post_html(url, referer=referer, host=host, cookies=cookies,
                                  count=count + 1, encoding=encoding, data=data, json=json, t=t)

    def post_json(self, url, referer=None, host=None, cookies=None,
                  count=0, encoding="utf-8", data={}, json={}, t=0):
        if count > 5:
            if self.w is None:
                print("url: %s， 连续5次抓取失败，放弃抓取" % url)
            else:
                self.w.log_thread.run_("url: %s， 连续5次抓取失败，放弃抓取" % url)
            return

        try:
            resp = requests.post(url, headers=self.get_headers(referer=referer, host=host, cookies=cookies, t=t),
                                 data=data,
                                 json=json,timeout=120)
        except BaseException:
            if self.w is None:
                print(
                "url: %s, [%s] -- [%s]" %
                (url, sys.exc_info()[0], sys.exc_info()[1]))
            else:
                self.w.log_thread.run_(
                    "url: %s, [%s] -- [%s]" %
                    (url, sys.exc_info()[0], sys.exc_info()[1]))
            return self.post_json(url, referer=referer, host=host, cookies=cookies, count=count + 1, encoding=encoding,
                                  data=data, json=json, t=t)

        if resp.status_code == 200:
            resp.encoding = encoding
            return resp.json()
        else:
            if self.w is None:
                print("url: %s, status: %s" %
                (url, resp.status_code))
            else:
                self.w.log_thread.run_(
                    "url: %s, status: %s" %
                    (url, resp.status_code))
            return self.post_json(url, referer=referer, host=host, cookies=cookies, count=count + 1, encoding=encoding,
                                  data=data, json=json, t=t)

    @staticmethod
    def cook_str_dict(cookies=""):
        cookies_dict = {}
        cooks = cookies.split(";")
        for cook in cooks:
            c = cook.split("=")
            key = c[0]
            value = "".join(c[1:])
            cookies_dict[key] = value
        return cookies_dict

    @staticmethod
    def cook_dict_str(cookies_dict={}):
        cookies = ""
        for key in cookies_dict:
            cookies += key
            cookies += "="
            cookies += cookies_dict[key]
            cookies += ";"
        return cookies.strip(";")

class SpuSku():
    def __init__(self, cookies=None):
        self.cookies = cookies
    def spu_get_sku(self, spu_lst=[]):

        url = "https://sz.jd.com/productDetail/getImageUrlBySpuIds.ajax?spuIds=%s" % ','.join(spu_lst)
        try:
            resp = Html().get_html(url, cookies=self.cookies, host="sz.jd.com")
        except:
            print()
            return False
        resp_json = json.loads(resp)
        lst = []
        if resp_json["message"] or resp_json["message"] == "success":
            data = resp_json["content"]["data"]
            for d in data:
                spu_id = d["spuId"]
                sku_id = int(d["proUrl"].split("/")[-1].split(".")[0])
                lst.append((spu_id, sku_id))
            return lst
        else:
            print(resp_json["message"])
            return False

if __name__ == '__main__':
    url = "https://jzt-api.jd.com/touchpoint/campaign/add"
    referer = "https://jzt.jd.com/touch_point/index.html"

    data = {"campaignType": 28, "putType": 3, "name": "www", "startTime": "2019-09-04", "endTime": None,
            "dateRange": "", "dayBudget": None, "uniformSpeed": 0, "billingType": 0, "subExpType": None,
            "requestFrom": 0}
    cookies = "shshshfpa=b17dd7df-7db4-0bab-2b65-ea77565a9b44-1563869747; shshshfpb=affW6n1h9K6qQbmyJiVncYg%3D%3D; areaId=17; user-key=832662e5-6190-4cc2-b6e5-3728a189b693; ipLocation=%u6e56%u5317; mt_xid=V2_52007VwMWVV9cU14dTx1dAG8EElFYWFJdG0kpDgBjAxcHDllOWx9KTkAAbwRGTlRaAFkDSxpZDW9QQVNbXwUJL0oYXA17AhtOXlpDWhpCHV4OZwciUG1YYlIcSBxeB2MAFlBUW1ZfGE8RWwZXARZTWA%3D%3D; PCSYCityID=CN_420000_420100_420107; ipLoc-djd=17-1381-3079-50764.1418251783; cn=7; unpl=V2_ZzNtbURSF0d9DUBceR1cDWIHF1oSURRCfQtFBHtNWAZlAUYIclRCFX0UR1xnGF4UZwcZX0RcQRBFCEVkexhdBWMAGlxKVXNFGwpEOnkaXTVXABJtQ2dDEXIKQlV%2fG1oBZgYaWkJURhV1D0JUSylcDWAzIoX065eewtzr1a%2bX7tPxo8Xm84Dura2g54DPhIi77jMVXktSSiV0OEdkMHddSGcHFV9GVkcXcwxHUXMeXAZiAxJaRldzFEUL; __jdv=76161171|jd.ss8899888.com|t_1001529093_a_33_320|jingfen|74ec947935194546a7ff922a1e5233ed|1567496196529; 3AB9D23F7A4B3C9B=OIKW2G436IZFYBK7CINTEPSZMSU324BMPQH6XZYPSL5KI746OVBSH5OIFTQNNXLOIHZ77OECZTGZXKSN32WSN2PDU4; shshshfp=cb77d0fe32230e07a48325408bd62381; language=zh_CN; __jdu=1563505375049612411651; TrackID=1tNSrxc_-lk4lQz1a_nYQQHMvzKnAU4ac7rWzeicLqUl9z_UW2uvnrTFBjBCesCMuUpZz-Bmx4WZo02CUqmmqCVY-16Vy0P4YVejOeWNrnz0; pinId=Ij4MViIlCwp9ao2-6idyxw; pin=fxb201943; unick=fxb201943; ceshi3.com=000; _tp=EMduwEfJf7%2B%2FbHN8WXAMcA%3D%3D; logining=1; _pst=fxb201943; thor=0331DD1635D56FDFF7B9D17506EAB2772B271A41D075888E1F071676EEA11E2A1CCD51AE860EBE21B63E3371BD75C0D3056EA7C2194556B2225F4B38AC30FE85CE0BAC330EFDC6F1242FF1F520E2FDED04ADCF15B1EF12DC869CD6F5392AF8E3A85C13D7E6418F7F16661EA18F4915351B78B0E0969576994BF46720B44BF823DE776CBE72475C08D07C74B87CF10FD6; _base_=YKH2KDFHMOZBLCUV7NSRBWQUJPBI7JIMU5R3EFJ5UDHJ5LCU7R2NILKK5UJ6GLA2RGYT464UKXAI4Z6HPCTN4UQM3WHVQ4ENFP57OC3J22GJ6JXASZ5HSVNXR3SVXXVJTCNE6YVKRXISU43D2PG5FYPIHIXMXGPYGVEOCQCSG4SOQWCP5WPWO6EFS7HEHMRWVKBRVHB33TFD4Y2ROKRNMJNVAOXP44SGQCURZQ64SL7HGPDX3R6BLYATHAAKS65ANVHSS6HGFDSJ5GNPZUF4HKTJMIZ4PZVKSIHU3ULSN74K4NW75PSROI3M6HZ6LKSCQ6SBYA6DJSYPK2WH642BK7ADA6DN2PTMQIMR2XFNAYJOIVSBZNMQ; b-sec=7AKEU26U64TIORR4O2YRLTVQ34FV74DMC347THEB3D7TX25C2HX4JUQH62PCPQ3O; __jda=146207855.1563505375049612411651.1563505375.1566452630.1567584230.47; __jdc=146207855; clientlanguage=zh_CN; JSESSIONID=984256F5E89F60E5A8811BEE9F47AD61.s1; __jdb=146207855.7.1563505375049612411651|47.1567584230"

    resp = Html().post_html(url, referer=referer, cookies=cookies, data=json.dumps(data), t=1)
    # self.w.log_thread.run_(resp)
    #
    # {"businessType": 16777216, "campaignId": 171690506, "campaignName": "www", "adGroupName": "frist",
    #  "ads": "{\"adList\":[{\"skuId\":48821764767,\"name\":\"系统推荐-48821764767-手动工具\",\"imgUrl\":\"jfs/t1/48631/18/1212/211378/5cee1ce0E25fec2af/cccbbb9b94070a6a.png\",\"mainVideoId\":null,\"playUrl\":null,\"categoryId\":9921,\"brandId\":\"354889\",\"brandName\":\"极立耐\",\"categoryName\":\"手动工具\",\"customTitle\":\"吸盘定位片 塑料环保自粘式贴片粘贴扎带固定座电线卡粘盘 粘贴块（一包100个） CHC-100 12.5X12.5mm 黑色\",\"_productName\":\"吸盘定位片 塑料环保自粘式贴片粘贴扎带固定座电线卡粘盘 粘贴块（一包100个） CHC-100 12.5X12.5mm 黑色\"},{\"skuId\":48821764770,\"name\":\"系统推荐-48821764770-手动工具\",\"imgUrl\":\"jfs/t1/39481/39/7636/429391/5cee1cf3Eb635235b/898a54c74859f38d.png\",\"mainVideoId\":null,\"playUrl\":null,\"categoryId\":9921,\"brandId\":\"354889\",\"brandName\":\"极立耐\",\"categoryName\":\"手动工具\",\"customTitle\":\"吸盘定位片 塑料环保自粘式贴片粘贴扎带固定座电线卡粘盘 粘贴块（一包100个） CHC-102 28X28mm 黑色\",\"_productName\":\"吸盘定位片 塑料环保自粘式贴片粘贴扎带固定座电线卡粘盘 粘贴块（一包100个） CHC-102 28X28mm 黑色\"},{\"skuId\":48821764771,\"name\":\"系统推荐-48821764771-手动工具\",\"imgUrl\":\"jfs/t1/63173/15/653/159518/5cee1cf5E32e111b5/5e6c983a7649a748.png\",\"mainVideoId\":null,\"playUrl\":null,\"categoryId\":9921,\"brandId\":\"354889\",\"brandName\":\"极立耐\",\"categoryName\":\"手动工具\",\"customTitle\":\"吸盘定位片 塑料环保自粘式贴片粘贴扎带固定座电线卡粘盘 粘贴块（一包100个） CHC-101 21.5X21.5mm 黑色\",\"_productName\":\"吸盘定位片 塑料环保自粘式贴片粘贴扎带固定座电线卡粘盘 粘贴块（一包100个） CHC-101 21.5X21.5mm 黑色\"},{\"skuId\":48821764768,\"name\":\"系统推荐-48821764768-手动工具\",\"imgUrl\":\"jfs/t1/60954/29/680/393569/5cee1ce5E046652a8/d006e3a09720c552.png\",\"mainVideoId\":null,\"playUrl\":null,\"categoryId\":9921,\"brandId\":\"354889\",\"brandName\":\"极立耐\",\"categoryName\":\"手动工具\",\"customTitle\":\"吸盘定位片 塑料环保自粘式贴片粘贴扎带固定座电线卡粘盘 粘贴块（一包100个） CHC-101S 19.5x19.5mm 白色\",\"_productName\":\"吸盘定位片 塑料环保自粘式贴片粘贴扎带固定座电线卡粘盘 粘贴块（一包100个） CHC-101S 19.5x19.5mm 白色\"},{\"skuId\":48821764769,\"name\":\"系统推荐-48821764769-手动工具\",\"imgUrl\":\"jfs/t1/49704/27/1153/805864/5cee1ce7E28af7b99/8cea597a8922ecd3.png\",\"mainVideoId\":null,\"playUrl\":null,\"categoryId\":9921,\"brandId\":\"354889\",\"brandName\":\"极立耐\",\"categoryName\":\"手动工具\",\"customTitle\":\"吸盘定位片 塑料环保自粘式贴片粘贴扎带固定座电线卡粘盘 粘贴块（一包100个） CHC-102 28X28mm 白色\",\"_productName\":\"吸盘定位片 塑料环保自粘式贴片粘贴扎带固定座电线卡粘盘 粘贴块（一包100个） CHC-102 28X28mm 白色\"},{\"skuId\":48821764772,\"name\":\"系统推荐-48821764772-手动工具\",\"imgUrl\":\"jfs/t1/57301/14/1139/477600/5cee1cf7E45e42f00/8e78417d7e5e91b6.png\",\"mainVideoId\":null,\"playUrl\":null,\"categoryId\":9921,\"brandId\":\"354889\",\"brandName\":\"极立耐\",\"categoryName\":\"手动工具\",\"customTitle\":\"吸盘定位片 塑料环保自粘式贴片粘贴扎带固定座电线卡粘盘 粘贴块（一包100个） CHC-101 21.5X21.5mm 白色\",\"_productName\":\"吸盘定位片 塑料环保自粘式贴片粘贴扎带固定座电线卡粘盘 粘贴块（一包100个） CHC-101 21.5X21.5mm 白色\"},{\"skuId\":48821764773,\"name\":\"系统推荐-48821764773-手动工具\",\"imgUrl\":\"jfs/t1/46905/19/1134/733219/5cee1d09E8e4cfa8d/66c00872cf1b2b81.png\",\"mainVideoId\":null,\"playUrl\":null,\"categoryId\":9921,\"brandId\":\"354889\",\"brandName\":\"极立耐\",\"categoryName\":\"手动工具\",\"customTitle\":\"吸盘定位片 塑料环保自粘式贴片粘贴扎带固定座电线卡粘盘 粘贴块（一包100个） CHC-100 12.5X12.5mm 白色\",\"_productName\":\"吸盘定位片 塑料环保自粘式贴片粘贴扎带固定座电线卡粘盘 粘贴块（一包100个） CHC-100 12.5X12.5mm 白色\"}]}",
    #  "requestFrom": 0}
