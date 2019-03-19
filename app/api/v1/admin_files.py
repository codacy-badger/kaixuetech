# -*- coding: utf-8 -*-
# @Time    : 2019/3/19 14:31
# @Author  : 昨夜
# @Email   : 903165495@qq.com


from app.libs.error_code import Success
from app.libs.get_method import get_join_method
from app.libs.redprint import Redprint
from app.libs.token_auth import  auth
from app.models.duration import Duration
from app.models.user import User
from app.validators.classforms import PageForm, onedataForm
from app.validators.forms import FileNameForm

api = Redprint('admin_files')
#获取文件
@api.route('/classfile', methods=['post'])
@auth.login_required
def get_classfile():
    """
        获取签到表
        ---
        tags:
          - AdminFiles
        parameters:
            - in: "header"
              name: "Authorization"
              description: base64加密后的token
              required: true
            - in: "body"
              name: "body"
              description: 获取签到表
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
                    site:
                       type: "int"
                       example: 1
    """
    form = onedataForm().validate_for_api()
    que = Duration.query.join(User, Duration.userid == User.id).add_entity(User)
    Big = Duration
    filt={
        Duration.site==form.site.data
    }
    data = get_join_method(Big, que, form, like_list=['id','name','old_name'],filt=filt)
    return Success(data=data)

#修改文件名称
@api.route('/filename', methods=['PUT'])
@auth.login_required
def change_filename():
    """
        修改文件名称
        ---
        tags:
          - AdminFiles
        parameters:
            - in: "header"
              name: "Authorization"
              description: base64加密后的token
              required: true
            - in: "body"
              name: "body"
              description: 修改文件名称
              required: true
              schema:
                type: "object"
                properties:
                    id:
                       type: "int"
                       example: 1
                    name:
                       type: "string"
                       example: "12"

    """
    form = FileNameForm().validate_for_api()
    id=form.id.data
    name = form.name.data
    dur=Duration.query.filter_by(id=id).first_or_404()
    dur.old_name=name+'.'+dur.type
    return Success(data=dur)
