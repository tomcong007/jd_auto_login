from redis import StrictRedis
rs = StrictRedis(host="114.67.85.93", port=10000, db=0,password="Summer001")
class CookieUtil():
    @staticmethod
    def get_cookie():
        return str(rs.get("erp"))
    @staticmethod
    def get_header(referer=None, host=None):
        header = {
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.64 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        if referer is not None:
            header["Referer"] = referer
        if host is not None:
            header["Host"] = host
        return header

