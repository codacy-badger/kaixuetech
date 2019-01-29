# -*- coding: utf-8 -*-
# @Time    : 2019/1/30 0:01
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from flask import g

from app.libs.error_code import Success
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.subject import Subject
from app.validators.forms import SubjectForm

api = Redprint('subject')

@api.route('', methods=['POST'])
@auth.login_required
def add():
    """
       添加科目
       ---
       tags:
         - Subject
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
                   name:
                       type: "string"
                       example: "高等数学"
                   year:
                       type: "string"
                       example: "2018-2019"
                   semester:
                       type: "string"
                       example: "下学期"
                   picture_url:
                       type: "string"
                       example: "www.baidu.com"
                   abstract:
                       type: "string"
                       example: "高等数学是一门高深的语言"
                   sub_type:
                       type: "int"
                       example: 1
       """
    uid = g.user.uid
    form = SubjectForm().validate_for_api()
    Subject.add(form.name.data,uid,form.year.data,form.semester.data,form.picture_url.data ,form.abstract.data,form.sub_type.data)
    return Success()