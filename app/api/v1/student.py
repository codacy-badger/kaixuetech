# -*- coding: utf-8 -*-
# @Time    : 2019/1/25 16:16
# @Author  : 昨夜
# @Email   : 903165495@qq.com

from flask import jsonify, g

from app.libs.Time import Time
from app.libs.error_code import Success, ParameterException
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.student import Student

from app.validators.forms import StudentForm, preStudentForm

api = Redprint('student')


@api.route('', methods=['POST'])
@auth.login_required
def add():
    """
       添加学生信息
       ---
       tags:
         - Student
       parameters:
           - in: "header"
             name: "Authorization"
             description: base64加密后的token
             required: true
           - in: "body"
             name: "body"
             description: 添加学校
             required: true
             schema:
               type: "object"
               properties:
                   name:
                       type: "string"
                       example: "方世杰"
                   sno:
                       type: "string"
                       example: "201511010127"
                   school_name:
                       type: "string"
                       example: "山东师范大学"
                   auth_url:
                       type: "string"
                       example: "http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJLCibicOeXme44Sj9Zzia8h15kzVYsy4ekhLo5KREuh1xWDiaXXO9yicsUFSIz02BnCRuIqOxic3sUgGKg/132"
       """
    uid = g.user.uid
    Student.query.filter_by(user_id=uid).first_or_401()
    form = StudentForm().validate_for_api()
    student = Student().add(user_id=uid, name=form.name.data, sno=form.sno.data, school_name=form.school_name.data,
                            auth_url=form.auth_url.data)
    return Success(data=student)


@api.route('', methods=['GET'])
@auth.login_required
def student():
    """
               查询学生信息
               ---
               tags:
                 - Student
               parameters:
                   - in: "header"
                     name: "Authorization"
                     description: base64加密后的token
                     required: true

               """
    uid = g.user.uid
    user = Student.query.filter_by(user_id=uid).first_or_404()

    return Success(data=user)


@api.route('/perf', methods=['POST'])
@auth.login_required
def perfect():
    """
       完善学生信息
       ---
       tags:
         - Student
       parameters:
           - in: "header"
             name: "Authorization"
             description: base64加密后的token
             required: true
           - in: "body"
             name: "body"
             description: 完善学生信息
             required: true
             schema:
               type: "object"
               properties:
                   major:
                       type: "string"
                       example: "计算机科学与技术"
                   grade:
                       type: "string"
                       example: "大四"
                   classno:
                       type: "string"
                       example: "1501"
                   enrolltime:
                       type: "string"
                       example: "2015-6"
       """
    uid = g.user.uid
    student = Student.query.filter_by(user_id=uid).first_or_404()
    form = preStudentForm().validate_for_api()
    if form.enrolltime.data is not None and Time().isVaildDate(form.enrolltime.data):
        student.enrolltime = form.enrolltime.data
    else:
        raise ParameterException()
    if form.grade.data is not None:
        student.grade = form.grade.data
    if form.major.data is not None:
        student.major = form.major.data
    if form.classno.data is not None:
        student.classno = form.classno.data
    return Success(data=student)
