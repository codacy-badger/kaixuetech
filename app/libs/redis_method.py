# -*- coding: utf-8 -*-
# @Time    : 2019/2/28 13:38
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from app.libs.add_redis import r

# 学校名来获得代码
def school_to_code(name):
    return r.hget("school_list",name)
