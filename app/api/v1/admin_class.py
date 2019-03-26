# -*- coding: utf-8 -*-
# @Time    : 2019/3/14 14:28
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from flask import jsonify, request
from sqlalchemy import desc

from app.libs.error_code import Success, Forbidden, DeleteSuccess, ParameterException
from app.libs.get_method import get_method, get_join_method
from app.libs.redis_method import code_to_school, code_to_province
from app.libs.redprint import Redprint
from app.libs.string_secret import add_secret, untie_secret
from app.libs.token_auth import auth
from app.libs.upload import qiniu_upload_file, aliyun_get_url
from app.models.class_student import ClassStudent
from app.models.class_study import ClassStudy
from app.models.class_subject import ClassSubject
from app.models.class_teach import ClassTeach
from app.models.class_teacher import ClassTeacher

from app.models.user import User
from app.validators.adminforms import DelAdminForm, AdminAuthForm, UserPutForm, ChPassForm, SchoolForm, TeDetailForm, \
    StDetailForm
from app.validators.classforms import PageForm, onePageForm
import json
api = Redprint('admin_class')
#获取老师列表
@api.route('/teacher', methods=['post'])
@auth.login_required
def get_teacher():
    """
        获取用户信息
        ---
        tags:
          - AdminClass
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
    data =get_method(ClassTeacher,like_list=['name','id','school_name'])
    return Success(data=data)

#学生和老师选择学校
@api.route('/school', methods=['POST'])
@auth.login_required
def up_teacher():
    """
       学生和老师选择学校
       ---
       tags:
         - AdminClass
       parameters:
           - in: "header"
             name: "Authorization"
             description: base64加密后的token
             required: true
           - in: "body"
             name: "body"
             description: 学生和老师选择学校
             required: true
             schema:
               type: "object"
               properties:
                    duid:
                       type: "int"
                       example: 10
                    school_id:
                       type: "string"
                       example: "0535"
                    auth:
                       type: "int"
                       example: 1

    """
    form=SchoolForm().validate_for_api()
    school_id=form.school_id.data
    duid = form.duid.data
    auth=form.auth.data
    if auth==2:
        Big = ClassTeacher
    elif auth==1:
        Big = ClassStudent
    else:
        raise ParameterException()
    Big.query.filter_by(id=duid).first_or_401()
    data = Big().create(duid, school_id)
    return Success(data=data)

#获取未审核学生信息
@api.route('/stauth', methods=['post'])
@auth.login_required
def get_au_student():
    """
        获取未审核学生信息
        ---
        tags:
          - AdminClass
        parameters:
            - in: "header"
              name: "Authorization"
              description: base64加密后的token
              required: true
            - in: "body"
              name: "body"
              description: 获取未审核学生信息
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
        ClassStudent.isauth==2
    }
    data =get_method(ClassStudent,like_list=['name','id', 'sno', 'school_name', 'major', 'grade', 'classno'],filt=filt)
    return Success(data=data)

