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

cur_dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append("%s/../../" % cur_dir)

from module.模板 import model
from module.模板 import deal
from module.模板 import arguments


class Search(graphene.ObjectType):
    pass
