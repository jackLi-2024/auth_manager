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
import logging
import module
import importlib

# from module.test.api import Search
# o = importlib.import_module("module.%s.api" % ("test"))
# eval("from module.%s.api import Search as search_%s" % ("test", "test"))

try:
    reload(sys)
    sys.setdefaultencoding("utf8")
except:
    pass

functions = os.listdir("module")
search_list = []
operate_list = []
for f in functions:
    if "py" in f or "pyc" in f:
        continue
    try:
        o = importlib.import_module("module.%s.api" % (f))
    except Exception as e:
        logging.exception(str(e))
        continue
    try:
        search_list.append(o.Search)
    except Exception as e:
        logging.exception(str(e))
    try:
        operate_list.append(o.Operate)
    except Exception as e:
        logging.exception(str(e))


class Query(*search_list):
    class Meta:
        description = '查询类接口'
        name = "SearchApi"

    pass


class Mutate(*operate_list):
    class Meta:
        description = '修改操作类接口'
        name = "OperateApi"

    pass


try:
    schema = graphene.Schema(Query, mutation=Mutate, auto_camelcase=False)
except:
    schema = graphene.Schema(Query, mutation=Query, auto_camelcase=False)