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

class SubObjActArgument(graphene.InputObjectType):
    class Meta:
        description = '请求参数'

    subject = graphene.String(description="权限主体可以是用户或者组", required=True)
    resource = graphene.String(description="权限资源可以是url等", required=True)
    action = graphene.String(description="权限行为", required=True)


class SubArgument(graphene.InputObjectType):
    class Meta:
        description = '请求参数'

    subject = graphene.String(description="权限主体可以是用户或者组", required=True)


class GroupArgument(graphene.InputObjectType):
    class Meta:
        description = '请求参数'

    group_name = graphene.String(description="组名称", required=True)


class SubGroupArgument(graphene.InputObjectType):
    class Meta:
        description = '请求参数'

    subject = graphene.String(description="权限主体可以是用户或者组", required=True)
    group_name = graphene.String(description="组名称", required=True)

#########################
