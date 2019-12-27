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


class Model(graphene.ObjectType):
    name = graphene.String(description="测试样例")


##########################################################
# 下面是返回模型
##########################################################

class Return(graphene.ObjectType):
    class Meta:
        description = "返回值"
