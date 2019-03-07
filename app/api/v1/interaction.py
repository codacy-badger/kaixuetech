# -*- coding: utf-8 -*-
# @Time    : 2019/3/7 18:04
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from flask import g
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.course_info import CourseInfo

api = Redprint('interaction')


# 创建课程
@api.route('course', methods=['POST'])
@auth.login_required
def course():
    """
           添加课程
           ---
           tags:
             - Interaction
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
                       duration_id:
                           type: "int"
                           example: 12
    """
    uid = g.user.uid

    CourseInfo.query.filter_by(id=form.subject_id.data, user_id=uid).first_or_403()