# # -*- coding: utf-8 -*-
# # @Time    : 2019/3/7 18:04
# # @Author  : 昨夜
# # @Email   : 903165495@qq.com
# import operator
#
# from flask import g, jsonify
# import os
#
#
# from app.libs.error_code import Success, ParameterException, RepeatException1
# from app.libs.redis_method import Student_Answer_Redis
# from app.libs.redprint import Redprint
# from app.libs.token_auth import auth
# from app.models.course_info import CourseInfo
# from app.models.course_pape_mid_ques import PaperMidQuestion
# from app.models.course_paper import CoursePaper
# from app.models.course_question import CourseQuestion
# from app.models.course_student import CourseStudent
# from app.models.course_ware import CourseWare
# from app.models.duration import Duration
# from app.models.studentes_middle_subject import Studentes_Middle_Subject
# from app.validators.forms import CourseForm, PaperForm, QuestionForm
# from app.validators.getforms import isint
# import json
#
# api = Redprint('interaction')
#
#
# # 共同方法
# def paperadd(course_info_id, ware_page, uid):
#     # 判断是否重复添加
#     CourseWare.query.filter_by(course_info_id=course_info_id, ware_page=ware_page).first_or_401()
#     # 判断是否存在课程
#     courseinfo = CourseInfo.query.filter_by(id=course_info_id).first_or_404()
#     # 添加考试
#     coursepaper = CoursePaper.add(name=str(ware_page))
#     # 添加课程考试中间表
#     CourseWare().add(courseinfo, ware_page, coursepaper, uid)
#
#
# # 创建课程
# @api.route('/course', methods=['POST'])
# @auth.login_required
# def course():
#     """
#            添加课程
#            ---
#            tags:
#              - Interaction
#            parameters:
#                - in: "header"
#                  name: "Authorization"
#                  description: base64加密后的token
#                  required: true
#                - in: "body"
#                  name: "body"
#                  description: 提交新的密码
#                  required: true
#                  schema:
#                    type: "object"
#                    properties:
#                        duration_id:
#                            type: "int"
#                            example: 12
#     """
#     uid = g.user.uid
#     form = CourseForm().validate_for_api()
#     duration = Duration.query.filter_by(id=form.duration_id.data, userid=uid).first_or_403()
#     name = os.path.splitext(duration.old_name)[0]
#     duration_id = duration.id
#     subject_id = duration.subject_id
#     courseinfo = CourseInfo.add(name, duration_id, subject_id)
#     return Success(data=courseinfo, msg="课程创建成功")
#
#
# # 查询课程下的所有题目
# @api.route('/<int:cos_id>/course', methods=['get'])
# @auth.login_required
# def courseget(cos_id):
#     """
#         归档课程信息
#         ---
#         tags:
#           - Interaction
#         parameters:
#           - in: "header"
#             name: "Authorization"
#             description: base64加密后的token
#             required: true
#           - name: "cos_id"
#             in: "path"
#             description: 课程id
#             required: false
#             type: "int"
#     """
#     isint(cos_id)
#     # uid = g.user.uid
#     coursepaper = CoursePaper.query.join(CourseWare,
#                                          CourseWare.paper_info_id == CoursePaper.id
#                                          ).filter(
#         CourseWare.course_info_id == cos_id
#     ).all()
#
#     return Success(data=coursepaper)
#
#
# # 初始化考卷
# @api.route('/paper', methods=['POST'])
# @auth.login_required
# def paper():
#     """
#            添加考试
#            ---
#            tags:
#              - Interaction
#            parameters:
#                - in: "header"
#                  name: "Authorization"
#                  description: base64加密后的token
#                  required: true
#                - in: "body"
#                  name: "body"
#                  description: 提交新的密码
#                  required: true
#                  schema:
#                    type: "object"
#                    properties:
#                        course_info_id:
#                            type: "int"
#                            example: 1
#                        ware_page:
#                            type: "int"
#                            example: 1
#
#     """
#     uid = g.user.uid
#     form = PaperForm().validate_for_api()
#     course_info_id = form.course_info_id.data
#     ware_page = form.ware_page.data
#     paperadd(course_info_id, ware_page, uid)
#     return Success()
#
#
# # 添加试题
# @api.route('/question', methods=['POST'])
# @auth.login_required
# def question():
#     """
#            添加试题
#            ---
#            tags:
#              - Interaction
#            parameters:
#                - in: "header"
#                  name: "Authorization"
#                  description: base64加密后的token
#                  required: true
#                - in: "body"
#                  name: "body"
#                  description: 添加试题
#                  required: true
#                  schema:
#                    type: "object"
#                    properties:
#                        genre:
#                            type: "int"
#                            example: 1
#                        questiontext:
#                            type: "string"
#                            example: "今天吃什么？"
#                        answer:
#                            type: "string"
#                            example: "1"
#                        paper_id:
#                            type: "int"
#                            example: 1
#                        order_num:
#                            type: "int"
#                            example: 1
#                        option:
#                            type: "array"
#                            description: The awesomeness list
#                            items:
#                                 type: "object"
#                                 properties:
#                                     order_num:
#                                         type: "int"
#                                         example: 1
#                                     opt_cont:
#                                         type: "string"
#                                         example: "我是一个选项"
#
#
#
#     """
#     uid = g.user.uid
#     form = QuestionForm().validate_for_api()
#     genre = form.genre.data
#     questiontext = form.questiontext.data
#     answer = form.answer.data
#     paper_id = form.paper_id.data
#     order_num = form.order_num.data
#     options = form.option.data
#     try:
#         data = [int(option['order_num']) for option in options]
#     except:
#         raise ParameterException()
#     data = sorted(data)
#     data1 = [x + 1 for x in range(len(data))]
#     if data != data1:
#         raise ParameterException()
#     # 1:单选投票题 2多选投票 3判断题 4单选题 5 多选题 6简答题 7数值评价题 8 匿名开放题 9拍照题
#     hasanswe = {
#         3: __validate_for_JUDGE,
#         4: __validate_for_ONE_SELECT,
#         5: __validate_for_MORE_SELECT
#     }
#
#     try:
#         hasanswe[genre](answer)
#     except:
#         raise ParameterException()
#
#     # 判断有没有这个序号
#     PaperMidQuestion.query.filter_by(paper_id=paper_id, order_num=order_num).first_or_401()
#     # 判断有没有这个考卷
#     CourseWare.query.filter_by(paper_info_id=paper_id, user_id=uid).first_or_403()
#     # 添加题目
#     option = json.dumps(options)
#     coursequestion = CourseQuestion.add(genre, questiontext, answer, option)
#     # 添加题目中间表
#     PaperMidQuestion.add(paper_id, coursequestion, order_num, uid)
#     return Success(msg="添加成功")
#
#
# # 学生提交答案
# @api.route('/answer', methods=['POST'])
# @auth.login_required
# def answer():
#     """
#            回答问题
#            ---
#            tags:
#              - Interaction
#            parameters:
#                - in: "header"
#                  name: "Authorization"
#                  description: base64加密后的token
#                  required: true
#                - in: "body"
#                  name: "body"
#                  description: 回答问题
#                  required: true
#                  schema:
#                    type: "object"
#                    properties:
#                        ware_id:
#                            type: "int"
#                            example: 1
#                        answer:
#                            type: "array"
#                            description: The awesomeness list
#                            items:
#                                 type: "object"
#                                 properties:
#                                     paper_id:
#                                         type: "int"
#                                         example: 1
#                                     ans:
#                                         type: "string"
#                                         example: "1"
#
#
#
#
#
#     """
#     uid = g.user.uid
#     paper_id = 1
#     answer = {1: "1"}
#     da1=Student_Answer_Redis.student_answer_get(str(uid)+','+str(paper_id))
#     if da1 is not None:
#         raise RepeatException1()
#     # 判断有没有这个测试
#     courseinfo = CourseInfo.query.join(CourseWare,
#                                        CourseWare.course_info_id == CourseInfo.id
#                                        ).filter(
#         CourseWare.paper_info_id == paper_id
#     ).first_or_404()
#     subject_id = courseinfo.subject_id
#
#     # 判断学生有没有选课
#     Studentes_Middle_Subject().iselect(subject_id, uid)
#     # 判断答案是否跟答案一致
#     coursepapers = CoursePaper.query.join(PaperMidQuestion, PaperMidQuestion.paper_id == CoursePaper.id).join(
#         CourseQuestion, PaperMidQuestion.question_id == CourseQuestion.id).filter(
#         CoursePaper.id == paper_id).add_entity(PaperMidQuestion).add_entity(CourseQuestion).all()
#     coursepaper = coursepapers[0][0]
#
#     if coursepaper.paper_state != 1:
#         raise ParameterException("不是作答时间！")
#
#     ques_list = [dict(item[1], **item[2]) for item in coursepapers]
#     hasanswe = {
#         1: __validate_for_ONE_SELECT,
#         2: __validate_for_MORE_SELECT,
#         3: __validate_for_JUDGE,
#         4: __validate_for_ONE_SELECT,
#         5: __validate_for_MORE_SELECT,
#         7: __validate_for_ONE_SELECT
#     }
#
#     def creat_start(quer):
#         star = {"id": 1, "answer": "1", "correct": 0}
#         try:
#             star["id"] = quer["id"]
#             hasanswe[quer["genre"]](answer[quer["id"]])
#             isin = [3, 4, 5]
#             if quer["genre"] in isin:
#                 if answer[quer["id"]] == quer["answer"]:
#                     star["correct"] = 1
#             star["answer"] = quer["answer"]
#         except:
#             star["answer"] = None
#         return star
#
#         # 1:单选投票题 2多选投票 3判断题 4单选题 5 多选题 6简答题 7数值评价题 8 匿名开放题 9拍照题
#
#     answer_list = json.dumps(list(map(creat_start,ques_list)))
#     coursestudent=CourseStudent.add(uid, paper_id, answer_list)
#     Student_Answer_Redis.student_answer_add(str(uid)+','+str(paper_id),answer_list)
#
#     return Success(data=coursestudent)
#
#
# def __validate_for_JUDGE(answer):
#     ans = ["0", "1"]
#     if answer not in ans:
#         raise ParameterException(msg="参数错误！")
#
#
# def __validate_for_ONE_SELECT(answer):
#     try:
#         int(answer)
#     except:
#         raise ParameterException(msg="参数错误！")
#
#
# def __validate_for_MORE_SELECT(answer):
#     from ast import literal_eval
#     mlist = literal_eval(answer)
#     if not isinstance(mlist, list):
#         raise ParameterException(msg="参数错误！")
#     try:
#         sum(mlist)
#     except:
#         raise ParameterException(msg="参数错误！")
