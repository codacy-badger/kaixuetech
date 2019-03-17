# -*- coding: utf-8 -*-
# @Time    : 2019/3/13 13:44
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from flask import g
from app.api.v1.classs import api
from app.libs.error_code import Success
from app.libs.token_auth import auth
from app.models.class_student import ClassStudent
from app.validators.classforms import SchoolForm, StAuthForm, StDetailForm


@api.route('/stschool', methods=['POST'])
@auth.login_required
def student_creat():
    """
       学生选择学校
       ---
       tags:
         - Class
       parameters:
           - in: "header"
             name: "Authorization"
             description: base64加密后的token
             required: true
           - in: "body"
             name: "body"
             description: 学生选择学校
             required: true
             schema:
               type: "object"
               properties:
                   school_id:
                       type: "string"
                       example: "0333"
    """
    uid = g.user.uid
    form=SchoolForm().validate_for_api()
    ClassStudent.query.filter_by(user_id=uid).first_or_401()
    data = ClassStudent().create(uid, form.school_id.data)
    return Success(data=data)

@api.route('/stauth', methods=['POST'])
@auth.login_required
def student_auth():
    """
       认证
       ---
       tags:
         - Class
       parameters:
           - in: "header"
             name: "Authorization"
             description: base64加密后的token
             required: true
           - in: "body"
             name: "body"
             description: 学生选择学校
             required: true
             schema:
               type: "object"
               properties:
                   sno:
                       type: "string"
                       example: "201511010127"
                   name:
                       type: "string"
                       example: "汤立虎"
                   grade:
                       type: "string"
                       example: "2019"
    """
    uid = g.user.uid
    form = StAuthForm().validate_for_api()
    student=ClassStudent.query.filter_by(user_id=uid).first_or_404()
    student.upauth(form.sno.data,form.name.data,form.grade.data)
    return Success(data=student)

@api.route('/stdetail', methods=['POST'])
@auth.login_required
def student_detail():
    """
       详细资料修改
       ---
       tags:
         - Class
       parameters:
           - in: "header"
             name: "Authorization"
             description: base64加密后的token
             required: true
           - in: "body"
             name: "body"
             description: 详细资料修改
             required: true
             schema:
               type: "object"
               properties:
                   auth_url:
                       type: "string"
                       example: "http://img2.mukewang.com/54584d6100015f5802200220-100-100.jpg"
                   major:
                       type: "string"
                       example: "计算机科学与技术"
                   classno:
                       type: "string"
                       example: "1501"
    """
    uid = g.user.uid
    form = StDetailForm().validate_for_api()
    student = ClassStudent.query.filter_by(user_id=uid).first_or_404()
    student.detail(form.auth_url.data, form.major.data, form.classno.data)
    return Success(data=student)