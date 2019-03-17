# -*- coding: utf-8 -*-
# @Time    : 2019/3/14 16:44
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from app.libs.error_code import Success, DeleteSuccess
from app.libs.get_method import get_method
from app.libs.redis_method import change_school, getschool
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.school import School
from app.models.school_province import SchoolProvince
from app.validators.adminforms import DelSchoolForm, DelAdminForm

api = Redprint('admin_school')

#获取老师列表
@api.route('', methods=['post'])
@auth.login_required
def get_school():
    """
        获取学校
        ---
        tags:
          - AdminSchool
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
    data =get_method(School,like_list=['id','schoolcode', 'name', 'province'])
    return Success(data=data)

#关闭服务学校
@api.route('/show', methods=['DELETE'])
@auth.login_required
def del_school():
    """
    修改学校状态
           ---
           tags:
             - AdminSchool
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
        user = School.query.filter_by(id=id).first_or_404()
        if user.show==0:
            user.show=1
        elif user.show==1:
            user.show=0
    change_school()
    return DeleteSuccess(msg="操作完成!")

#获取服务学校
@api.route('province', methods=['get'])
@auth.login_required
def group_school():
    """
        获取省份
        ---
        tags:
          - AdminSchool
        parameters:
            - in: "header"
              name: "Authorization"
              description: base64加密后的token
              required: true
    """

    a=getschool()

    return Success(data=a)
