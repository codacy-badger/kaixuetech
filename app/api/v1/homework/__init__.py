# -*- coding: utf-8 -*-
# @Time    : 2019/3/20 17:46
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from app.libs.redprint import Redprint

api = Redprint('homework')

from  app.api.v1.homework import student,teacher

