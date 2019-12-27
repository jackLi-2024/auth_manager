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

try:
    reload(sys)
    sys.setdefaultencoding("utf8")
except:
    pass

import graphene


#################

class GenerateTokenArgument(graphene.InputObjectType):
    class Meta:
        description = '请求参数'

    enc_data = graphene.String(description="需要加密的json字符串", required=True)
    user_id = graphene.String(description="同一平台用户唯一标识", required=True)
    app_id = graphene.String(description="应用平台id", required=True)


class FreshTokenArgument(graphene.InputObjectType):
    class Meta:
        description = '请求参数'

    fresh_token = graphene.String(description="刷新的token", required=True)


class ValidateTokenArgument(graphene.InputObjectType):
    class Meta:
        description = "请求参数"

    token = graphene.String(description="验证的token", required=True)


class LogoutTokenArgument(graphene.InputObjectType):
    class Meta:
        description = "请求参数"

    user_id = graphene.String(description="同一平台用户唯一标识", required=True)
    app_id = graphene.String(description="应用平台id", required=True)

#########################
