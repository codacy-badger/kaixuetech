# -*- coding: utf-8 -*-
# @Time    : 2019/2/28 14:18
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from flask import jsonify, g

from app.libs.Time import Time
from app.libs.error_code import Success, Forbidden
from app.libs.ran_num import random_num
from app.libs.redis_method import school_to_code
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.attend import Attend
from app.models.attendes_middle import Attendes_Middle
from app.models.subject import Subject
from app.validators.forms import AttendForm, StudentAttendForm

api = Redprint('attend')


@api.route('', methods=['POST'])
@auth.login_required
def add():
    """
           老师添加考勤
           ---
           tags:
             - Attend
           parameters:
               - in: "header"
                 name: "Authorization"
                 description: base64加密后的token
                 required: true
               - in: "body"
                 name: "body"
                 description: 老师添加考勤
                 required: true
                 schema:
                   type: "object"
                   properties:
                       subject_id:
                            type: "int"
                            example: 12
                       attend_name:
                            type: "string"
                            example: "第一次签到"
        """
    uid = g.user.uid
    form = AttendForm().validate_for_api()
    subjectes = Subject.query.filter_by(id=form.subject_id.data).first_or_404()  #获取科目信息

    """
    判断是否是自己的课
    """
    if subjectes.teacherone.user_id !=uid:
        raise Forbidden()

    school_name=subjectes.teacherone.school_name

    """
    生成随机码
    """
    school_code=school_to_code(school_name)
    date=Time().nowdate()
    attend_number=random_num(school_code+date)
    attend_name=form.attend_name.data
    attend=Attend.add(attend_name,subjectes,attend_number)  #添加考勤表
    datas=subjectes.studentes_middle_subjectes.all()
    def addstudents(data):
        Attendes_Middle.add(attend, data)
    list(map(addstudents,datas))
    return Success(data=attend)

"""
学生签到
"""
@api.route('/student_attend/', methods=['POST'])
@auth.login_required
def student_attend():
    uid = g.user.uid

    #判断学生有没有选这门课

    form=StudentAttendForm.validate_for_api()
    attend = Attend.query.filter_by(attend_number=form.code.data).first_or_404()