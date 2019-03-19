# -*- coding: utf-8 -*-
# @Time    : 2019/3/18 11:35
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from flask import g

from app.libs.error_code import Success, ParameterException
from app.libs.secrect import upid
from app.libs.token_auth import auth
from app.models.course_info import CourseInfo
from app.models.course_paper import CoursePaper
from app.models.course_ware import CourseWare
from app.validators.forms import AnswerForm, TestForm
from . import api




# 学生提交答案
@api.route('/stanswer', methods=['POST'])
@auth.login_required
def student_answer():
    """
           回答问题
           ---
           tags:
             - Interaction
           parameters:
               - in: "header"
                 name: "Authorization"
                 description: base64加密后的token
                 required: true
               - in: "body"
                 name: "body"
                 description: 回答问题
                 required: true
                 schema:
                   type: "object"
                   properties:
                       paper_id:
                           type: "int"
                           example: 1
                       answer:
                           type: "array"
                           description: The awesomeness list
                           items:
                                type: "object"
                                properties:
                                    ques_id:
                                        type: "int"
                                        example: 1
                                    ans:
                                        type: "string"
                                        example: "1"
                                    genre:
                                        type: "string"
                                        example: "1"
    """
    uid = g.user.uid
    form = AnswerForm().validate_for_api()
    paper_id=form.paper_id.data
    answer = form.answer.data
    #判断有没有考卷

    return Success()

#获取考试题目 通过课堂id
@api.route('/stpaper', methods=['POST'])
@auth.login_required
def student_paper():
    """
           获取考试题目 通过课堂id
           ---
           tags:
             - Interaction
           parameters:
               - in: "header"
                 name: "Authorization"
                 description: base64加密后的token
                 required: true
               - in: "body"
                 name: "body"
                 description: 获取考试题目 通过课堂id
                 required: true
                 schema:
                   type: "object"
                   properties:
                       sec_id:
                           type: "string"
                           example: "b'eyJhbGciOiJIUzI1NiIsImlhdCI6MTU1Mjk4NTI2NywiZXhwIjoxNTUyOTg4ODY3fQ.eyJzdWJqZWN0IjoxfQ.RC7FBPqogRSOTEJyQIuq1CTQzWIkTm72SV_GzwTCEN4'"
                       subject_id:
                           type: "int"
                           example: 1
    """
    form = TestForm().validate_for_api()
    sec_id=form.sec_id.data
    subject_id = form.subject_id.data
    try:
        sec_id=upid(sec_id)["subject"]
        if subject_id != sec_id:
            raise ParameterException()
    except:
        raise ParameterException()
    ware=CourseWare.query.join(CoursePaper,
                          CourseWare.paper_info_id==CoursePaper.id
                          ).join(CourseInfo,CourseWare.course_info_id==CourseInfo.id).filter(
                                  CoursePaper.paper_state==1,
                                 CourseInfo.subject_id==subject_id,
                                                                                    ).first_or_404("暂时无新互动！")
    paper_info_id=ware.paper_info_id



    return Success(data=ware)