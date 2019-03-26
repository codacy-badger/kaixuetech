# -*- coding: utf-8 -*-
# @Time    : 2019/3/5 15:10
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from flask import request, g
from app.libs.error_code import Success, Uploadmore, ParameterException, UpflieError
from app.libs.redprint import Redprint
from app.libs.string_secret import add_secret, untie_secret
from app.libs.token_auth import auth
from app.libs.upload import  aliyun_upload_file

import json

from app.models.duration import Duration
from app.validators.forms import DurationForm

api = Redprint('duration')


@api.route('', methods=['POST'])
@auth.login_required
def add():
    """
        获取资料
        ---
        tags:
          - Duration
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
                    site:
                       type: "int"
                       example: 1
                    folder_id:
                       type: "int"
                       example: 10
                    dat:
                       type: "string"
                       example: "W3sibmFtZSI6ICJodHRwOi8vdXBsb2FkLmthaXh1ZXRlY2guY29tL01UQXhOVFV6TURVNU1UQTVNalUyTVRjPS5wbmciLCAidHlwZSI6ICJwbmciLCAib2xkX25hbWUiOiAiMTU0Njc4NDQyNzM0OC5wbmcifV0="
                    subject_id:
                       type: "int"
                       example: 1
    """
    form = DurationForm().validate_for_api()
    site=form.site.data
    folder_id=form.folder_id.data
    dat = form.dat.data
    subject_id = form.subject_id.data
    A=untie_secret(dat)
    data = json.loads(A)
    userid = g.user.uid
    for da in data:
        name=da["name"]
        old_name=da["old_name"]
        type=da["type"]
        Duration.add(name,old_name,userid,subject_id,type,site,folder_id)
    return Success("上传成功！")
@api.route('/upload/<int:site>', methods=['POST'])
@auth.login_required
def upload(site):
    """
           上传文件
           ---
           tags:
             - Duration
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
               - name: "site"
                 in: "path"
                 description: 属性
                 required: True
                 type: "int"

    """
    if  not isinstance(site,'int'):
        raise ParameterException()
    f = request.files
    file_list = [fi for fi in f]
    if len(file_list) < 1:
        raise ParameterException()
    def more_file(file):
        return aliyun_upload_file(f[file])
    if site==0:
        if len(file_list)>1:
            raise Uploadmore()
        else:
            file_name=f[file_list[0]].filename.split('.')[-1]
            Str2 = ['ppt','pptx', 'doc', 'pdf']
            if file_name in Str2:
                data=[aliyun_upload_file(f[file_list[0]])]
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
