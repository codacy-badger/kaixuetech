# -*- coding: utf-8 -*-
# @Time    : 2019/3/15 13:50
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from flask import g

from app.api.v1.attend import api
from app.libs.Time import Time
from app.libs.error_code import Success, ParameterException
from app.libs.ran_num import random_num
from app.libs.token_auth import auth
from app.models.attend_info import AttendInfo
from app.models.attend_student import AttendStudent
from app.models.attend_subject import AttendSubject
from app.models.class_study import ClassStudy
from app.models.class_teach import ClassTeach
from app.models.class_teacher import ClassTeacher
from app.validators.forms import AttendForm, TeacherEndAttendForm


@api.route('/te', methods=['POST'])
@auth.login_required
def teacher_add():
    """
           老师创建考勤
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
                 description: 老师创建考勤
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
    subject_id=form.subject_id.data
    attend_name = form.attend_name.data
    #是否是自己的课

    teacher=ClassTeacher.query.join(ClassTeach,ClassTeacher.id==ClassTeach.teacher_id).filter_by(user_id=uid,subject_id=subject_id).first_or_404()
    school_code = teacher.school_id
    date = Time().nowdate()
    attend_number = random_num(school_code + date)
    attend=AttendInfo.add(attend_name, attend_number)
    #创建签到表
    attend=AttendSubject.add(attend.id, subject_id,teacher.id,uid)
    attend_id=attend.id
    def add_student(student):
        student_id=student.id
        user_id=student.user_id
        AttendStudent.add(attend_id, student_id,user_id)

    # 查询选课的学生
    studens=ClassStudy.query.filter_by(subject_id=subject_id).all()
    list(map(add_student,studens))
    return Success(data=attend)

"""
结束签到
"""
@api.route('/teend', methods=['POST'])
@auth.login_required
def teacher_end():
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
    attend=AttendInfo.query.join(AttendSubject,
                                 AttendSubject.attend_id==AttendInfo.id
                                 ).filter_by(
                                    attend_id=form.attend_id.data,
                                    teacher_id=uid
                                        ).first_or_404("没有找到你想要的！")

    if attend.attend_state==1:
        attend.attend_state=2
        attend.end_time=Time().now()
    else:
        raise ParameterException("已经结束了！")

    return Success(data=attend,msg="签到已经结束")