# -*- coding: utf-8 -*-
# @Time    : 2019/3/18 11:35
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from flask import g
import os

from sqlalchemy import desc
from app.libs.Time import Time
from app.libs.error_code import Success, NotFound, ParameterException
from app.libs.token_auth import auth
from app.models.course_info import CourseInfo
from app.models.course_pape_mid_ques import PaperMidQuestion
from app.models.course_paper import CoursePaper
from app.models.course_question import CourseQuestion
from app.models.course_ware import CourseWare
from app.models.duration import Duration
from app.validators.forms import QuestionForm, TeCourseForm, GetQuesForm
from . import api

# 创建课程
@api.route('/course', methods=['POST'])
@auth.login_required
def teacher_course():
    """
           老师添加课程
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
                 description: 老师添加课程
                 required: true
                 schema:
                   type: "object"
                   properties:
                       chi_id:
                           type: "int"
                           example: 12
                       kin:
                           type: "int"
                           example: 1
    """
    uid = g.user.uid

    form = TeCourseForm().validate_for_api()
    chi_id = form.chi_id.data
    kin = form.kin.data
    kin=kin-1
    if kin==0:
        #课件动态
        duration = Duration.query.filter_by(id=chi_id, userid=uid).first_or_404()
        name = os.path.splitext(duration.old_name)[0]
        child_id = duration.id
        subject_id = duration.subject_id

        courseinfo = CourseInfo.add(name=name,kind=kin,child_id=child_id,subject_id=subject_id)
        return Success(data=courseinfo, msg="课程创建成功")
    else:
        return NotFound("功能还未开放！")

# 添加测试互动
@api.route('/question', methods=['POST'])
@auth.login_required
def teacher_question():
    """
           添加试题
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
                 description: 添加试题
                 required: true
                 schema:
                   type: "object"
                   properties:
                       course_id:
                           type: "int"
                           example: 1
                       page:
                           type: "int"
                           example: 1
                       genre:
                           type: "int"
                           example: 1
                       questiontext:
                           type: "string"
                           example: "今天吃什么？"
                       answer:
                           type: "string"
                           example: "1"

                       option:
                           type: "array"
                           description: The awesomeness list
                           items:
                                type: "object"
                                properties:
                                    order_num:
                                        type: "int"
                                        example: 1
                                    opt_cont:
                                        type: "string"
                                        example: "我是一个选项"



    """
    uid = g.user.uid
    form = QuestionForm().validate_for_api()
    course_id=form.course_id.data
    page = form.page.data
    genre = form.genre.data
    questiontext = form.questiontext.data
    answer = form.answer.data
    options = form.option.data

    try:
        data = [int(option['order_num']) for option in options]
    except:
        raise ParameterException("序号有误！")
    data = sorted(data)
    data1 = [x + 1 for x in range(len(data))]

    if data != data1:
        raise ParameterException("序号有误！")

    # 查询考卷是否初始化了
    courseware=CourseWare.query.filter_by(course_info_id=course_id,ware_page=page,user_id=uid).first()
    if courseware is None:
        # 初始化考卷
        paper=CoursePaper.add(str(page))
        courseware=CourseWare.add(course_id,page,paper,uid)

    paper_id=courseware.paper_info_id


    # 1:单选投票题 2多选投票 3判断题 4单选题 5 多选题 6简答题 7数值评价题 8 匿名开放题 9拍照题
    hasanswe = {
        3: __validate_for_JUDGE,
        4: __validate_for_ONE_SELECT,
        5: __validate_for_MORE_SELECT
    }
    try:
        hasanswe[genre](answer)
    except:
        pass
    # 判断有没有这个序号
    a=PaperMidQuestion.query.order_by(desc(PaperMidQuestion.order_num)).filter_by(paper_id=paper_id).first()
    if a is None:
        order_num=1
    else:
        order_num=a.order_num+1
    # 添加题目
    import json
    option = json.dumps(options)
    coursequestion = CourseQuestion.add(genre, questiontext, answer, option)
    # 添加题目中间表
    PaperMidQuestion.add(paper_id, coursequestion, order_num, uid)
    return Success(msg="添加成功",data=coursequestion)



#查询所有试卷通过 courid
@api.route('/getpaper', methods=['POST'])
@auth.login_required
def teacher_getpaper():
    """
          查询所有试卷通过 couri
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
                 description: 查询所有试卷通过 couri
                 required: true
                 schema:
                   type: "object"
                   properties:
                       id:
                           type: "int"
                           example: 1

    """
    uid = g.user.uid
    form = GetQuesForm().validate_for_api()
    course_id=form.id.data

    coursepaper = CoursePaper.query.join(CourseWare,
                                         CourseWare.paper_info_id==CoursePaper.id
                                         ).filter(CourseWare.course_info_id==course_id,
                                          CourseWare.user_id==uid
                                                  ).all()
    return Success(data=coursepaper)


#查询所有题目通过 paper_id
@api.route('/getquestion', methods=['POST'])
@auth.login_required
def teacher_getquestion():
    """
           查询所有题目通过 paper_id
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
                 description: 查询所有题目通过 courid
                 required: true
                 schema:
                   type: "object"
                   properties:
                       id:
                           type: "int"
                           example: 1

    """
    uid = g.user.uid
    form = GetQuesForm().validate_for_api()
    paper_id=form.id.data

    qusetion = CourseQuestion.query.join(PaperMidQuestion,
                                            PaperMidQuestion.question_id==CourseQuestion.id
                                         ).filter(PaperMidQuestion.paper_id==paper_id,
                                                  PaperMidQuestion.user_id==uid
                                                  ).order_by(PaperMidQuestion.order_num).all()


    return Success(data=qusetion)


#开始测试 通过考卷id
#查询所有题目通过 paper_id
@api.route('/start', methods=['POST'])
@auth.login_required
def teacher_start():
    """
           查询所有题目通过 paper_id
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
                 description: 查询所有题目通过 courid
                 required: true
                 schema:
                   type: "object"
                   properties:
                       id:
                           type: "int"
                           example: 1

    """
    uid = g.user.uid
    form = GetQuesForm().validate_for_api()
    paper_id=form.id.data
    qusetion = CoursePaper.query.join(CourseWare,
                                      CourseWare.paper_info_id==CoursePaper.id
                                         ).filter(CourseWare.paper_info_id==paper_id,
                                                  CourseWare.user_id==uid,
                                                  CoursePaper.paper_state==0
                                                  ).first_or_404()
    qusetion.paper_state=1
    qusetion.start_time=Time().now()
    return Success(data=qusetion)


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