# -*- coding: utf-8 -*-
# @Time    : 2019/3/15 13:50
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from flask import g

from app.api.v1.attend import api
from app.libs.Time import Time
from app.libs.error_code import Success, RepeatException1
from app.libs.redis_method import school_to_code, Student_Attend_Redis
from app.libs.token_auth import auth
from app.models.attend_info import AttendInfo
from app.models.attend_student import AttendStudent
from app.validators.forms import StudentAttendForm

"""
学生签到
"""
@api.route('/stattend/', methods=['POST'])
@auth.login_required
def student_attend():
    """
           学生签到
           ---
           tags:
             - Attend
           parameters:
               - in: "header"
                 name: "Authorization"
                 description: base64加密后的token
                 required: true
               - in: "body"
                 name: "body"
                 description: 学生签到
                 required: true
                 schema:
                   type: "object"
                   properties:
                       code:
                            type: "string"
                            example: "6607"
                       attend_position:
                             type: "string"
                             example: "116.414617,39.943485"
                       scl_name:
                             type: "string"
                             example: "北京工业大学"
                       ip:
                             type: "string"
                             example: "112.17.240.35"
    """
    uid = g.user.uid
    form = StudentAttendForm().validate_for_api()
    ip=form.ip.data
    school_name=form.scl_name.data
    attend_position=form.attend_position.data
    code=form.code.data
    school_code = school_to_code(school_name)
    date = Time().nowdate()
    attend_number = school_code + date + code
    a=Student_Attend_Redis.student_attend_get(attend_number, uid)
    if a!=0:
        raise RepeatException1("请勿重复签到！")
    atstuent=AttendStudent.query.join(AttendInfo,AttendStudent.attend_id==AttendInfo.id).filter(
        AttendStudent.user_id==uid,
        AttendStudent.attend_state == 0,
        AttendInfo.attend_number_secret==attend_number,
        AttendInfo.attend_state!=0).add_entity(AttendInfo).first_or_404()
    atstuent[0].attend_position = attend_position
    atstuent[0].attend_ipattend_ip = ip
    atstuent[0].attend_time = Time().now()
    if ip=='0,0':
        atstuent[0].attend_position_state = 0
    else:
        atstuent[0].attend_position_state = 1
    if atstuent[1].attend_state==1:
        # 签到中
        atstuent[0].attend_state=1
    else:
        #签到结束
        atstuent[0].attend_state = 4
    Student_Attend_Redis.student_attend_add(attend_number,uid)
    return Success(data=atstuent, msg="签到成功！")

