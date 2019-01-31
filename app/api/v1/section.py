# -*- coding: utf-8 -*-
# @Time    : 2019/1/31 13:53
# @Author  : 昨夜
# @Email   : 903165495@qq.com
import datetime

from flask import g

from app.libs.error_code import Success
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.section import Section
from app.validators.forms import SectionForm

api = Redprint('section')
@api.route('', methods=['POST'])
@auth.login_required
def add():
    """
         添加课堂
         ---
         tags:
           - Section
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
                         example: "第一节"
                     subject_id:
                         type: "int"
                         example: 1
                     class_time:
                         type: "string"
                         example: "2019/01/31 15:00"
                     duration:
                         type: "string"
                         example: 45.0
                     learn_data:
                         type: "string"
                         example: "www.baidu.com"
                     abstract:
                         type: "string"
                         example: "我是这节课的介绍"
         """
    form=SectionForm().validate_for_api()
    string=(form.class_time.data)
    time=datetime.datetime.strptime(string, "%Y/%m/%d %H:%M")
    print(time)
    Section().add(form.name.data,
                  form.subject_id.data,
                  time,
                  form.duration.data,
                  form.learn_data.data,
                  form.abstract.data
                  )
    return Success()

