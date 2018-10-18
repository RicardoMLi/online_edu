# -*- coding: UTF-8 -*-

import logging

from utils.yuntongxun.CCPRestSDK import REST

#主帐号
accountSid= '8a216da863cde6f90163f32977671135';

#主帐号Token
accountToken= 'eedd4b8d094b40cdaf6386085584131f';

#应用Id
appId='8a216da863cde6f90163f32977ce113b';

#请求地址，格式如下，不需要写http://
serverIP='app.cloopen.com';

#请求端口 
serverPort='8883';

#REST版本号
softVersion='2013-12-26';

class CCP(object):

    def __init__(self):
        self.rest = REST(serverIP, serverPort, softVersion)
        self.rest.setAccount(accountSid, accountToken)
        self.rest.setAppId(appId)

    @staticmethod
    def instance():
        if not hasattr(CCP, "_instance"):
            CCP._instance = CCP()
        return CCP._instance

    def sendTemplateSMS(self, to, datas, tempId):
        try:
            result = self.rest.sendTemplateSMS(to, datas, tempId)
        except Exception as e:
            logging.error(e)
            raise e

        if result.get("statusCode") == "000000":
            return True
        else:
            return False

ccp = CCP.instance()

if __name__ == "__main__":
    ccp = CCP.instance()
    ccp.sendTemplateSMS("13537144941", ["1234", 5], 1)