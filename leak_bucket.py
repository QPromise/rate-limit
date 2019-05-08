# coding=utf-8
import time
from functools import wraps
from flask import make_response


def leakbucket(*args, **kwargs):
    """
    漏桶算法

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
        def _leakbucket(*args, **kwargs):
            if rate is None or default is None or token > default:
                return func()

            current_count = token_info.get('count', None)
            curr_time = time.time()
            if current_count is None:
                current_count = default - rate    # 如果初始化一个满的桶,第一个请求就会被拒绝
                token_info['last_time'] = curr_time

            last_time = token_info.get('last_time')
            all_count = current_count - (curr_time - last_time) * rate
            if all_count < 0:
                all_count = 0

            if all_count + token > default:
                token_info['count'] = all_count
                token_info['last_time'] = curr_time
                res = make_response(u'流量限制')
                return res, 503
            else:
                token_info['count'] = all_count + token
                token_info['last_time'] = curr_time
                return func(*args, **kwargs)

        return _leakbucket
    return decorator
