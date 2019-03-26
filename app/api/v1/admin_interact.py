# -*- coding: utf-8 -*-
# @Time    : 2019/3/20 13:43
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from flask import jsonify

from app.libs.error_code import Success
from app.libs.get_method import get_method, get_join_method
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.course_info import CourseInfo
from app.models.course_pape_mid_ques import PaperMidQuestion
from app.models.course_paper import CoursePaper
from app.models.course_question import CourseQuestion
from app.models.course_ware import CourseWare
from app.validators.classforms import onePageForm
from app.validators.forms import DeleteOneForm, DeletetwoForm

api = Redprint('admin_interact')

#获取文件
@api.route('/interact', methods=['post'])
@auth.login_required
def get_interact():
    """
        获取互动
        ---
        tags:
          - AdminInteract
        parameters:
            - in: "header"
              name: "Authorization"
              description: base64加密后的token
              required: true
            - in: "body"
              name: "body"
              description: 获取互动
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
    data =get_method(CourseInfo,like_list=['id', 'name','subject_id','kind','child_id'])
    return Success(data=data)

#获取全部试卷
@api.route('/paper', methods=['post'])
@auth.login_required
def get_paper():
    """
        获取全部试卷
        ---
        tags:
          - AdminInteract
        parameters:
            - in: "header"
              name: "Authorization"
              description: base64加密后的token
              required: true
            - in: "body"
              name: "body"
              description: 获取全部试卷
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
    data =get_method(CoursePaper,like_list=['id', 'name','paper_state'])
    return Success(data=data)

#获取全部试卷
@api.route('/question', methods=['post'])
@auth.login_required
def get_question():
    """
        获取全部题目
        ---
        tags:
          - AdminInteract
        parameters:
            - in: "header"
              name: "Authorization"
              description: base64加密后的token
              required: true
            - in: "body"
              name: "body"
              description: 获取全部题目
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
    data =get_method(CourseQuestion,like_list=['id', 'genre','answer','questiontext','option'])

    def to_json(dat):
        dat=dat.adminjsonstr()
        return dat
    items=data["items"]
    data["items"]=list(map(to_json,items))
    return Success(data=data)

#通过试卷id查找题目
@api.route('/questionid', methods=['post'])
@auth.login_required
def get_questionid():
    """
        通过试卷id查找题目
        ---
        tags:
          - AdminInteract
        parameters:
            - in: "header"
              name: "Authorization"
              description: base64加密后的token
              required: true
            - in: "body"
              name: "body"
              description: 通过试卷id查找题目
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
    que = CourseQuestion.query.join(PaperMidQuestion, PaperMidQuestion.question_id == CourseQuestion.id)
    Big = CourseQuestion
    filt = {
        PaperMidQuestion.paper_id == form.duid.data,
        PaperMidQuestion.status==1
    }
    data = get_join_method(Big, que, form, like_list=['id', 'genre','answer','questiontext','option'], filt=filt)
    def to_json(dat):
        dat=dat.adminjsonstr()
        return dat
    items=data["items"]
    data["items"]=list(map(to_json,items))
    return Success(data=data)

#删除题目
@api.route('/delques', methods=['DELETE'])
@auth.login_required
def del_question():
    """
        通过试卷删除题目
        ---
        tags:
          - AdminInteract
        parameters:
            - in: "header"
              name: "Authorization"
              description: base64加密后的token
              required: true
            - in: "body"
              name: "body"
              description: 通过试卷删除题目 id 问题id  id2试卷id
              required: true
              schema:
                type: "object"
                properties:
                    id:
                       type: "int"
                       example: 1
                    id2:
                       type: "int"
                       example: 1
    """
    form = DeletetwoForm().validate_for_api()
    id=form.id.data
    id2 = form.id2.data
    #查找
    midquestion=PaperMidQuestion.query.join(CourseQuestion,
                                            CourseQuestion.id==PaperMidQuestion.question_id
                                            ).filter(CourseQuestion.id==id,
                                                     PaperMidQuestion.paper_id==id2,
                                                     PaperMidQuestion.status==1
                                                     ).first_or_404()

    midquestion.delete()
    return Success(msg="删除成功！")


#删除试卷
@api.route('/delpaper', methods=['DELETE'])
@auth.login_required
def del_paper():
    """
        删除试卷
        ---
        tags:
          - AdminInteract
        parameters:
            - in: "header"
              name: "Authorization"
              description: base64加密后的token
              required: true
            - in: "body"
              name: "body"
              description: 删除试卷 id 试卷id
              required: true
              schema:
                type: "object"
                properties:
                    id:
                       type: "int"
                       example: 1

    """
    form = DeleteOneForm().validate_for_api()
    id=form.id.data

    #查找

    midquestion=PaperMidQuestion.query.join(CoursePaper,
                                            CoursePaper.id==PaperMidQuestion.paper_id
                                            ).filter(CoursePaper.id==id,
                                                     PaperMidQuestion.status==1
                                                     ).join(CourseWare,
                                                            CourseWare.paper_info_id==CoursePaper.id
                                                            ).add_entity(CoursePaper).add_entity(CourseWare).all()
    midquestion[0][1].delete()
    midquestion[0][2].delete()
    for item in midquestion:
        item[0].delete()
    return Success(msg="删除成功！")

@api.route('/subinte', methods=['POST'])
@auth.login_required
def subinte():
    """
        通过学科id查找互动
        ---
        tags:
          - AdminInteract
        parameters:
            - in: "header"
              name: "Authorization"
              description: base64加密后的token
              required: true
            - in: "body"
              name: "body"
              description: 通过学科id查找互动
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
    que = CourseInfo.query
    Big = CourseInfo
    filt = {
        CourseInfo.subject_id == form.duid.data
    }
    data = get_join_method(Big, que, form, like_list=['id', 'name','subject_id','kind','child_id','create_time','change_num'], filt=filt)
    return Success(data=data)