from datetime import datetime as dt
import sys,shutil,os
class LoggerUtil():
    @staticmethod
    def get_log_file():
        filename = "商品sku扫描记录%s.txt" % (dt.now().strftime('%Y-%m-%d'))
        if not os.path.exists(filename):
            with open(filename,"w",encoding="utf-8") as w:
                w.write("日志记录:\n")
        return filename
    """
       ocr每天扫描会生成新的日志文件
       """
    @staticmethod
    def write_file_log(info=None):
        if info is None:
            info = "[%s][%s]" % (sys.exc_info()[0], sys.exc_info()[1])
        date_str = dt.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(LoggerUtil.get_log_file(), "a+", encoding="utf-8") as f:
            f.write("[%s]:%s\n" % (date_str, info))
            print("[%s]:%s\n" % (date_str, info))
    @staticmethod 
    def write_ocr_error_info(info=None):
        if info is None:
            info = "[%s][%s]" % (sys.exc_info()[0], sys.exc_info()[1])
        date_str = dt.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(LoggerUtil.get_ocr_error_file(), "a+", encoding="utf-8") as f:
            f.write("[%s]:%s\n" % (date_str, info))
            print("[%s]:%s\n" % (date_str, info))
    @staticmethod
    def write_pic_error_info(info=None):
        if info is None:
            info = "[%s][%s]" % (sys.exc_info()[0], sys.exc_info()[1])
        date_str = dt.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(LoggerUtil.get_pic_error_file(), "a+", encoding="utf-8") as f:
            f.write("[%s]:%s\n" % (date_str, info))
            print("[%s]:%s\n" % (date_str, info))

    @staticmethod
    def get_order_file():
        filename = "订单扫描记录%s.txt" % (dt.now().strftime('%Y-%m-%d'))
        if not os.path.exists(filename):
            with open(filename, "w", encoding="utf-8") as w:
                w.write("日志记录:\n")
        return filename

    @staticmethod
    def write_order_log(info=None):
        if info is None:
            info = "[%s][%s]" % (sys.exc_info()[0], sys.exc_info()[1])
        date_str = dt.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(LoggerUtil.get_order_file(), "a+", encoding="utf-8") as f:
            f.write("[%s]:%s\n" % (date_str, info))
            print("[%s]:%s\n" % (date_str, info))

    @staticmethod
    def get_cok_file():
        filename = "cookie%s.txt" % (dt.now().strftime('%Y-%m-%d'))
        if not os.path.exists(filename):
            with open(filename, "w", encoding="utf-8") as w:
                w.write("日志记录:\n")
        return filename

    """
       ocr每天扫描会生成新的日志文件
       """

    @staticmethod
    def write_cookie_log(info=None):
        if info is None:
            info = "[%s][%s]" % (sys.exc_info()[0], sys.exc_info()[1])
        date_str = dt.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(LoggerUtil.get_cok_file(), "a+", encoding="utf-8") as f:
            f.write("[%s]:%s\n" % (date_str, info))
            print("[%s]:%s\n" % (date_str, info))