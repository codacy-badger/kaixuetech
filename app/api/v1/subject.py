# -*- coding: utf-8 -*-
# @Time    : 2019/1/30 0:01
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from flask import g, jsonify, request

from app.libs.error_code import Success, DeleteSuccess, Forbidden
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.base import db
from app.models.subject import Subject

from app.validators.forms import SubjectForm
from app.models.teacher import Teacher

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
  subject = Subject.add(uid, form.name.data, form.picture_url.data, form.year.data, form.abstract.data,
                        form.sub_type.data)
  user = Teacher.query.filter_by(user_id=uid).first_or_404()
  user.subjectes.append(subject)
  return Success()


@api.route('/<int:p>/<int:pp>/', methods=['GET'])
@auth.login_required
def get(p,pp):
  """
    查询课程信息
    ---
    tags:
      - Subject
    parameters:
      - in: "header"
        name: "Authorization"
        description: base64加密后的token
        required: true
      - name: "p"
        in: "path"
        description: 页码
        required: false
        type: "int"
      - name: "pp"
        in: "path"
        description: 一页的数量
        required: false
        type: "int"
"""


  uid = g.user.uid
  user = Subject.query.filter_by(user_id=uid).paginate(page=p, per_page=pp, error_out=False)

  data = {"items": user.items, "pages": user.pages, 'total': user.total, 'page': user.page, 'per_page': user.per_page}

  return jsonify(data)

@api.route('/<int:id>/', methods=['GET'])
@auth.login_required
def getone(id):
  """
    查询课程信息
    ---
    tags:
      - Subject
    parameters:
      - in: "header"
        name: "Authorization"
        description: base64加密后的token
        required: true
      - name: "id"
        in: "path"
        description: 课程id
        required: false
        type: "int"

  """
  user = Subject.query.filter_by(id=id).first_or_404()
  return jsonify(user)

@api.route('/<int:id>/', methods=['DELETE'])
@auth.login_required
def delete_user(id):
  """
    删除课程信息
    ---
    tags:
      - Subject
    parameters:
      - in: "header"
        name: "Authorization"
        description: base64加密后的token
        required: true
      - name: "id"
        in: "path"
        description: 课程id
        required: false
        type: "int"

  """
  uid = g.user.uid
  with db.auto_commit():
      user = Subject.query.filter_by(id=id).first_or_404()
      if user.auth<10 and user.user_id !=uid:
        raise Forbidden()
      else:
        user.delete()
  return DeleteSuccess()