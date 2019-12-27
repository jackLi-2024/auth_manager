#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:Lijiacai
Email:1050518702@qq.com
===========================================
CopyRight@JackLee.com
===========================================
"""
import datetime
import os
import sys
import json
import time

try:
    reload(sys)
    sys.setdefaultencoding("utf8")
except:
    pass

from LJC_utils.utils import TokenCrud


class GenerateTokenDeal(TokenCrud):
    def deal(self):
        enc_data = self.arguments.get("enc_data")
        user_id = self.arguments.get("user_id")
        app_id = self.arguments.get("app_id")
        secret = self.random_string()
        fresh_token = self.token_encode(enc_data, secret, user_id, app_id=app_id)
        access_token = self.token_encode(enc_data, secret, user_id, app_id=app_id)
        access_key = "access_appid:{}_userid:{}_token:{}".format(app_id, user_id, access_token)
        fresh_key = "fresh_appid:{}_userid:{}_token:{}".format(app_id, user_id, fresh_token)
        names = self.keys(pattern=r"*appid:{}_userid:{}_token*".format(app_id, user_id))
        if names:
            self.delete(names)
        self.set(access_key, secret, ex=self.access_expire)
        self.set(fresh_key, secret, ex=self.fresh_expire)
        return {"fresh_token": fresh_token, "access_token": access_token}


class FreshTokenDeal(TokenCrud):
    def deal(self):
        fresh_token = self.arguments.get("fresh_token")
        names = self.keys(pattern=r"*token:{}".format(fresh_token))
        if names:
            property_list = names[0].decode("utf8").split("_")
            app_id = property_list[1]
            user_id = property_list[2]
            SECRET = str(self.get(names[0].decode("utf8")).decode("utf8"))
            token_info = self.token_decode(fresh_token, SECRET)
            names = self.keys(pattern=r"access_{}_{}_token*".format(app_id, user_id))
            if names:
                self.delete(names)
            secret = self.random_string()
            enc_data = token_info.get("data")
            access_token = self.token_encode(enc_data, secret, user_id, app_id=app_id)
            access_key = "access_{}_{}_token:{}".format(app_id, user_id, access_token)
            self.set(access_key, secret, ex=self.access_expire)
            return {"fresh_token": fresh_token, "access_token": access_token}
        else:
            raise Exception("该token已失效")


class ValidateTokenDeal(TokenCrud):
    def deal(self):
        token = self.arguments.get("token")
        names = self.keys(pattern=r"*token:{}".format(token))
        if names:
            property_list = names[0].decode("utf8").split("_")
            SECRET = str(self.get(names[0].decode("utf8")).decode("utf8"))
            token_info = self.token_decode(token, SECRET)
            return {"dec_data": token_info.get("data"), "user_id": token_info.get("user_id")}
        else:
            raise Exception("该token已失效")


class LogoutTokenDeal(TokenCrud):
    def deal(self):
        user_id = self.arguments.get("user_id")
        app_id = self.arguments.get("app_id")
        names = self.keys(pattern=r"*appid:{}_userid:{}_token*".format(app_id, user_id))
        if names:
            self.delete(names)
        else:
            raise Exception("参数错误")

        return {"action": True}
