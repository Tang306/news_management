import requests

import logging

import consts, debug, cache, decorator


def fetch(url, data={}, headers={}, timeout=5):
    try:
        logging.warning('url--> %s' % url)
        logging.warning('data--> %s' % data)
        result = requests.post(url, headers=headers, data=data, timeout=timeout).json()
        logging.warning('response--> %s' % result)
        return result
    except Exception as e:
        debug.get_debug_detail(e)
        return {'code': 99904, 'data': {}, 'msg': ''}


def add_slow_request(data):
    '''添加慢请求'''
    url = '%s/system/api/monitor/add_slow_request'
    return fetch(url=url, headers={}, data=data)


def add_sys_error(data):
    '''添加错误请求'''
    url = '%s/system/api/monitor/add_sys_error'
    return fetch(url=url, headers={}, data=data)


def add_request_log(data={}):
    '''添加请求日志'''
    url = '%s/system/api/monitor/add_request_log'
    return fetch(url=url, headers={}, data=data)


def add_operate_log(data={}):
    '''添加操作日志'''
    url = '%s/system/api/monitor/add_operate_log'
    return fetch(url=url, headers={}, data=data)


def get_user_profile(username):
    '''获取个人信息'''
    cache_obj = cache.Cache(config=cache.CACHE_ACCOUNT)
    cache_key = 'user_profile_%s' % username
    profile = cache_obj.get(cache_key)

    # 如果命中缓存
    if profile:
        return profile
    else:
        url = '%s/profile/api/get_user_profile'
        return fetch(url=url, headers={"USERNAME": username})['data']


