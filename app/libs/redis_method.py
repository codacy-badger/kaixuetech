# -*- coding: utf-8 -*-
# @Time    : 2019/2/28 13:38
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from app.libs.add_redis import r

from hashlib import sha1

# 加密算法
from app.libs.error_code import ParameterException
from app.models.school import School
import json

def jia_mi(str):
    sh = sha1()
    sh.update(str.encode())
    return sh.hexdigest()

# 学校名来获得代码
def school_to_code(name):
    try:
        a=r.hget("school_list",name).decode()
    except:
        raise ParameterException()
    return a

def code_to_school(code):
    try:
        a=r.hget("school_code_list", code).decode()
    except:
        raise ParameterException("学校有误！")
    return a
def code_to_province(code):
    try:
        a=r.hget("school_province_list", code).decode()
    except:
        raise ParameterException("学校有误！")
    return a
def change_school():
    schools = (School.query.filter_by(show=1).all())
    school1s = (School.query.filter_by(show=1).group_by(School.province).all())
    datas = []
    for school1 in school1s:
        data = {"label": school1.province,
                "value": school1.province,
                "children": []
                }
        for school in schools:
            if school.province == school1.province:
                data["children"].append(school.to_json())
                schools.remove(school)
        datas.append(data)



    r.hdel("school", "sdsdsd#%#$%")
    a = r.hset("school","sdsdsd#%#$%", datas)
    return  a
def getschool():
    a = r.hget("school", "sdsdsd#%#$%").decode()
    user_dict = eval(a)
    return user_dict

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


#学生答题
class Student_Answer_Redis():
    @staticmethod
    def student_answer_add(key, value):
        a = r.hset('student_answer', key, value)
        return a

        # 获取
    @staticmethod
    def student_answer_get(key):
        a = r.hget('student_answer', key)
        return a