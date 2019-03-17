# -*- coding: utf-8 -*-
# @Time    : 2019/3/5 15:10
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from flask import request, g
from app.libs.error_code import Success, Uploadmore, ParameterException, UpflieError
from app.libs.redprint import Redprint
from app.libs.string_secret import add_secret, untie_secret
from app.libs.token_auth import auth
from app.libs.upload import qiniu_upload_file

import json
api = Redprint('duration')

@api.route('upload/<int:site>', methods=['POST'])
@auth.login_required
def upload(site):
    """
           上传文件
           ---
           tags:
             - Upload
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
                 name: "file"
                 description: "file to upload"
                 required: false
                 type: "file"
               - name: "site"
                 in: "path"
                 description: 属性
                 required: True
                 type: "int"

    """
    if type(site) is not int:
        raise ParameterException()
    f = request.files
    file_list = [fi for fi in f]
    if len(file_list) < 1:
        raise ParameterException()
    def more_file(file):
        return qiniu_upload_file(f[file])
    if site==0:
        if len(file_list)>1:
            raise Uploadmore()
        else:
            file_name=f[file_list[0]].filename.split('.')[-1]
            Str2 = ['ppt','pptx', 'doc', 'pdf']
            if file_name in Str2:
                data=[qiniu_upload_file(f[file_list[0]])]
                password = json.dumps(data)
                str_da = add_secret(password)
                return Success(data=str_da)
            return UpflieError(msg="格式不对！")
    if site==1:
        data=list(map(more_file,file_list))
        password = json.dumps(data)
        str_da=add_secret(password)
        return Success(data=str_da)

    raise ParameterException()
   # datas=(json.loads(untie_secret(form.dat.data)))
