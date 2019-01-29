# -*- coding: utf-8 -*-
# @Time    : 2019/1/25 16:16
# @Author  : 昨夜
# @Email   : 903165495@qq.com

from flask import jsonify, g
from app.libs.error_code import Success, ParameterException
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.student import Student


from app.validators.forms import SchoolForm, AuthForm

api = Redprint('student')


@api.route('/school', methods=['POST'])
@auth.login_required
def add_school():
    """
       添加学校
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
    Student.query.filter_by(user_id=uid).first_or_401()
    form = SchoolForm().validate_for_api()
    Student().school(uid, form.school.data)
    return Success()


@api.route('/auth', methods=['POST'])
@auth.login_required
def add_auth():
    """
            添加身份验证
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
                  description: 添加验证
                  required: true
                  schema:
                    type: "object"
                    properties:
                        name:
                            type: "string"
                            example: "方世杰"
                        auth_url:
                            type: "string"
                            example: "我是图片链接"
                        sno:
                            type: "string"
                            example: "201511010127"
            """
    form = AuthForm().validate_for_api()
    uid = g.user.uid
    user = Student.query.filter_by(user_id=uid).first_or_404()

    if user.examine == 1:  # 还未认证
        user.auth(form.name.data, form.auth_url.data, form.sno.data)
        return Success()
    else:
        return ParameterException()


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

    return jsonify(user)
