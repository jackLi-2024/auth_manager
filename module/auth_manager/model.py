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


class CasbinModel(graphene.ObjectType):
    user = graphene.String(description="用户")
    group = graphene.String(description="组")
    resource = graphene.String(description="资源")
    action = graphene.String(description="资源权限")


##########################################################
# 下面是返回模型
##########################################################

class OperateReturn(graphene.ObjectType):
    class Meta:
        description = "返回值"

    status = graphene.Boolean(description="操作执行 true:操作成功  false:操作失败")


class SearchReturn(graphene.ObjectType):
    class Meta:
        description = "返回值"

    rows = graphene.List(CasbinModel, description="查询结果列表")
