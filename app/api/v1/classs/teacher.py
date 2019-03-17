# -*- coding: utf-8 -*-
# @Time    : 2019/3/13 13:44
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from flask import g
from app.api.v1.classs import api
from app.libs.error_code import Success
from app.libs.token_auth import auth
from app.models.class_teacher import ClassTeacher
from app.validators.classforms import SchoolForm, TeDetailForm


@api.route('/teschool', methods=['POST'])
@auth.login_required
def teacher_creat():
    """
       老师选择学校
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
             description: 老师选择学校
             required: true
             schema:
               type: "object"
               properties:
                   school_id:
                       type: "int"
                       example: 10
    """
    uid = g.user.uid
    form=SchoolForm().validate_for_api()
    ClassTeacher.query.filter_by(user_id=uid).first_or_401()
    data = ClassTeacher().create(uid, form.school_id.data)
    return Success(data=data)
@api.route('/tedetail', methods=['POST'])
@auth.login_required
def teacher_detail():
    """
       老师详细资料修改
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
             description: 老师详细资料修改
             required: true
             schema:
               type: "object"
               properties:
                   head_url:
                       type: "string"
                       example: "http://img2.mukewang.com/54584d6100015f5802200220-100-100.jpg"
                   abstract:
                       type: "string"
                       example: "我是一个老师"
                   abstract:
                       type: "string"
                       example: "方世杰"
    """
    uid = g.user.uid
    form = TeDetailForm().validate_for_api()
    teacher = ClassTeacher.query.filter_by(user_id=uid).first_or_404()
    teacher.detail(form.head_url.data, form.abstract.data, form.abstract.data)
    return Success(data=teacher)