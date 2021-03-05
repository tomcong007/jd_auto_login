#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : cookie_class.py
@Author: 孟凡不凡
@Date  : 2019/7/11 17:23
@Desc  :  cookies维持
'''
import time
from threading import Thread

from PyQt5 import QtWidgets
from PyQt5.QtCore import QUrl, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from datetime import datetime as dt

from PyQt5.QtWidgets import QPushButton

from cookie import Ui_Cookie_Form
from util.html_util import Html
from util.sql_util import MysqlUtil
import PyQt5.sip
erp_log_url = "http://passport.jd.com/common/loginPage?regTag=2&pwdTag=2&from=lop_jdwl&btnTag=2248088d7c49c1c4&ReturnUrl=http%3A%2F%2Fb.jclps.com%2F"
baidu_url = "https://www.baidu.com"
wms_log_url = "http://passport.jd.com/common/loginPage?regTag=2&pwdTag=2&from=lop_jdwl&btnTag=2248088d7c49c1c4&ReturnUrl=http://jwms.jclps.com"
wms_log_url_su = "http://jwms.jclps.com"
wms_old_warehouse_url = "https://jwms.jclps.com/report-new/dashboard?loginType=warehouse&warehouseNo=800000163"



# 创建自己的浏览器控件，继承自QWebEngineView
class MyWebEngineView(QWebEngineView):
    def __init__(self, *args, **kwargs):
        super(MyWebEngineView, self).__init__(*args, **kwargs)
        # 绑定cookie被添加的信号槽
        QWebEngineProfile.defaultProfile().cookieStore().cookieAdded.connect(self.onCookieAdd)
        self.cookies = {}  # 存放cookie字典

    def onCookieAdd(self, cookie):  # 处理cookie添加的事件
        name = cookie.name().data().decode('utf-8')  # 先获取cookie的名字，再把编码处理一下
        value = cookie.value().data().decode('utf-8')  # 先获取cookie值，再把编码处理一下
        self.cookies[name] = value  # 将cookie保存到字典里

    # 获取cookie
    def get_cookie(self):
        cookie_str = ''
        for key, value in self.cookies.items():  # 遍历字典
            cookie_str += (key + '=' + value + ';')  # 将键值对拿出来拼接一下
        return cookie_str  # 返回拼接好的字符串

    def clear_cookies(self):
        self.page().profile().clearHttpCache()
        self.page().profile().cookieStore().deleteAllCookies()
        self.cookies = {}


class Cookie_class(QtWidgets.QMainWindow, Ui_Cookie_Form):
    def __init__(self, parent=None):
        super(Cookie_class, self).__init__(parent)

        self.setupUi(self)
        self.setWindowIcon(QIcon("login.jpg"))
        self.web = MyWebEngineView(self.web_widget)
        self.web.resize(800, 400)
        self.web.load(QUrl(baidu_url))
        self.clear_cookies.clicked.connect(self.clear)
        self.erp_btn.clicked.connect(self.erp_commit)
        self.wms_btn.clicked.connect(self.wms_commit)
        self.log_thread = logThread()
        self.log_thread.result.connect(self.add_log)

        self.erp_load_btn = QPushButton("加载erp登陆页面")
        self.erp_load_btn.clicked.connect(self.erp_load)
        self.erp_load_btn.setVisible(False)


        self.wms_load_btn = QPushButton("加载wms登陆页面")
        self.wms_load_btn.clicked.connect(self.wms_load)
        self.wms_load_btn.setVisible(False)

        self.baidu_load_btn = QPushButton("加载baidu登陆页面")
        self.baidu_load_btn.clicked.connect(self.baidu_load)
        self.baidu_load_btn.setVisible(False)

        self.wms_warehouse_load_btn = QPushButton("加载wms仓库登陆页面")
        self.wms_warehouse_load_btn.clicked.connect(self.wms_warehouse_load)
        self.wms_warehouse_load_btn.setVisible(False)

        self.erp_login_btn = QPushButton("erp登陆流程")
        self.erp_login_btn.clicked.connect(self.erp_login_load)
        self.erp_login_btn.setVisible(False)

        self.wms_login_btn = QPushButton("erp登陆流程")
        self.wms_login_btn.clicked.connect(self.wms_login_load)
        self.wms_login_btn.setVisible(False)
        self.xxx = ""
        # self.automatic_login_thread = AutoLoginThread(self)
        # self.automatic_login_thread.start()


    def wms_login_load(self):
        self.web.page().runJavaScript("""document.getElementById("loginname").value="hbtj0001";""")
        self.web.page().runJavaScript("""document.getElementById("nloginpwd").value="qaz987";""")
        self.web.page().runJavaScript("""document.getElementById("paipaiLoginSubmit").click();""")

    def erp_login_load(self):
        self.web.page().runJavaScript("""document.getElementById("loginname").value="sanbenjd001";""")
        self.web.page().runJavaScript("""document.getElementById("nloginpwd").value="sanbenjd001";""")
        self.web.page().runJavaScript("""document.getElementById("paipaiLoginSubmit").click();""")



    def erp_load(self):
        self.web.page().load(QUrl(erp_log_url))

    def wms_load(self):
        self.web.page().load(QUrl(wms_log_url))

    def wms_load_su(self):
        self.web.page().load(QUrl(wms_log_url_su))

    def baidu_load(self):
        self.web.page().load(QUrl(baidu_url))

    def wms_warehouse_load(self):
        self.web.page().load(QUrl(wms_old_warehouse_url))

    # 添加日志
    def add_log(self, p_str):
        date_str = dt.now().strftime('%Y-%m-%d %H:%M:%S')
        self.log_text.append("[%s]: %s" % (date_str, p_str))



    # 获取网页源代码
    def get_info(self):
        self.web.page().toHtml(self.x)
        return self.xxx
    def x(self,html):
        # print(html)
        self.xxx =html
    # 清理缓存
    def clear(self):
        self.web.clear_cookies()
        self.log_thread.run_("缓存清理结束")

    # 设置按钮是否可按
    def set_btn(self):
        if self.erp_btn.isEnabled():
            self.wms_btn.setEnabled(False)
            self.erp_btn.setEnabled(False)
            # self.clear_cookies.setEnabled(False)
        else:
            self.wms_btn.setEnabled(True)
            self.erp_btn.setEnabled(True)
            # self.clear_cookies.setEnabled(True)

    def erp_is_run(self):
        if self.erp_spider.isFinished():
            self.set_btn()
            self.erp_run_time.stop()

    def erp_commit(self):
        self.set_btn()
        self.erp_spider = ErpThread(self)
        self.erp_run_time = QTimer()
        self.erp_run_time.timeout.connect(self.erp_is_run)
        self.erp_run_time.start(1000)
        self.erp_spider.start()



    def wms_is_run(self):
        if self.wms_spider.isFinished():
            self.set_btn()
            self.wms_run_time.stop()
    def test(self):
        if self.wms_btn.isEnabled():
            pass

    def wms_commit(self):
        self.set_btn()
        self.wms_spider = WmsThread(self)
        self.wms_run_time = QTimer()
        self.wms_run_time.timeout.connect(self.wms_is_run)
        self.wms_run_time.start(1000)
        self.wms_spider.start()


class ErpThread(QThread):
    def __init__(self, w, parent=None):
        super(ErpThread, self).__init__(parent)
        self.w = w

    def is_login(self):
        text = self.w.get_info()
        if "云物流" in text:
            return True
        return False

    def save_erp_cookies(self):
        cookie = self.w.web.get_cookie()
        cookies_dict = Dict_Str.cook_str_dict(cookie)
        key_lst = ["__jda", "__jdc", "__jdv", "__jdb", "pin", "thor", "unick"]
        new_cookies = {}
        conn, cur = MysqlUtil().get_conn()
        for key in cookies_dict.keys():
            cur.execute("select id, val from t_cookie where region = %s and name = %s order by update_date desc;",
                        ("erp", key))
            data = cur.fetchone()
            if data:
                id, val = data
                if val == cookies_dict[key]:
                    cur.execute("update t_cookie set update_date = now() where id = %s;", (id,))
                else:
                    cur.execute(
                        "insert into t_cookie (region, name, val, create_date, update_date) values (%s, %s, %s, now(), now());",
                        ("erp", key, cookies_dict[key]))
            else:
                cur.execute(
                    "insert into t_cookie (region, name, val, create_date, update_date) values (%s, %s, %s, now(), now());",
                    ("erp", key, cookies_dict[key]))

            new_cookies[key] = cookies_dict[key]

        if cookie is not None:
            cur.execute("update t_spider_cookie set val = %s where name = 'erp'", (Dict_Str.cook_dict_str(new_cookies)))
        conn.commit()
        cur.close()
        conn.close()

    def run(self):
        while True:
            self.w.erp_load_btn.click()
            self.w.log_thread.run_("正在进入erp登陆页面，请等待")
            time.sleep(5)
            self.w.erp_login_btn.click()
            self.w.log_thread.run_("正在进行登陆")
            time.sleep(5)

            self.w.get_info()
            time.sleep(2)
            if self.is_login():
                self.w.log_thread.run_("登陆成功， 休眠中...")
                self.save_erp_cookies()
                time.sleep(2)
                self.w.log_thread.run_("cookies更新成功， 休眠中...")

                time.sleep(10)
                self.w.baidu_load_btn.click()
                time.sleep(10)

                break
            else:
                self.w.log_thread.run_("登陆失败, 稍后重新登陆")
        self.w.clear()


class WmsThread(QThread):
    def __init__(self, w, parent=None):
        super(WmsThread, self).__init__(parent)
        self.w = w

    def is_login(self):
        url = "https://jwms.jclps.com/api/master/commonInfo/getUserInfo.do"
        referer = "https://jwms.jclps.com/?loginType=tenant"
        text = Html(self.w).get_html(url, referer, cookies=self.w.web.get_cookie())
        if "CP20000000032" in text:
            return True
        return False

    def is_warehouse(self):
        url = "https://jwms.jclps.com/home.do?t=%s" % int(time.time())
        referer = "https://jwms.jclps.com/main_agent?loginType=warehouse&warehouseNo=800000163"
        text = Html(self.w).get_html(url, referer, cookies=self.w.web.get_cookie())

        if "登录仓库：" in text:
            return True
        return False



    def save_wms_cookies(self):
        cookie = self.w.web.get_cookie()
        cookies_dict = Dict_Str.cook_str_dict(cookie)
        key_lst = ["__jda", "__jdc", "__jdv", "__jdb", "pin", "thor", "unick", "13A92E989B1D0AB30D0E5714C05D1171",
                   "jcloud.wms.SessionID","domain_code"]
        new_cookies = {}
        conn, cur = MysqlUtil().get_conn()
        for key in cookies_dict.keys():

            cur.execute(
                "select id, val from t_cookie where region = %s and name = %s order by update_date desc;",
                ("wms_erp", key))
            data = cur.fetchone()
            if data:
                id, val = data
                if val == cookies_dict[key]:
                    cur.execute("update t_cookie set update_date = now() where id = %s;", (id,))
                else:
                    cur.execute(
                        "insert into t_cookie (region, name, val, create_date, update_date) values (%s, %s, %s, now(), now());",
                        ("wms_erp", key, cookies_dict[key]))
            else:
                cur.execute(
                    "insert into t_cookie (region, name, val, create_date, update_date) values (%s, %s, %s, now(), now());",
                    ("wms_erp", key, cookies_dict[key]))

            new_cookies[key] = cookies_dict[key]

        if cookie is not None:
            cur.execute("update t_spider_cookie set val = %s where name = 'erp_wms_cookie'",
                        (Dict_Str.cook_dict_str(new_cookies)))
        conn.commit()
        self.w.log_thread.run_("erp_wms_cookie: 更新成功")
        cur.close()
        conn.close()

    def run(self):
        # 点击进入登陆界面
        self.w.wms_load_btn.click()
        self.w.log_thread.run_("正在进入wms登陆页面，请等待")
        time.sleep(5)
        # 点击登陆流程

        flag = True
        while True:
            self.w.wms_load_btn.click()
            time.sleep(3)
            self.w.wms_login_btn.click()
            self.w.log_thread.run_("正在进行登陆")
            time.sleep(5)
            if self.is_login():
                self.w.log_thread.run_("验证码登陆成功")
                time.sleep(5)
                while True:
                    self.w.wms_warehouse_load_btn.click()
                    self.w.log_thread.run_("正在跳转wms仓库页面")
                    time.sleep(10)
                    if self.is_warehouse():
                        self.w.log_thread.run_("仓库登陆成功")
                        time.sleep(10)
                        self.save_wms_cookies()
                        time.sleep(10)
                        self.w.baidu_load_btn.click()
                        break
                    else:
                        time.sleep(10)
                        continue
                break
            else:
                if flag:
                    flag = False
                    time.sleep(2)
                else:
                    time.sleep(2)
        self.w.clear()


class Dict_Str():
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


class logThread(QThread):
    result = pyqtSignal(str)

    def __init__(self, parent=None):
        super(logThread, self).__init__(parent)

    def run_(self, message):
        # time.sleep(random.random() * 5)
        self.result.emit(message)


class AutoLoginThread(QThread):
    def __init__(self, w=None, parent=None):
        super(AutoLoginThread, self).__init__(parent)
        self.w = w

    def is_auto_login(self):
        time.sleep(10)
        while True:
            if self.w.wms_btn.isEnabled():
                self.w.wms_btn.click()
                self.w.log_thread.run_("开始登录wms")
                break
            else:
                time.sleep(10)

    def auto_login(self):
        if self.w.wms_btn.isEnabled():
            self.w.erp_btn.click()
            t = Thread(target=self.is_auto_login)
            t.start()
            t.join()


    def run(self):
        while True:
            self.auto_login()
            self.w.log_thread.run_("占时不需要自动登录，6小时后自行登录")
            time.sleep(6*60*60)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = Cookie_class()
    mainWindow.show()
    sys.exit(app.exec_())
