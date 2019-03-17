# -*- coding: utf-8 -*-
# @Time    : 2019/3/15 13:38
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from flask import request

from app.libs.error_code import ParameterException, Success
from app.libs.redprint import Redprint
from app.libs.string_secret import add_secret, add_secret1
from app.libs.token_auth import auth
from app.libs.upload import qiniu_upload_file
import json
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
               - in: "formData"
                 name: "file1"
                 description: "file to upload"
                 required: false
                 type: "file"


    """
    f = request.files
    file_list = [fi for fi in f]
    if len(file_list) < 1:
        raise ParameterException()
    def more_file(file):
        return qiniu_upload_file(f[file])
    data = list(map(more_file, file_list))
    password = json.dumps(data)
    str_da = add_secret(password)
    a={"secret_url":str_da,"url":data,'head':'http://upload.kaixuetech.com/'}
    return Success(data=a)