#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : order_manag_util.py
@Author: 孟凡不凡
@Date  : 2019/4/16 17:41
@Desc  :  销售订单管理
'''
import sys
import time

import requests,random
from util.cookie_util import CookieUtil


class OrderManage():
    @staticmethod
    def build_request(dict={}, start=0, length=100):
        params = {
            "sellerId": 20000000049,
            # 云笔记
            "deptId:": "",
            "sellerNo": "",
            "deptNo": "",
            "shopId": "",
            "shopNo": "",
            "spCreateTime":"",
            "soType":"1",
            "soNo":"",
        }
        if "spCreateTime" in dict:
            params["spCreateTime"] = dict["spCreateTime"]
        if "soNo" in dict:
            params["soNo"] = dict["soNo"]

        aoData = [
            {"name": "sEcho", "value": 5},
            {"name": "iColumns", "value": 17},
            {"name": "sColumns", "value": ",,,,,,,,,,"},
            {"name": "iDisplayStart", "value": start},
            {"name": "iDisplayLength", "value": length},
            {"name": "mDataProp_0", "value": 0},
            {"name": "mDataProp_1", "value": "1"},
            {"name": "mDataProp_2", "value": "soNo"},
            {"name": "mDataProp_3", "value": "spSoNo"},
            {"name": "mDataProp_4", "value": "parentId"},
            {"name": "mDataProp_5", "value": "soType"},
            {"name": "mDataProp_6", "value": "soStatus"},
            {"name": "mDataProp_7", "value": "consignee"},
            {"name": "mDataProp_8", "value": "consigneeAddr"},
            {"name": "mDataProp_9", "value": "shipperName"},
            {"name": "mDataProp_10", "value": "wayBill"},
            {"name": "mDataProp_11", "value": "spCreateTime"},
            {"name": "mDataProp_12", "value": "createTime"},
            {"name": "mDataProp_13", "value": "stationName"},
            {"name": "mDataProp_14", "value": "chronergyStr"},
            {"name": "mDataProp_15", "value": "expectDeliveryDate"},
            {"name": "mDataProp_16", "value": "orderAmount"},
            {"name": "iSortCol_0", "value": 11},
            {"name": "sSortDir_0", "value": "desc"},
            {"name": "iSortingCols", "value": 1}

        ]
        params["aoData"] = str(aoData)
        referer = "https://b.jclps.com/goToMainIframe.do"
        host = "b.jclps.com"

        resp = requests.post("https://b.jclps.com/so/querySoMainList.do?rand=" + str(random.random()),
                             data=params, headers=CookieUtil.get_header(referer, host),
                             cookies={"cookie": CookieUtil.get_cookie()})

        return resp




class OrderSoMain():
    @staticmethod
    def get_order_main(id=4418117297882):
        order_url = "https://b.jclps.com/so/toSoMain.do?id=%s&rand=%s&_=%s" % (id, random.random(), int(time.time() * 1000))
        host = "b.jclps.com"
        referer = "https://b.jclps.com/goToMainIframe.do"

        try:
            resp = requests.get(order_url, headers=CookieUtil.get_header(referer, host),
                                cookies={"cookie": CookieUtil.get_cookie()})
        except:
            print(sys.exc_info())
            return
        return resp
    @staticmethod
    def get_order_date(soNo="CSL4418117297882"):
        order_date_url = "https://b.jclps.com/so/querySoStatus.do?soNo=%s" % soNo
        host = "b.jclps.com"
        referer = "https://b.jclps.com/goToMainIframe.do"

        try:
            resp = requests.get(order_date_url, headers=CookieUtil.get_header(referer, host),
                                cookies={"cookie": CookieUtil.get_cookie()})
        except:
            print(sys.exc_info())
            return
        return resp


if __name__ == '__main__':
    # print(OrderManage().build_request().json())
    print(OrderSoMain().get_order_date().text)