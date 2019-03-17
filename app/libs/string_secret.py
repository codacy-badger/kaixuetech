# -*- coding: utf-8 -*-
# @Time    : 2019/3/5 17:19
# @Author  : 昨夜
# @Email   : 903165495@qq.com
import base64

from app.libs.error_code import UpflieError


def add_secret(str1):
    da = base64.b64encode(str1.encode('utf-8'))
    da1= str(da,'utf-8')
    return da1
def add_secret1(str1):
    da = base64.b64encode(str1)
    da1= str(da)
    return da1
def untie_secret(str):
    try:
        da1 =base64.b64decode(str.encode('utf-8'))
        return da1
    except:
        return UpflieError()