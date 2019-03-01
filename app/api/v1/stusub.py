# -*- coding: utf-8 -*-
# @Time    : 2019/2/27 15:44
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from flask import g


from app.libs.error_code import Success, ParameterException
from app.libs.redprint import Redprint
from app.libs.token_auth import auth, verify_auth_token
from app.models.student import Student
from app.models.studentes_middle_subject import Studentes_Middle_Subject
from app.models.subject import Subject
from app.validators.forms import invitationForm, invitation2Form

api = Redprint('stusub')

@api.route('', methods=['POST'])
@auth.login_required
def add():
    """
           添加选课信息
           ---
           tags:
             - StuSub
           parameters:
               - in: "header"
                 name: "Authorization"
                 description: base64加密后的token
                 required: true
               - in: "body"
                 name: "body"
                 description: 添加选课信息
                 required: true
                 schema:
                   type: "object"
                   properties:
                       invi:
                           type: "string"
                           example: "D6FQEC"

    """
    uid = g.user.uid
    form = invitationForm().validate_for_api()
    Studentes_Middle_Subject.query.filter_by(student_id=uid ,invitation =form.invi.data,sub_status=1).first_or_401()
    subject = Subject.query.filter_by(invitation=form.invi.data).first_or_404()
    student = Student.query.filter_by(user_id=uid).first_or_404()

    data=Studentes_Middle_Subject.addstusub(subjects=subject,
                                            students=student,
                                            invitation=form.invi.data)
    return Success(data=data)

# @api.route('/<string:token>/<string:invi>', methods=['get'])
#
# def add_by_qr(token,invi):
#     """
#        归档课程信息
#        ---
#        tags:
#          - StuSub
#        parameters:
#          - name: "token"
#            in: "path"
#            description: 令牌
#            required: true
#            type: "string"
#          - name: "invi"
#            in: "path"
#            description: 随机码
#            required: true
#            type: "string"
#
#      """
#     uid = verify_auth_token(token).uid
#     if len(invi)!=6:
#         raise ParameterException()
#     StuSub.query.filter_by(student_id=uid, invitation=invi).first_or_401()
#     subject = Subject.query.filter_by(invitation=invi).first_or_404().append('user_id')
#     StuSub.addstusub(student_id=uid,
#                      subject_id=subject.id,
#                      teacher_id=subject.user_id,
#                      invitation=invi)
#     return Success()