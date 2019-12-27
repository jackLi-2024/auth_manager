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
import random
import sys
import json
import time
import redis
import pymysql
import configparser
import jwt
import hashlib
import casbin_sqlalchemy_adapter
import casbin
import functools
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool


def get_config(conf_file="./configure/main.conf"):
    config = configparser.ConfigParser()
    config.read(conf_file)
    info = config._sections
    return info


class RedisDB():
    def __init__(self, host='localhost', port=6379,
                 db=0, password=None, socket_timeout=None,
                 socket_connect_timeout=None,
                 socket_keepalive=None, socket_keepalive_options=None,
                 connection_pool=None, unix_socket_path=None,
                 encoding='utf-8', encoding_errors='strict',
                 charset=None, errors=None,
                 decode_responses=False, retry_on_timeout=False,
                 ssl=False, ssl_keyfile=None, ssl_certfile=None,
                 ssl_cert_reqs='required', ssl_ca_certs=None,
                 max_connections=None):
        self.client = redis.Redis(host=host, port=port,
                                  db=db, password=password, socket_timeout=socket_timeout,
                                  socket_connect_timeout=socket_connect_timeout,
                                  socket_keepalive=socket_keepalive, socket_keepalive_options=socket_keepalive_options,
                                  connection_pool=connection_pool, unix_socket_path=unix_socket_path,
                                  encoding=encoding, encoding_errors=encoding_errors,
                                  charset=charset, errors=errors,
                                  decode_responses=decode_responses, retry_on_timeout=retry_on_timeout,
                                  ssl=ssl, ssl_keyfile=ssl_keyfile, ssl_certfile=ssl_certfile,
                                  ssl_cert_reqs=ssl_cert_reqs, ssl_ca_certs=ssl_ca_certs,
                                  max_connections=max_connections)

    def get_client(self):
        return self.client

    def __del__(self):
        self.close()

    def close(self):
        try:
            del self.client
        except:
            pass


config = get_config()
engin = create_engine(config.get("orm").get("host"), poolclass=NullPool, echo=False)


#######


class TokenCrud():
    def __init__(self, args=None, **kwargs):
        cont = config.get("redis", {})
        host = cont.get("host")
        port = int(cont.get("port", 6379))
        db = int(cont.get("db", 0))
        password = cont.get("password")
        token_expire = config.get("token", {})
        self.access_expire = int(token_expire.get("access_expire", 180))
        self.fresh_expire = int(token_expire.get("fresh_expire", 24 * 60 * 60 * 1))
        self.client = RedisDB(host=host, port=port, password=password, db=db).client
        self.arguments = kwargs.get("arguments", {})
        if not self.arguments:
            self.arguments = kwargs.get("condition", {})
        self.kwargs = kwargs
        self.args = args

    def set(self, name, value, ex=None, px=None, nx=False, xx=False):
        self.client.set(name=name, value=value, ex=ex, px=px, nx=nx, xx=xx)

    def get(self, name):
        return self.client.get(name=name)

    def delete(self, names: list):
        self.client.delete(*names)

    def keys(self, pattern: str):
        return self.client.keys(pattern=pattern)

    def token_encode(self, enc_json_data, SECRET, user_id, app_id):
        payload = {
            "data": enc_json_data,
            "user_id": user_id,
            "app_id": app_id,
            "timestamp": time.time() + random.randint(1, 10000)
        }
        return self.__token__(payload=payload, SECRET=SECRET)

    def __token__(self, payload: dict, SECRET: str):
        token = jwt.encode(payload, SECRET, algorithm='HS256')
        return token.decode()

    def token_decode(self, token, SECRET):
        decoded = jwt.decode(token.encode(), SECRET, algorithms='HS256')
        return decoded

    def random_string(self):
        m = hashlib.md5()
        m.update(str(time.time()).encode('utf-8'))
        return m.hexdigest()

    def deal(self):
        pass

    def run(self):
        return self.deal()


class AuthManger():
    path = "./configure/model.conf"

    def __init__(self, args=None, **kwargs):
        adapter = casbin_sqlalchemy_adapter.Adapter(engin)
        self.e = casbin.Enforcer(self.path, adapter, True)
        self.arguments = kwargs.get("arguments", {})
        if not self.arguments:
            self.arguments = kwargs.get("condition", {})
        self.kwargs = kwargs
        self.args = args

    def add_permission_for_user(self, sub: str, obj: str, act: str):  # 添加单个用户权限
        """
        :param sub: 主体  例如 用户 alice
        :param obj: 资源  例如 url 接口或者其他资源
        :param act: 行为 例如 get post等请求行为
        :return: bool True or false 表示添加是否成功
        """
        res = self.e.add_permission_for_user(sub, obj, act)
        return res

    def remove_permission(self, sub: str, obj: str, act: str):

        de = self.e.delete_permission_for_user(sub, obj, act)
        return de

    def delete_role(self, sub: str):
        return self.e.delete_role(sub)

    def add_group_for_user(self, sub: str, group_name: str):  # 添加组
        """
        :param sub: str 主体
        :param group_name: str 组名
        :return: bool
        """
        return self.e.add_grouping_policy([sub, group_name])

    def add_permission_for_group(self, sub: str, obj: str, act: str):  # 添加组权限
        return self.e.add_named_policy('p', [sub, obj, act])

    def remove_user_for_group(self, sub: str, group_name: str):  # 删除组内用户

        return self.e.remove_grouping_policy([sub, group_name])

    def search_groups(self):  # 获取所有用户组
        return self.e.get_all_named_roles('g')

    def search_group_for_user(self, sub: str):  # 查询某个用户的组
        """
        :param name: str sub 比如用户
        :return: list  [sub group] 用户 和 组名
        """
        return self.e.get_filtered_grouping_policy(0, sub)

    def search_permission_for_group(self, group_name: str):  # 查询某个组的所有权限
        return self.e.get_filtered_policy(0, group_name)

    def search_permission_for_user(self, sub: str):  # 查询某个用户的所有权限
        dic = {sub: []}
        pers = self.search_group_for_user(sub)
        for per in pers:
            if len(per) != 2:
                raise ValueError(f'获取用户权限失败 need 2 got {len(per)}')
            group_name = per[-1]
            g_pers = self.search_permission_for_group(group_name)
            for gp in g_pers:
                if len(gp) != 3:
                    raise ValueError(f'获取组权限失败 need 3 got {len(gp)}')
                dic[sub].append(gp[1:])
        return dic

    def is_permission(self, sub: str, obj: str, act: str):  # 判断权限
        return self.e.enforce(sub, obj, act)

    def run(self):
        return self.deal()

    def deal(self):
        pass


if __name__ == '__main__':
    # get_config()
    a = TokenCrud().token_decode(
        token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRhIjpudWxsLCJ1c2VyX2lkIjoiMTIzIiwiYXBwX2lkIjoiMSIsInRpbWVzdGFtcCI6MTU3NzI2NTE1Mi41MDI0NDUyfQ.yCdGxT0XCAlpy4MyJKk44YcERN8eP3XbA3YX-jUbuBg",
        SECRET=b"668657345a6d611161d738c1302ad4a7")
    print(a)
