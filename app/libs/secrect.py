# -*- coding: utf-8 -*-
# @Time    : 2019/3/19 16:24
# @Author  : 昨夜
# @Email   : 903165495@qq.com

from itsdangerous import TimedJSONWebSignatureSerializer



s = TimedJSONWebSignatureSerializer("122525sdsdsde33#$#$$!DSXs#$#$##$2sddrr899**--+", expires_in=3600)

def addid(dic):
    data = s.dumps(dic)

    return str(data,encoding="utf8")
def upid(str):
    stri = bytes(str, encoding="utf8")
    data = s.loads(stri)
    return data
