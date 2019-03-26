# -*- coding: utf-8 -*-
# @Time    : 2019/3/12 14:27
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from flask import jsonify
from sqlalchemy import desc

from app.libs.error_code import Success, Forbidden, DeleteSuccess, ParameterException
from app.libs.get_method import get_method
from app.libs.redprint import Redprint
from app.libs.token_auth import auth

from app.models.user import User
from app.validators.adminforms import DelAdminForm, AdminAuthForm, UserPutForm, ChPassForm


api = Redprint('admin_user')

#获取管理员列表
@api.route('', methods=['GET'])
@auth.login_required
def get_admin_user():
    """
        获取管理员信息
        ---
        tags:
          - AdminUser
        parameters:
            - in: "header"
              name: "Authorization"
              description: base64加密后的token
              required: true
    """

    def item(user):
        user.append('email', 'comments').hide('wechat_open_id')
    users = User.query.filter(User.auth>10,User.status==1).all()
    list(map(item,users))
    total=len(users)
    data={'list':users,'total':total}
    return jsonify(data),200


#获取管理员列表
@api.route('/user', methods=['POST'])
@auth.login_required
def get_user():
    """
        获取用户信息
        ---
        tags:
          - AdminUser
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
                    page:
                       type: "int"
                       example: 1
                    limit:
                       type: "int"
                       example: 10
                    sort:
                       type: "string"
                       example: "-id"
                    likename:
                       type: "string"
                       example: "12"
    """
    filt={
        User.auth < 10
    }
    data=get_method(User, like_list=['phone', 'id','nickname','auth'], filt=filt)
    return Success(data=data)





# 修改密码
@api.route('/psw', methods=['PUT'])
@auth.login_required
def psw_admin_user():
    """
       修改管理员密码
      ---
      tags:
        - AdminUser
      parameters:
          - in: "header"
            name: "Authorization"
            description: base64加密后的token
            required: true
          - in: "body"
            name: "body"
            description: 修改管理员信息
            required: true
            schema:
               type: "object"
               properties:
                   duid:
                       type: "int"
                       example: 12
                   secret:
                       type: "string"
                       example: "我是密码"
                   secret2:
                       type: "string"
                       example: "我是重复密码"
    """
    form = ChPassForm().validate_for_api()
    user = User.query.filter_by(id=form.duid.data).first_or_404()
    user.change_password(form.secret.data)
    return Success("修改密码成功！")
#修改信息
@api.route('', methods=['PUT'])
@auth.login_required
def up_admin_user():
    """
       修改管理员信息
      ---
      tags:
        - AdminUser
      parameters:
          - in: "header"
            name: "Authorization"
            description: base64加密后的token
            required: true
          - in: "body"
            name: "body"
            description: 修改管理员信息
            required: true
            schema:
               type: "object"
               properties:
                   duid:
                       type: "int"
                       example: 12
                   comments:
                       type: "string"
                       example: "我是备注"
                   nickname:
                       type: "string"
                       example: "我是昵称"
    """
    form = UserPutForm().validate_for_api()
    user = User.query.filter_by(id=form.duid.data).first_or_404()
    comments=form.comments.data
    nickname=form.nickname.data
    if comments is not None:
        user.comments=comments
    if nickname is not None:
        user.nickname=nickname
    return Success("修改成功！")

# 删除管理员
@api.route('', methods=['DELETE'])
@auth.login_required
def del_admin_user():
    """
    删除管理员
           ---

           tags:
             - AdminUser
           parameters:
               - in: "header"
                 name: "Authorization"
                 description: base64加密后的token
                 required: true
               - in: "body"
                 name: "body"
                 description: 删除管理员
                 required: true
                 schema:
                   type: "object"
                   properties:
                       duid:
                           type: "array"
                           example: [1,2]
    """
    form = DelAdminForm().validate_for_api()

    for id in form.duid.data:
        user=User.query.filter_by(id=id).first_or_404()
        if user.auth==11:
            raise Forbidden(msg="超级管理员账号不可删除!")
        user.delete()
    return DeleteSuccess(msg="删除成功!")


#添加管理员
@api.route('/auth', methods=['POST'])
@auth.login_required
def add():
    """
            添加管理员
           ---
           tags:
             - AdminUser
           parameters:
               - in: "header"
                 name: "Authorization"
                 description: base64加密后的token
                 required: true
               - in: "body"
                 name: "body"
                 description: 添加管理员
                 required: true
                 schema:
                   type: "object"
                   properties:
                       duid:
                           type: "int"
                           example: 12
                       au:
                          type: "int"
                          example: 12
    """
    form = AdminAuthForm().validate_for_api()
    if form.au.data ==11:
        raise ParameterException()
    user = User.query.filter_by(id=form.duid.data).first_or_404()
    user.auth=form.au.data
    return Success("管理添加成功！")


