import json
from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from urllib.parse import quote_plus,urlparse,parse_qs
from base64 import decodebytes,encodebytes

class AliPay(object):
    """
    支付宝支付接口
    """
    #初始化支付宝公共请求参数
    def __init__(self,app_id,app_notify_url,app_private_key_path,alipay_public_key_path,return_url,debug=False):
        self.app_id = app_id
        self.app_notify_url = app_notify_url
        self.app_private_key_path = app_private_key_path
        self.app_private_key = None
        self.return_url = return_url

        with open(self.app_private_key_path) as f:
            self.app_private_key = RSA.import_key(f.read())

        self.alipay_public_key_path = alipay_public_key_path
        with open(self.alipay_public_key_path) as f:
            self.alipay_public_key = RSA.import_key(f.read())

        #debug为true时请求支付宝沙箱环境的url
        if debug:
            self.__gateway = "https://openapi.alipaydev.com/gateway.do"
        else:
            self.__gateway = "https://openapi.alipay.com/gateway.do"

    #构造支付宝请求参数
    def direct_pay(self,subject,out_trade_no,total_amount,return_url=None,**kwargs):
        biz_content = {
            "subject":subject,
            "out_trade_no":out_trade_no,
            "total_amount":total_amount,
            "product_code":"FAST_INSTANT_TRADE_PAY",
        }

        biz_content.update(kwargs)
        data = self.build_body("alipay.trade.page.pay",biz_content,self.return_url)

        return self.sign_data(data)


    def build_body(self,method,biz_content,return_url=None):
        data = {
            "app_id":self.app_id,
            "method":method,
            "charset":"utf-8",
            "sign_type":"RSA2",
            "timestamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version":"1.0",
            "biz_content":biz_content

        }

        if return_url:
            data["notify_url"] = self.app_notify_url
            data["return_url"] = self.return_url

        return data

    def sign_data(self,data):
        data.pop("sign",None)
        #将字符串排序
        unsigned_items = self.ordered_data(data)
        unsigned_string = "&".join("{0}={1}".format(k,v) for k,v in unsigned_items)
        sign = self.sign(unsigned_string.encode("utf-8"))
        quoted_string = "&".join("{0}={1}".format(k,quote_plus(v)) for k,v in unsigned_items)

        #获得最终的订单信息字符串
        signed_string = quoted_string + "&sign=" + quote_plus(sign)
        return signed_string

    def ordered_data(self,data):
        complex_keys = []
        for key,value in data.items():
            if isinstance(value,dict):
                complex_keys.append(key)

        #将字典类型的数据dump出来
        for key in complex_keys:
            data[key] = json.dumps(data[key],separators=(',',':'))

        return sorted([(k,v) for k,v in data.items()])

    #开始计算签名
    def sign(self,unsigned_string):
        key = self.app_private_key
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(SHA256.new(unsigned_string))
        #base64编码,转换为unicode编码并移除回车
        sign = encodebytes(signature).decode("utf-8").replace("\n","")

        return sign

    #验证支付宝返回的url中sign字段与阿里秘钥解码的是否一样
    def _verify(self,raw_content,signature):
        #开始计算签名
        key = self.alipay_public_key
        signer = PKCS1_v1_5.new(key)
        digest = SHA256.new()
        digest.update(raw_content.encode("utf-8"))

        if signer.verify(digest,decodebytes(signature.encode("utf-8"))):
            return True

        return False

    def verify(self,data,signature):
        if "sign_type" in data:
            sign_type = data.pop("sign_type")

        #排序后的字符串
        unsigned_items = self.ordered_data(data)
        message = "&".join("{}={}".format(k,v) for k,v in unsigned_items)

        return self._verify(message,signature)

if __name__ == "__main__":

    # return_url = "http://www.skycobo.com/?charset=utf-8&out_trade_no=201809201889&method=alipay.trade.page.pay.return&total_amount=2.00&sign=pD7fDYbicvsAq0Kq6tGa%2FouEYYwgwvXk823PxFJYnMlFbuueW5lcpJdEHnwASeguq8wmsEShKw%2BeHa0nUPUjmY%2F5KPFkWmDsUdYamgsHzKCB5C6l40AzrXZZiu9Nlc84DTWm1afdOcCnRhXn2ScDklWaQ5bvDGp3wz7feXGBYv1XyKHw%2FqDjsBFR0OS6FjYvXXxr9iAhJXXOUPCESL8xRytuSVPY%2B0L%2FcZiUAVFxuunAZ%2Ff%2F%2Bf%2B49NF%2Ft6Z7eJCSqPJ5g7hDwNBdRx%2BQ7%2FiDEjC1V8t7KCFpmvdvcJBSBG6PFR8UdGil67%2BzYDosYoxyPOw4M%2BLEqIk1hE5Z9hwa6A%3D%3D&trade_no=2018092021001004560500302075&auth_app_id=2016092100564248&version=1.0&app_id=2016092100564248&sign_type=RSA2&seller_id=2088102176651605&timestamp=2018-09-20+19%3A40%3A19"
    # o = urlparse(return_url)
    # query = parse_qs(o.query)
    # processed_query = {}
    # ali_sign = query.pop("sign")[0]

    alipay = AliPay(
        app_id="2016092100564248",
        app_notify_url="http://127.0.0.1:8000/alipay/return/",
        app_private_key_path="../trade/keys/private_2048.txt",
        alipay_public_key_path="../trade/keys/alipay_2048.txt",
        debug=True,
        return_url="http://127.0.0.1:8000/alipay/return/"
    )
    #
    # for k,v in query.items():
    #     processed_query[k] = v[0]
    #
    # print(alipay.verify(processed_query,ali_sign))

    url = alipay.direct_pay(
        subject="测试订单",
        out_trade_no="20182900099999",
        total_amount=2,
        return_url="http://127.0.0.1:8000/alipay/return/"
    )
    return_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

    print(return_url)
