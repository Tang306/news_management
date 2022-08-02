import datetime
import json
import os
import time
import hashlib
import utils

from django.conf import settings
from django.utils.crypto import constant_time_compare
from django.utils.encoding import smart_str
from django.db import transaction
from django.http import JsonResponse
from utils import format_return
from decorator import validate_params
from account.models import User
import consts


class MD5PasswordHasher(object):

    @staticmethod
    def salt():
        return consts.SECRET_KEY

    def encode(self, password):
        return hashlib.md5((self.salt() + password).encode('utf-8')).hexdigest()

    def make_password(self, password):
        return self.encode(smart_str(password))

    def check_password(self, password, encoded):
        return constant_time_compare(self.encode(smart_str(password)), encoded)


class UserBase(object):
    """
    用户接口
    """
    expiration_time = 60 * 24  # 过期时间

    def __init__(self):
        self.hasher = MD5PasswordHasher()

    def _set_password(self, raw_password):
        password = self.hasher.make_password(raw_password)
        return password

    def _check_password(self, raw_password, password):
        return self.hasher.check_password(raw_password, password)

    def set_user_password(self, user, password):
        user.password = self._set_password(password)
        user.save()
        return utils.format_return({"code": 0, "msg": "成功"})

    @validate_params
    def admin_register(self, nickname, username, password):
        """
        注册管理员
        """
        if len(username) < 4:
            return format_return(11001, msg="手机号不能低于4位")
        if not username.isdigit():
            return format_return(11001, msg="手机号必须为纯数字")
        if User.objects.filter(username=username, state=1).count():
            return format_return(11013, "手机号已注册")
        if not utils.Validator().validate_password(password):
            return format_return(11002, "密码不合法")

        user = User.objects.create(
            username=username,
            nickname=nickname,
            password=self._set_password(password),
            state=1,
        )
        data = {"user_id": user.id, "nickname": user.nickname, "state": user.state}
        return format_return(0, data=data)

    @validate_params
    def register(self, nickname, username, password, state):
        """
        注册普通用户
        """

        if len(username) < 4:
            return format_return(11000, msg='手机号不能低于4位')
        if not username.isdigit():
            return format_return(11001, msg="手机号必须为纯数字")
        if User.objects.filter(username=username).count():
            return format_return(11005, "手机号已注册")
        if not utils.Validator().validate_password(password):
            return format_return(11002, "密码不合法")

        user = User.objects.create(
            username=username,
            nickname=nickname,
            password=self._set_password(password),
            state=state,
        )
        data = {"create_time": user.create_time, "user_id": user.id, "nickname": user.nickname, "username": user.username, "state": user.state}
        return format_return(0, data=data)

    @validate_params
    def login(self, username, password):
        """
        登录
        """
        if not User.objects.filter(username=username).exclude(state__lte=-1):
            return format_return(11004, "用户不存在")
        if not utils.Validator().validate_password(password):
            return format_return(11002, "密码格式错误")
        user = User.objects.filter(username=username, password=self._set_password(password)).exclude(state__lte=-1)
        if user:
            user = user[0]
            user.last_login = datetime.datetime.now()
            user.save()
            user_id = user.id
            token = utils.Validator().generate_token(user_id, UserBase.expiration_time)
            data = {"last_login": user.last_login, "user_id": user.id, "username": user.username, "nickname": user.nickname, "state": user.state, "token": token}
            return format_return(0, data=data)
        else:
            return format_return(11003, "密码不正确")

    @validate_params
    def change_password(self, user_id, old_password, new_password):
        """
        修改密码
        """
        if not utils.Validator().validate_password(new_password):
            return format_return(11002, "密码格式错误")

        user = User.objects.filter(id=user_id, password=self._set_password(old_password)).exclude(state__lte=-1)
        if not user:
            return format_return(11003, "密码不正确")
        user = user[0]
        user.password = self._set_password(new_password)
        user.save()
        data = {"user_id": user.id, "nickname": user.nickname, "username": user.username, "state": user.state}
        return format_return(0, data=data)

    def reset_password_by_user_id(self, user_id):
        """
        密码初始化
        """
        user = self.get_user_by_id(user_id)
        if not user:
            return format_return(11004, "用户不存在")
        suffix = user.username[-4:]
        new_password = 'test_' + suffix
        user.password = self._set_password(new_password)
        user.save()
        data = {"user_id": user.id, "nickname": user.nickname, "state": user.state}
        return format_return(0, data=data)

    def edit_user_information(self, user_id, nickname, username, password, state):
        """
        编辑用户权限
        """
        user = self.get_user_by_id(user_id)
        if not user:
            return format_return(11004, "用户不存在")
        if not utils.Validator().validate_password(password):
            return format_return(11002, "密码不合法")
        user.password = self._set_password(password)
        user.nickname = nickname
        user.username = username
        user.state = state
        user.save()
        data = {"user_id": user.id, "nickname": user.nickname, "username": user.username, "state": user.state}
        return format_return(0, data=data)

    def del_user_information(self, user_id):
        """
        删除用户
        """
        user = self.get_user_by_id(user_id)
        user.state = -2
        user.save()
        data = {"user_id": user.id, "nickname": user.nickname, "state": user.state}
        return format_return(0, data=data)

    @staticmethod
    def get_user_by_id(id):
        """
        查询用户
        """
        return User.objects.filter(id=id).exclude(state=-2).first()

    def get_user_information(self, nickname, state):
        """
        筛选用户
        """
        users_list = User.objects.exclude(state=-2).exclude(state=1).order_by('id')
        if nickname:
            users_list = users_list.filter(nickname=nickname)
        if state:
            if int(state) == -1:  # 禁用
                users_list = users_list.filter(state=state)
            else:  # 启用
                users_list = users_list.filter(state__gte=2)
        return users_list




