# -*- coding: utf-8 -*-
# @Time    : 2019/3/14 13:01
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from flask import g
from app.api.v1.classs import api
from app.libs.error_code import Success
from app.libs.ran_num import random_code, code_update, get_code_id
from app.libs.token_auth import auth
from app.models.class_student import ClassStudent
from app.models.class_study import ClassStudy
from app.models.class_subject import ClassSubject
from app.models.class_teach import ClassTeach
from app.models.class_teacher import ClassTeacher
from app.validators.adminforms import invitationForm
from app.validators.classforms import  SubjectForm


@api.route('/teach', methods=['POST'])
@auth.login_required
def teacher_subject_creat():
    """
       添加科目
       ---
       tags:
         - Class
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
                   name:
                       type: "string"
                       example: "高等数学"

       """
    uid = g.user.uid
    form = SubjectForm().validate_for_api()
    name=form.name.data
    # 判断是不是老师
    teacher = ClassTeacher.query.filter_by(user_id=uid).first_or_404("还未注册老师")
    invitation = random_code()

    # 创建课堂
    subject=ClassSubject.add(invitation,name)
    code_update(invitation,subject.id)
    #选课
    teach=ClassTeach.add(subject.id,teacher.id,uid)
    return Success(msg="课堂添加成功！",data=teach)

@api.route('/study', methods=['POST'])
@auth.login_required
def student_subject_creat():
    """
           学生选课
           ---
           tags:
             - Class
           parameters:
               - in: "header"
                 name: "Authorization"
                 description: base64加密后的token
                 required: true
               - in: "body"
                 name: "body"
                 description: 学生选课
                 required: true
                 schema:
                   type: "object"
                   properties:
                       invi:
                           type: "string"
                           example: "QBD7PM"

    """
    uid = g.user.uid
    #是否创建学生了
    form = invitationForm().validate_for_api()
    student=ClassStudent().query.filter_by(user_id=uid).first_or_404("还未注册学生")


    invi=(form.invi.data)
    subject_id=(get_code_id(invi))
    # 选课
    study=ClassStudy.add(student.id,subject_id,uid)
    return Success(data=study,msg="选课成功！")