#获取学生列表
@api.route('/student', methods=['post'])
@auth.login_required
def get_student():
    """
        获取用户信息
        ---
        tags:
          - AdminClass
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
    data =get_method(ClassStudent,like_list=['name','id', 'sno', 'school_name', 'major', 'grade', 'classno'])
    return Success(data=data)

# 获取单个学生
@api.route('/student/<int:duid>/<int:au>', methods=['GET'])
@auth.login_required
def onestudent(duid,au):
    """
               详情接口
               ---
               tags:
                 - AdminClass
               parameters:
                   - in: "header"
                     name: "Authorization"
                     description: base64加密后的token
                     required: true
                   - name: "duid"
                     in: "path"
                     description: "学生/老师id"
                     required: true
                     type: "int"
                   - name: "au"
                     in: "path"
                     description: "权限 1为学生 2 为老师"
                     required: true
                     type: "int"

           """
    if au==2:
        Big = ClassTeacher
    elif au==1:
        Big = ClassStudent
    else:
        raise ParameterException()
    big=Big.query.join(User,Big.user_id==User.id).filter(Big.id==duid).add_entity(User).first_or_404()
    return Success(data=big)
@api.route('/province/<string:code>', methods=['get'])
@auth.login_required
def province(code):
    """
            获取用户信息
            ---
            tags:
              - AdminClass
            parameters:
                - in: "header"
                  name: "Authorization"
                  description: base64加密后的token
                  required: true
                - name: "code"
                  in: "path"
                  description: "ID of pet to return"
                  required: true
                  type: "string"

        """
    return jsonify(code_to_province(code))
#禁用学生或老师
@api.route('/limitau', methods=['DELETE'])
@auth.login_required
def limitau():
    """
       禁用学生或老师
       ---
       tags:
         - AdminClass
       parameters:
           - in: "header"
             name: "Authorization"
             description: base64加密后的token
             required: true
           - in: "body"
             name: "body"
             description: 学生和老师选择学校
             required: true
             schema:
               type: "object"
               properties:
                    duid:
                       type: "int"
                       example: 10
                    au:
                       type: "int"
                       example: 1

    """
    form=AdminAuthForm().validate_for_api()
    duid = form.duid.data
    au=form.au.data
    if au==2:
        Big = ClassTeacher
    elif au==1:
        Big = ClassStudent
    else:
        raise ParameterException()
    big=Big.query.filter_by(id=duid).first_or_404()
    if big.status==1:
        big.status = 0
    elif big.status==0:
        big.status = 1
    else:
        ParameterException()
    return DeleteSuccess(msg="操作完成!")

#修改老师信息
@api.route('/tedetail', methods=['post'])
@auth.login_required
def tedetail():
    """
        修改老师信息
        ---
        tags:
          - AdminClass
        parameters:
            - in: "header"
              name: "Authorization"
              description: base64加密后的token
              required: true
            - in: "body"
              name: "body"
              description: 修改老师信息
              required: true
              schema:
                type: "object"
                properties:
                    duid:
                       type: "int"
                       example: 10
                    head_url:
                       type: "string"
                       example: "-id"
                    abstract:
                       type: "string"
                       example: "-id"
                    name:
                       type: "string"
                       example: "-id"
                    school_id:
                       type: "string"
                       example: "12"
    """

    form = TeDetailForm().validate_for_api()
    duid=form.duid.data
    head_url = form.head_url.data
    if head_url is not None and head_url  is not '':
        head_url = (json.loads(untie_secret(head_url)))[0]["name"]
    abstract = form.abstract.data
    name = form.name.data
    school_id = form.school_id.data
    teacher=ClassTeacher.query.filter_by(id=duid).first_or_404("不存在该老师")
    teacher.admin(head_url, abstract, name, school_id)
    return Success(data=teacher)
#修改学生信息
@api.route('/stdetail', methods=['post'])
@auth.login_required
def stdetail():
    """
        修改学生信息
        ---
        tags:
          - AdminClass
        parameters:
            - in: "header"
              name: "Authorization"
              description: base64加密后的token
              required: true
            - in: "body"
              name: "body"
              description: 修改学生信息
              required: true
              schema:
                type: "object"
                properties:
                    duid:
                       type: "int"
                       example: 10
                    auth_url:
                       type: "string"
                       example: "头像"
                    sno:
                       type: "string"
                       example: "学号"
                    school_id:
                       type: "string"
                       example: "-id"
                    name:
                       type: "string"
                       example: "学生名字"
                    major:
                       type: "string"
                       example: "12"
                    grade:
                       type: "string"
                       example: "12"
                    classno:
                       type: "string"
                       example: "12"
    """
    form = StDetailForm().validate_for_api()
    duid=form.duid.data
    auth_url = form.auth_url.data

    if auth_url is not None and auth_url  is not '':
        auth_url = (json.loads(untie_secret(auth_url)))[0]["name"]
    sno = form.sno.data
    school_id = form.school_id.data
    name = form.name.data
    major = form.major.data
    grade = form.grade.data
    classno = form.classno.data
    student=ClassStudent.query.filter_by(id=duid).first_or_404()
    student.admin(auth_url,sno,school_id,name,major,grade,classno)
    return jsonify(student)

#获取班级列表
@api.route('/tesubject', methods=['post'])
@auth.login_required
def get_tesubject():
    """
        老师获取班级列表
        ---
        tags:
          - AdminClass
        parameters:
            - in: "header"
              name: "Authorization"
              description: base64加密后的token
              required: true
            - in: "body"
              name: "body"
              description: 老师获取班级列表
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
                    duid:
                       type: "int"
                       example: 1
    """
    form = onePageForm().validate_for_api()
    que=ClassSubject.query.join(ClassTeach,ClassTeach.subject_id==ClassSubject.id)
    Big=ClassSubject
    filt={
        ClassTeach.teacher_id==form.duid.data
    }
    data =get_join_method(Big,que,form,like_list=['id', 'name', 'invitation', 'abstract','sub_status'],filt=filt)
    return Success(data=data)

#获取老师列表
@api.route('/stsubject', methods=['post'])
@auth.login_required
def get_stsubject():
    """
        获取学生班级
        ---
        tags:
          - AdminClass
        parameters:
            - in: "header"
              name: "Authorization"
              description: base64加密后的token
              required: true
            - in: "body"
              name: "body"
              description: 获取学生班级
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
                    duid:
                       type: "int"
                       example: 1
    """
    form = onePageForm().validate_for_api()
    que = ClassSubject.query.join(ClassStudy, ClassStudy.subject_id == ClassSubject.id)
    Big = ClassSubject
    filt = {
        ClassTeach.teacher_id == form.duid.data
    }
    data = get_join_method(Big, que, form, like_list=['id', 'name', 'invitation', 'abstract','sub_status'], filt=filt)
    return Success(data=data)


#获取全部班级
@api.route('/subjectall', methods=['post'])
@auth.login_required
def get_subjectall():
    """
        获取全部班级
        ---
        tags:
          - AdminClass
        parameters:
            - in: "header"
              name: "Authorization"
              description: base64加密后的token
              required: true
            - in: "body"
              name: "body"
              description: 获取全部班级
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

    data =get_method(ClassSubject,like_list=['id', 'name', 'invitation', 'abstract','sub_status'])
    return Success(data=data)


