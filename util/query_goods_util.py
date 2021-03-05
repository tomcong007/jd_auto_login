import requests,random
from util.cookie_util import CookieUtil
class QueryGoodsUtil():
    @staticmethod
    def build_request(dict,start=0,length=10):
        params = {
            "sellerId": 20000000049,
            #云笔记
            "deptId:": 4418046511276,
            "sellerNo": "CCP0020000000049",
            "deptNo": "CBU4418046511276",
            "shopId":"",
            "shopNo":""
        }
        if "deptNo" in dict:
            params["deptNo"] = dict["deptNo"]
        #查询某店铺商品
        if "shopId" in dict:
            params["shopId"] = dict["shopId"]
        #对应的店铺编号
        if "shopNo" in dict:
            params["shopNo"] = dict["shopNo"]
        if "jdDeliver" in dict:
            params["jdDeliver"] = dict["jdDeliver"]
        #查询单sku_num
        if "barcode" in dict:
            params["barcode"] = dict["barcode"]
        aoData = [
            {"name": "sEcho", "value": 3},
            {"name": "iColumns", "value": 11},
            {"name": "sColumns", "value": ",,,,,,,,,,"},
            {"name": "iDisplayStart", "value": start},
            {"name": "iDisplayLength", "value": length},
            {"name": "mDataProp_0", "value": 0},
            {"name": "mDataProp_1", "value": "shopGoodsName"},
            {"name": "mDataProp_2", "value": "goodsNo"},
            {"name": "mDataProp_3", "value": "spGoodsNo"},
            {"name": "mDataProp_4", "value": "isvGoodsNo"},
            {"name": "mDataProp_5", "value": "shopGoodsNo"},
            {"name": "mDataProp_6", "value": "barcode"},
            {"name": "mDataProp_7", "value": "shopName"},
            {"name": "mDataProp_8", "value": "createTime"},
            {"name": "mDataProp_10", "value": "isCombination"},
            {"name": "sSortDir_0", "value": "desc"},
            {"name": "iSortingCols", "value": 1}]
        params["aoData"] = str(aoData)
        referer = "https://b.jclps.com/goToMainIframe.do"

        resp = requests.post("https://b.jclps.com/shopGoods/queryShopGoodsList.do?rand=" + str(random.random()),
                             data=params, headers=CookieUtil.get_header(referer), cookies={"cookie": CookieUtil.get_cookie()})

        return resp


