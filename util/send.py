#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : send.py
@Author: 孟凡不凡
@Date  : 2019/3/19 15:37
@Desc  :  短信发送
'''
import requests


class Send():
    def __init__(self):
        self.send_url = "http://api.1cloudsp.com/api/v2/send"
        self.accesskey = "5tctFWkXe8xRpYdp"
        self.secret = "SMr5iTdcvjnjsaCv5ncttJqbCt3oZpUa"
        self.sign = "19160"
        self.templateId = "39026"
        self.datas = {
            "accesskey": self.accesskey,
            "secret": self.secret,
            "sign" : self.sign,
            "templateId" : self.templateId
        }


    def send(self, mobel="13122111286", content="erp"):

        self.datas["mobile"] = mobel
        self.datas["content"] = content
        html = requests.post(self.send_url, data=self.datas)
        if html.status_code == 200:
            json_str = html.json()

            if json_str["code"] == 0:
                return True, 0
            else:
                return False, json_str["msg"]

        else:
            return False, html.text

if __name__ == '__main__':
    Send().send()