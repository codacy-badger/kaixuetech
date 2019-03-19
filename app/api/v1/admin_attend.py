# -*- coding: utf-8 -*-
# @Time    : 2019/3/18 16:47
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from app.libs.error_code import Success
from app.libs.get_method import get_method, get_join_method
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.attend_info import AttendInfo
from app.models.attend_student import AttendStudent
from app.models.attend_subject import AttendSubject
from app.models.class_student import ClassStudent
from app.validators.classforms import onePageForm
from app.validators.forms import TeacherEndAttendForm

api = Redprint('admin_attend')

#获取签到表
@api.route('/attendall', methods=['post'])
@auth.login_required
def get_attendall():
    """
        获取签到表
        ---
        tags:
          - AdminAttend
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
    """
    data =get_method(AttendInfo,like_list=['id', 'attend_name',  'attend_number', 'attend_state'])

    return Success(data=data)


#获取老师签到表
@api.route('/teattend', methods=['post'])
@auth.login_required
def get_teattend():
    """
        获取老师签到表
        ---
        tags:
          - AdminAttend
        parameters:
            - in: "header"
              name: "Authorization"
              description: base64加密后的token
              required: true
            - in: "body"
              name: "body"
              description: #获取老师签到表
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
    que = AttendInfo.query.join(AttendSubject, AttendSubject.attend_id == AttendInfo.id)
    Big = AttendInfo
    filt = {
        AttendSubject.subject_id == form.duid.data
    }
    data = get_join_method(Big, que, form, like_list=['id', 'attend_name',  'attend_number', 'attend_state'], filt=filt)
    return Success(data=data)

#获取签到情况签到表id
@api.route('/stattend', methods=['post'])
@auth.login_required
def get_stattend():
    """
        获取签到情况 通过签到表id
        ---
        tags:
          - AdminAttend
        parameters:
            - in: "header"
              name: "Authorization"
              description: base64加密后的token
              required: true
            - in: "body"
              name: "body"
              description: 获取签到情况 通过签到表id
              required: true
              schema:
                type: "object"
                properties:
                    attend_id:
                       type: "int"
                       example: 1
    """
    form = TeacherEndAttendForm().validate_for_api()
    attendstudent = AttendStudent.query.join(ClassStudent, AttendStudent.student_id == ClassStudent.id)
    student=attendstudent.filter(AttendStudent.attend_id==form.attend_id.data).add_entity(ClassStudent).all()
    return Success(data=student)