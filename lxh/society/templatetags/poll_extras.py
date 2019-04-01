#coding:utf-8
from django import template
from datetime import datetime
register = template.Library()


# 判断时间差  过滤器
def date_minus(value):
    value = value.replace(tzinfo=None)
    newtime = datetime.now()
    minus_time = (newtime - value).total_seconds()
    if minus_time < 60:
        value = '1分钟前'
    elif minus_time < 3600:
        value = str(int(minus_time / 60)) + '分钟前'
    elif minus_time < 86400:
        value = str(int(minus_time / 3600)) + '小时前'
    elif minus_time >= 86400:
        value = str(int(minus_time / 86400)) + '天前'
    return value


register.filter('minus', date_minus)
