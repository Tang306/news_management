import re
import json
import time
import random
import datetime
import decimal
import consts
import jwt
from account.models import User
from django.conf import settings


def format_return(code, msg='', data=None, change_none=False, lang='zh'):
    """格式化返回"""
    temp = data if data is not None else {}

    # 是否要将None变成""
    if change_none:
        temp = json.loads(json.dumps(temp).replace('null', '""'))
    return code, msg or consts.ERROR_DICT.get(code, ''), temp


def format_date_time(datetime):
    '''格式时间'''
    return datetime.strftime('%Y-%m-%d %H:%M:%S') if datetime else ""


def format_date(datetime):
    '''格式时间'''
    return datetime.strftime('%Y-%m-%d') if datetime else ""


class Validator(object):
    """通用参数验证器"""

    def validate_digit(self, number):
        # 验数字格式
        return True if re.match(
            r'^[-+]?(([0-9]+)([.]([0-9]+))?|([.]([0-9]+))?)$', number) else False

    def validate_password(self, password):
        # 密码 6-20 位
        # return True if re.match(r'^([a-zA-Z0-9!@#$%^&*()_?<>{}]){8,16}$',
        # password) else False
        return True if re.match(r'^\S{6,20}$', password) else False

    def validate_date_time(self, date_str):
        # 验证日期（精确到秒）字符串
        if not isinstance(date_str, datetime.datetime):
            try:
                datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            except BaseException:
                return False
        return True

    def validate_date(self, date_str):
        # 验证日期（精确到天）字符串
        if not isinstance(date_str, datetime.datetime):
            try:
                datetime.datetime.strptime(date_str, '%Y-%m-%d')
            except BaseException:
                return False
        return True

    def generate_token(self, user_id, expiration_time):
        # 构造header
        headers = {
            'typ': 'jwt',
            'alg': 'HS256'
        }
        # 构造payload
        payload = {
            'user_id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=expiration_time)  # 超时时间
        }
        token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm="HS256", headers=headers).decode('utf-8')
        return token

    @staticmethod
    def get_user_by_id(id):
        """
        查询用户
        """
        return User.objects.filter(id=id).exclude(state=-2).first()