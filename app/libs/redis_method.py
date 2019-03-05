# -*- coding: utf-8 -*-
# @Time    : 2019/2/28 13:38
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from app.libs.add_redis import r

from hashlib import sha1

# 加密算法
def jia_mi(str):
    sh = sha1()
    sh.update(str.encode())
    return sh.hexdigest()

# 学校名来获得代码
def school_to_code(name):
    return r.hget("school_list",name).decode()

"""
学生签到
"""

class Student_Attend_Redis():
    # 添加
    @staticmethod
    def student_attend_add(studentid,attendid):
        data=jia_mi(str(studentid)+';'+str(attendid))
        a=r.hset('student_attend', data, data)
        return a
    #获取
    @staticmethod
    def student_attend_get(studentid,attendid):
        data = jia_mi(str(studentid) + ';' + str(attendid))
        a=r.hget('student_attend', data)
        return a
