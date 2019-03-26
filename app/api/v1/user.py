# -*- coding: utf-8 -*-
# @Time    : 2019/1/25 16:16
# @Author  : 昨夜
# @Email   : 903165495@qq.com

from flask import jsonify, g


from app.libs.error_code import Success
from app.libs.redprint import Redprint
from app.libs.token_auth import auth

from app.models.user import User
from app.validators.forms import PassForm, DetailForm

api = Redprint('user')

@api.route('', methods=['GET'])
@auth.login_required
def get_user():
    """
    获取用户信息
    ---
    tags:
      - User
    parameters:
        - in: "header"
          name: "Authorization"
          description: base64加密后的token
          required: true
    """
    uid = g.user.uid
    user = User.query.filter_by(id=uid).first_or_404()
    return jsonify(user)


@api.route('/change_pa', methods=['POST'])
@auth.login_required
def change_password():
    """
        用户修改密码
        ---
        tags:
          - User
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
                    secret:
                        type: "string"
                        example: "123456"
        """
    uid = g.user.uid
    form = PassForm().validate_for_api()
    user = User.query.filter_by(id=uid).first_or_404()
    user.change_password(form.secret.data)
    return Success()


@api.route('/wxdetail', methods=['POST'])
@auth.login_required
def change_detail():
    """
        添加用户微信小程序信息
        ---
        tags:
          - User
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
                    wechat_open_id:
                        type: "string"
                        example: "123456"
                    nickname:
                        type: "string"
                        example: "123456"
    """
    uid = g.user.uid
    form = DetailForm().validate_for_api()
    user = User.query.filter_by(id=uid).first_or_404()
    if form.wechat_open_id.data is not None:
        user.wechat_open_id = form.wechat_open_id.data
    if form.nickname.data is not None:
        user.nickname = form.nickname.data
    return Success()


