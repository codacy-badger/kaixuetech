# -*- coding: utf-8 -*-
# @Time    : 2019/3/18 11:35
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from flask import g

from app.libs.error_code import Success, ParameterException
from app.libs.secrect import upid, addid
from app.libs.token_auth import auth
from app.models.course_info import CourseInfo
from app.models.course_pape_mid_ques import PaperMidQuestion
from app.models.course_paper import CoursePaper
from app.models.course_question import CourseQuestion
from app.models.course_student import CourseStudent
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

    hasanswe = {
        1:__validate_for_ONE_SELECT,
        2:__validate_for_MORE_SELECT,
        3: __validate_for_JUDGE,
        4: __validate_for_ONE_SELECT,
        5: __validate_for_MORE_SELECT,
        6:__validate_for_Str,
        7:__validate_for_ONE_SELECT,
        8:__validate_for_Str,
        9:__validate_for_Str
    }
    for item in answer:
        genre=item["genre"]
        answer1=item["ans"]
        try:
            hasanswe[genre](answer1)
        except:
            pass
    # 题目类型 1:单选投票题 2多选投票 3判断题 4单选题 5 多选题 6简答题 7 数值评价题 8 匿名开放题 9拍照题
    import json
    answe=json.dumps(answer)
    course_student=CourseStudent.add(uid,paper_id,answe)
    return Success(data=course_student)

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
                           example: "eyJhbGciOiJIUzI1NiIsImlhdCI6MTU1Mjk4ODQwOSwiZXhwIjoxNTUyOTkyMDA5fQ.eyJzdWJqZWN0IjoxfQ.vOCu8HiiYc8um0bRPeqS9Heas3L-6JnQaaZA_RLs7ZE"
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
    ques=CourseQuestion.query.join(PaperMidQuestion,
                              PaperMidQuestion.question_id==CourseQuestion.id
                          ).filter(
        PaperMidQuestion.paper_id==paper_info_id
    ).all()
    data={'paper_id':paper_info_id}
    secret_id=addid(data)

    quest=[i.jsonstr() for i in ques]

    data = {'question': quest,
            'secret_id': secret_id}
    return Success(data=data)

def __validate_for_JUDGE(answer):
    ans = ["0", "1"]
    if answer not in ans:
        raise ParameterException(msg="参数错误！")


def __validate_for_ONE_SELECT(answer):
    try:
        int(answer)
    except:
        raise ParameterException(msg="参数错误！")


def __validate_for_MORE_SELECT(answer):
    from ast import literal_eval
    mlist = literal_eval(answer)
    if not isinstance(mlist, list):
        raise ParameterException(msg="参数错误！")
    try:
        sum(mlist)
    except:
        raise ParameterException(msg="参数错误！")
def __validate_for_Str(answer):
    pass
