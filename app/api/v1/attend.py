# -*- coding: utf-8 -*-
# @Time    : 2019/2/28 14:18
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from flask import jsonify, g

from app.libs.Time import Time
from app.libs.error_code import Success, Forbidden, HadDone
from app.libs.ran_num import random_num
from app.libs.redis_method import school_to_code, Student_Attend_Redis
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.attend import Attend
from app.models.attendes_middle import Attendes_Middle
from app.models.student import Student
from app.models.studentes_middle_subject import Studentes_Middle_Subject
from app.models.subject import Subject
from app.validators.forms import AttendForm, StudentAttendForm, TeacherEndAttendForm

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
                       code:
                            type: "string"
                            example: "1478"
                       attend_position:
                             type: "string"
                             example: "116.414617,39.943485"
                       ip:
                             type: "string"
                             example: "112.17.240.35"
    """
    uid = g.user.uid

    form = StudentAttendForm().validate_for_api()
    student = Student.query.filter_by(user_id=uid).first_or_404()

    school_name=student.school_name
    school_code = school_to_code(school_name)
    date = Time().nowdate()
    attend_number = school_code + date+form.code.data

    # 判断学生有没有选这门课
    att = Student_Attend_Redis.student_attend_get(uid, attend_number)
    if att is not None:
        raise HadDone()

    attend = Attend.query.filter_by(attend_number_secret=attend_number,attend_state=1).first_or_404()
    print("11")
    student_id = student.id  # 学生id
    attend_id=attend.id    #考勤表id
    attendes_middles=Attendes_Middle.query.filter_by(attend_id=attend_id,student_id=student_id).first_or_404()
    # 进行签到
    attendes_middles.up(form.attend_position.data, form.ip.data)
    Student_Attend_Redis.student_attend_add(uid, attend_number)
    return Success(data=attendes_middles)

"""
结束签到
"""
@api.route('/teacher_end_attend/', methods=['POST'])
@auth.login_required
def teacher_end_attend():
    """
              老师结束签到
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
                    description: 老师结束签到
                    required: true
                    schema:
                      type: "object"
                      properties:
                          attend_id:
                               type: "int"
                               example: 1

       """
    uid = g.user.uid
    form = TeacherEndAttendForm().validate_for_api()
    attend = Attend.query.filter_by(id=form.attend_id.data,attend_state=1).first_or_404()
    atten_middle=attend.attendes_middles.filter_by(attend_position_state=1).all()
    return Success(data=atten_middle)