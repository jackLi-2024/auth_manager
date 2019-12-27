#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:Lijiacai
Email:1050518702@qq.com
===========================================
CopyRight@JackLee.com
===========================================
"""

import os
import sys
import json
import graphene

try:
    reload(sys)
    sys.setdefaultencoding("utf8")
except:
    pass


##########################################################
# 下面是返回模型
##########################################################

class LogoutTokenReturn(graphene.ObjectType):
    class Meta:
        description = "返回值"

    action = graphene.Boolean(description="操作执行 true:操作成功  false:操作失败")


class GenerateTokenReturn(graphene.ObjectType):
    class Meta:
        description = "返回值"

    access_token = graphene.String(description="访问token")
    fresh_token = graphene.String(description="刷新token")


class FreshTokenReturn(graphene.ObjectType):
    class Meta:
        description = "返回值"

    access_token = graphene.String(description="访问token")
    fresh_token = graphene.String(description="刷新token")


class ValidateTokenReturn(graphene.ObjectType):
    class Meta:
        description = "返回值"

    dec_data = graphene.String(description="解密后的json字符串")
    user_id = graphene.String(description="同一平台用户唯一标识")
