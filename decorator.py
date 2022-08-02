from django.http import HttpResponse, JsonResponse

import utils
import jwt
from utils import format_return
from utils import Validator
from functools import wraps
import inspect, cache, consts
# from account.interface import UserBase


def common_ajax_response(func):
    """
    @note: 通用的ajax返回值格式化，格式为：dict(code=0, msg='', data={})
    """

    def _decorator(request, *args, **kwargs):
        result = func(request, *args, **kwargs)
        if isinstance(result, HttpResponse):
            return result
        code, msg, data = result

        r = dict(code=code, msg=msg, data=data)
        response = JsonResponse(r)
        # response['Access-Control-Allow-Origin'] = '*'
        return response

    return _decorator

def require_role(role=[]):
    """
    定义权限
    """
    def check_promission(func):
        """
        后台权限验证
        """
        def _decorator(request, *args, **kwargs):
            token = request.META.get('HTTP_AUTHORIZATION')
            if not token:
                return format_return(11006, "没有token")
            try:
                result = jwt.decode(token, consts.SECRET_KEY, algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                return format_return(11008, "token已过期")
            except jwt.InvalidTokenError:
                return format_return(11009, "无效的token")
            except Exception as e:
                return format_return(11010, 'token认证失败请登录')
            user_id = result['user_id']
            user = utils.Validator.get_user_by_id(user_id)
            if not user:
                return format_return(11004, "用户不存在")
            if user.state not in role:
                return format_return(11007, "无权限打开")
            request.user_id = user_id
            return func(request, *args, **kwargs)
        return _decorator
    return check_promission


def validate_params(func):
    """
    @note: 通用的参数校验，第一步非空校验
    """

    def _decorator(*args, **kwargs):

        def _get_param_items(func, args, kwargs):

            parameters = inspect.signature(func).parameters
            arg_keys = tuple(parameters.keys())
            vparams = [k for k, v in parameters.items() if k == str(v)]

            param_items = []
            # collect args   *args 传入的参数以及对应的函数参数注解
            for i, value in enumerate(args):
                _key = arg_keys[i]
                if _key in vparams:
                    param_items.append([_key, value])

            # collect kwargs  **kwargs 传入的参数以及对应的函数参数注解
            for arg_name, value in kwargs.items():
                if arg_name in vparams:
                    param_items.append([arg_name, value])

            return param_items

        check_list = _get_param_items(func, args, kwargs)
        # 不能为空检测
        for item in check_list:
            if item[1] is None:
                return format_return(99901)

        return func(*args, **kwargs)

    return _decorator

