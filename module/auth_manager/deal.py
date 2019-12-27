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

from LJC_utils.utils import AuthManger


class AddPermissionForUser(AuthManger):
    def deal(self):
        sub = self.arguments.get("subject")
        obj = self.arguments.get("resource")
        act = self.arguments.get("action")
        return {"status": self.add_permission_for_user(sub, obj, act)}


class AddPermissionForGroup(AuthManger):
    def deal(self):
        sub = self.arguments.get("subject")
        obj = self.arguments.get("resource")
        act = self.arguments.get("action")
        return {"status": self.add_permission_for_group(sub, obj, act)}


class DeleteRole(AuthManger):
    def deal(self):
        sub = self.arguments.get("subject")
        self.delete_role(sub)
        return {"status": True}


class AddGroupForUser(AuthManger):
    def deal(self):
        sub = self.arguments.get("subject")
        group_name = self.arguments.get("group_name")
        return {"status": self.add_group_for_user(sub, group_name)}


class RemoveUserForGroup(AuthManger):
    def deal(self):
        sub = self.arguments.get("subject")
        group_name = self.arguments.get("group_name")
        return {"status": self.remove_user_for_group(sub, group_name)}


class RemovePermission(AuthManger):
    def deal(self):
        sub = self.arguments.get("subject")
        obj = self.arguments.get("resource")
        act = self.arguments.get("action")
        return {"status": self.remove_permission(sub, obj, act)}


class SearchGroupForUser(AuthManger):
    def deal(self):
        sub = self.arguments.get("subject")
        result = self.search_group_for_user(sub)
        out = []
        for i in result:
            out.append({"group": i[1]})
        return {"rows": out}


class SearchPermissionForGroup(AuthManger):
    def deal(self):
        group_name = self.arguments.get("group_name")
        out = []
        result = self.search_permission_for_group(group_name)
        for i in result:
            out.append({"group": i[0], "resource": i[1], "action": i[2]})
        return {"rows": out}


class SearchPermissionForUser(AuthManger):
    def deal(self):
        sub = self.arguments.get("subject")
        result = self.search_permission_for_user(sub).get(sub, [])
        out = []
        for i in result:
            out.append({"action": i[1], "resource": i[0], "user": sub})
        return {"rows": out}


class SearchGroups(AuthManger):
    def deal(self):
        result = self.search_groups()
        out = []
        for i in result:
            out.append({"group": i})
        return {"rows": out}


class IsPermission(AuthManger):
    def deal(self):
        sub = self.arguments.get("subject")
        obj = self.arguments.get("resource")
        act = self.arguments.get("action")
        return {"status": self.is_permission(sub, obj, act)}
