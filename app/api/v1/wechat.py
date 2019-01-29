# -*- coding: utf-8 -*-
# @Time    : 2019/1/27 14:55
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.libs.url_format import get_url_format
from app.validators.forms import JsCodeForm
from flask import jsonify
import json
api = Redprint('wechat')

import requests
@api.route('', methods=['POST'])
def get_openid():
    """
           用户修改密码
           ---
           tags:
             - Wechat
           parameters:

               - in: "body"
                 name: "body"
                 description: 提交新的密码
                 required: true
                 schema:
                   type: "object"
                   properties:
                       code:
                           type: "string"
                           example: "123456"
           """
    form = JsCodeForm().validate_for_api()
    code=form.code.data

    data={
       "appid" :"wxb20c58d5ec8bd8a0",
        "secret":"92bf4844dd33e06382f28ee9ba751139",
        "js_code":code,
        "grant_type":"authorization_code"
    }

    url="https://api.weixin.qq.com/sns/jscode2session"
    url=get_url_format(url=url,params=data)
    a=requests.get(url)

    dictinfo = json.loads(a.text)
    return jsonify(dictinfo)