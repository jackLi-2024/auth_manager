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

from module.auth_manager import model
from module.auth_manager import deal
from module.auth_manager import arguments


class Search(graphene.ObjectType):
    add_permission_for_user = graphene.Field(model.OperateReturn,
                                             condition=arguments.SubObjActArgument(required=True),
                                             description="为用户加权限")
    add_permission_for_group = graphene.Field(model.OperateReturn,
                                              condition=arguments.SubObjActArgument(required=True),
                                              description="为组加权限")
    delete_role = graphene.Field(model.OperateReturn,
                                 condition=arguments.SubArgument(required=True),
                                 description="删除角色:用户/组")
    add_group_for_user = graphene.Field(model.OperateReturn,
                                        condition=arguments.SubGroupArgument(required=True),
                                        description="为用户添加组,使用户拥有组的权限")

    remove_user_for_group = graphene.Field(model.OperateReturn,
                                           condition=arguments.SubGroupArgument(required=True),
                                           description="为组移除用户，使用户不再拥有组的权限")

    remove_permission = graphene.Field(model.OperateReturn,
                                       condition=arguments.SubObjActArgument(required=True),
                                       description="移除权限:用户/组")

    search_group_for_user = graphene.Field(model.SearchReturn,
                                           condition=arguments.SubArgument(required=True),
                                           description="为用户查询组")

    search_permission_for_group = graphene.Field(model.SearchReturn,
                                                 condition=arguments.GroupArgument(required=True),
                                                 description="查询某组所有权限")
    search_permission_for_user = graphene.Field(model.SearchReturn,
                                                condition=arguments.SubArgument(required=True),
                                                description="查询某用户所有权限")
    search_groups = graphene.Field(model.SearchReturn,
                                   description="查询所有组")
    is_permission = graphene.Field(model.OperateReturn,
                                   condition=arguments.SubObjActArgument(required=True),
                                   description="判断权限是否存在: 用户/组")

    def resolve_add_permission_for_user(self, info, **kwargs):
        return deal.AddPermissionForUser(**kwargs).run()

    def resolve_add_permission_for_group(self, info, **kwargs):
        return deal.AddPermissionForGroup(**kwargs).run()

    def resolve_delete_role(self, info, **kwargs):
        return deal.DeleteRole(**kwargs).run()

    def resolve_add_group_for_user(self, info, **kwargs):
        return deal.AddGroupForUser(**kwargs).run()

    def resolve_remove_user_for_group(self, info, **kwargs):
        return deal.RemoveUserForGroup(**kwargs).run()

    def resolve_remove_permission(self, info, **kwargs):
        return deal.RemovePermission(**kwargs).run()

    def resolve_search_group_for_user(self, info, **kwargs):
        return deal.SearchGroupForUser(**kwargs).run()

    def resolve_search_permission_for_group(self, info, **kwargs):
        return deal.SearchPermissionForGroup(**kwargs).run()

    def resolve_search_permission_for_user(self, info, **kwargs):
        return deal.SearchPermissionForUser(**kwargs).run()

    def resolve_search_groups(self, info, **kwargs):
        return deal.SearchGroups(**kwargs).run()

    def resolve_is_permission(self, info, **kwargs):
        return deal.IsPermission(**kwargs).run()
