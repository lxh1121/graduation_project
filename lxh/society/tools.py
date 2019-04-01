#coding:utf-8

import hashlib
import re

#
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# 展示信息跳转
def show_message(msg, url):
    str = '<script>alert("' + msg + '"),location.href="' + url + '"</script>'
    return str

# 判断密码格式
def judge_pass(password):
    r = r'^[a-zA-Z0-9]{6,20}$'
    result = re.match(r, password)
    if result is None:
        return None
    else:
        return password

# 密码加密
def add_pass(password):
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    return md5.hexdigest()


# 判断手机号格式
def judge_phone(phone):
    r = r'^[0-9]{11}$'
    result = re.match(r, phone)
    if result is None:
        return None
    else:
        return phone


# 判断审核状态
def page_aduit(article_list, page, page_yeshu):
    paginator = Paginator(article_list, page_yeshu)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果请求的页数不是整数，返回第一页。
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        contacts = paginator.page(paginator.num_pages)
    return contacts


# 星期转化为汉字星期几
def week_chinese(now_week):
    if now_week == 0:
        now_week = '一'
    elif now_week == 1:
        now_week = '二'
    elif now_week == 2:
        now_week = '三'
    elif now_week == 3:
        now_week = '四'
    elif now_week == 4:
        now_week = '五'
    elif now_week == 5:
        now_week = '六'
    elif now_week == 6:
        now_week = '日'
    return now_week

