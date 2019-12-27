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

from module.auth_token import model
from module.auth_token import deal
from module.auth_token import arguments


class Search(graphene.ObjectType):
    generate_token = graphene.Field(model.GenerateTokenReturn,
                                    condition=arguments.GenerateTokenArgument(required=True),
                                    description="生成token")

    fresh_token = graphene.Field(model.FreshTokenReturn,
                                 condition=arguments.FreshTokenArgument(required=True),
                                 description="刷新token")

    validate_token = graphene.Field(model.ValidateTokenReturn,
                                    condition=arguments.ValidateTokenArgument(required=True),
                                    description="验证token并返回token信息")

    logout_token = graphene.Field(model.LogoutTokenReturn,
                                  condition=arguments.LogoutTokenArgument(required=True),
                                  description="注销token")

    def resolve_generate_token(self, info, **kwargs):
        return deal.GenerateTokenDeal(**kwargs).run()

    def resolve_fresh_token(self, info, **kwargs):
        return deal.FreshTokenDeal(**kwargs).run()

    def resolve_validate_token(self, info, **kwargs):
        return deal.ValidateTokenDeal(**kwargs).run()

    def resolve_logout_token(self, info, **kwargs):
        return deal.LogoutTokenDeal(**kwargs).run()
