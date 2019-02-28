# -*- coding: utf-8 -*-
# @Time    : 2019/1/25 16:16
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from flask import g, jsonify

from app.libs.error_code import ParameterException, Success
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.teacher import Teacher
from app.validators.forms import SchoolForm, TeacherForm

api = Redprint('teacher')

@api.route('', methods=['get'])
@auth.login_required
def get():
    """
         查询老师信息
         ---
         tags:
           - Teacher
         parameters:
             - in: "header"
               name: "Authorization"
               description: base64加密后的token
               required: true

         """
    uid = g.user.uid
    user = Teacher.query.filter_by(user_id=uid).first_or_404().hide('user_id')
    return jsonify(user)

@api.route('', methods=['POST'])
@auth.login_required
def add():
    """
       添加学校
       ---
       tags:
         - Teacher
       parameters:
           - in: "header"
             name: "Authorization"
             description: base64加密后的token
             required: true
           - in: "body"
             name: "body"
             description: 提交新的密码
             required: true
             schema:
               type: "object"
               properties:
                   school:
                       type: "string"
                       example: "山东师范大学"
    """
    uid = g.user.uid
    Teacher.query.filter_by(user_id=uid).first_or_401()

    form = SchoolForm().validate_for_api()
    Teacher().addschool(uid, form.school.data)
    return Success()

@api.route('/detail', methods=['POST'])
@auth.login_required
def detail():
    """
           添加老师细节
           ---
           tags:
             - Teacher
           parameters:
               - in: "header"
                 name: "Authorization"
                 description: base64加密后的token
                 required: true
               - in: "body"
                 name: "body"
                 description: 提交新的密码
                 required: true
                 schema:
                   type: "object"
                   properties:
                       abstract:
                           type: "string"
                           example: "这里可以填写一些老师的自我介绍"
                       head_url:
                           type: "string"
                           example: "https://gss0.bdstatic.com/70cFfyinKgQIm2_p8IuM_a/daf/pic/item/b3fb43166d224f4a0a3944f604f790529922d1b6.jpg"
        """
    form = TeacherForm().validate_for_api()
    uid = g.user.uid
    user = Teacher.query.filter_by(user_id=uid).first_or_404()
    if form.abstract.data is None and form.head_url.data is None:
        return ParameterException()
    user.updetail(form.head_url.data,form.abstract.data)
    return Success()



