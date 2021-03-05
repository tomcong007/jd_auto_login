#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : get_status.py
@Author: 孟凡不凡
@Date  : 2019/6/4 17:16
@Desc  :  订单路径同步
'''
import sys

import requests

from util.cookie_util import CookieUtil
from util.sql_util import MysqlUtil
status_url = "https://b.jclps.com/so/querySoStatus.do?soNo=%s"
class SoStatus():
    @staticmethod
    def get_status(soNo="CSL4418130120093"):
        url = status_url % soNo
        referer = "https://b.jclps.com/goToMainIframe.do"
        resp = requests.get(url, headers=CookieUtil.get_header(referer=referer),
                                    cookies={"cookie": CookieUtil.get_cookie()})
        if resp.status_code == 200:
            status_json = resp.json()
            try:
                aaData = status_json["data"]["aaData"]
            except:
                print(sys.exc_info())
                return
            conn, cur = MysqlUtil().get_conn()
            for data in aaData:
                soStatus = data["soStatus"]
                operateTime = data["operateTime"]
                source = data["source"]
                operateUser = data["operateUser"]
                cur.execute("select * from t_order_status where soNo = %s and soStatus =%s;", (soNo, soStatus))
                if not cur.fetchone():
                    cur.execute("insert into t_order_status values (%s, %s, %s, %s, %s);" , (soNo, soStatus, operateTime,source, operateUser) )

            print("soNo: %s, 处理成功" % soNo)
            conn.commit()
            cur.close()
            conn.close()


        else:
            print(resp.status_code)
            print(resp.content)
            return

if __name__ == '__main__':
    conn, cur = MysqlUtil().get_conn()
    cur.execute("select DISTINCT soNo from t_order_detail")
    datas = cur.fetchall()
    cur.close()
    conn.close()
    for soNo in datas:
        get_status(soNo)