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
from app.models.duration import Duration
from app.models.folder import Folder
from app.models.subject import Subject
from app.validators.forms import DurationForm, UploadForm
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

@api.route('teacher', methods=['POST'])
@auth.login_required
def add():
    """
           老师添加资料
           ---
           tags:
             - Upload
           parameters:
               - in: "header"
                 name: "Authorization"
                 description: base64加密后的token
                 required: true
               - in: "body"
                 name: "body"
                 description: 老师添加资料
                 required: true
                 schema:
                   type: "object"
                   properties:
                       dat:
                           type: "string"
                           example: "山东师范大学"
                       subject_id:
                           type: "int"
                           example: 1
                       folder_id:
                           type: "int"
                           example: 0
                       site:
                           type: "int"
                           example: 0
        """
    uid = g.user.uid
    form = DurationForm().validate_for_api()
    Subject.query.filter_by(id=form.subject_id.data,user_id=uid).first_or_400()
    if form.folder_id.data !=0:
        Folder.query.filter_by(id=form.folder_id.data, user_id=uid).first_or_400()
    datas=(json.loads(untie_secret(form.dat.data)))
    for data in datas:
        Duration.add(data["name"], data["old_name"], uid, form.subject_id.data, data["type"],form.site.data,form.folder_id.data)
    return Success(msg="上传成功！")