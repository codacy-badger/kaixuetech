# -*- coding: utf-8 -*-
# @Time    : 2019/3/8 10:54
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from app.libs.error_code import ParameterException


def isint(ini):

    if isinstance(ini,int):
        return True
    raise ParameterException()