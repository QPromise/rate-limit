# coding=utf-8
import time
from functools import wraps
from flask import make_response


def tokenbucket(*args, **kwargs):
    """
    令牌桶算法

    :param args:
    :param kwargs:
    :return:
    """
    def decorator(func):
        token = kwargs.get('token', 1)
        rate = kwargs.get('rate', None)
        default = kwargs.get('default', None)
        token_info = {}

        @wraps(func)
        def _tokenbucket(*args, **kwargs):
            if rate is None or default is None or token > default:
                return func()

            current_count = token_info.get('count', None)
            curr_time = time.time()
            if current_count is None:
                current_count = default
                token_info['last_time'] = curr_time

            last_time = token_info.get('last_time')
            all_count = current_count + (curr_time - last_time) * rate
            if all_count > default:
                all_count = default

            if token > all_count:
                res = make_response(u'流量限制')
                return res, 503
            else:
                token_info['count'] = all_count - token
                token_info['last_time'] = curr_time
                return func(*args, **kwargs)

        return _tokenbucket
    return decorator

