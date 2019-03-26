# -*- coding: utf-8 -*-
# @Time    : 2019/3/15 13:38
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from flask import request

from app.libs.aliyun_oss import stsauth
from app.libs.error_code import ParameterException, Success
from app.libs.redprint import Redprint
from app.libs.string_secret import add_secret, add_secret1
from app.libs.token_auth import auth
from app.libs.upload import qiniu_upload_file, aliyun_upload_file, aliyun_get_url
import json

from app.validators.forms import NameForm

api = Redprint('admin_libs')

@api.route('/upload', methods=['POST'])
@auth.login_required
def upload():
    """
           上传文件
           ---
           tags:
             - AdminLibs
           operationId: "uploadFile"
           consumes:
             - "multipart/form-data"
           parameters:
               - in: "header"
                 name: "Authorization"
                 description: base64加密后的token
                 required: true
               - in: "formData"
                 name: "file"
                 description: "file to upload"
                 required: false
                 type: "file"



    """
    f = request.files
    file_list = [fi for fi in f]
    if len(file_list) < 1:
        raise ParameterException()
    def more_file(file):
        return aliyun_upload_file(f[file])
        # return qiniu_upload_file(f[file])
    data = list(map(more_file, file_list))
    password = json.dumps(data)
    str_da = add_secret(password)
    for i in data:
        i["name"]=aliyun_get_url(i["name"])
    a={"secret_url":str_da,"url":data}
    return Success(data=a)

@api.route('/url', methods=['POST'])
@auth.login_required
def url():
    """
        获取完整链接
        ---
        tags:
          - AdminLibs
        parameters:
            - in: "header"
              name: "Authorization"
              description: base64加密后的token
              required: true
            - in: "body"
              name: "body"
              description: 获取完整链接
              required: true
              schema:
                type: "object"
                properties:
                    name:
                       type: "string"
                       example: "MTUxNTUzMjI2ODg0MDcxMTU=.png"

    """
    form=NameForm().validate_for_api()
    return Success(data=aliyun_get_url(form.name.data))
@api.route('/stsauth', methods=['get'])
# @auth.login_required
def get_stsauth():
    """
        获取完整链接
        ---
        tags:
          - AdminLibs


    """
    return Success(data=stsauth())
