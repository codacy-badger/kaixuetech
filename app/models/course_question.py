# -*- coding: utf-8 -*-
# @Time    : 2019/3/7 17:27
# @Author  : 昨夜
# @Email   : 903165495@qq.com
"""
考卷的问题
"""
from sqlalchemy import Column, Integer, Text,String, orm, SmallInteger
from app.models.base import Base, db

class CourseQuestion(Base):
    __tablename__ = 'course_question'
    id = Column(Integer, primary_key=True, comment='题目id')
    genre = Column(Integer, comment='题目类型 1:单选投票题 2多选投票 3判断题 4单选题 5 多选题 6简答题 7 数值评价题 8 匿名开放题 9拍照题' )
    score= Column(Integer,default=1, comment='题目分数')
    questiontext= Column(Text, comment='题目内容')
    answer= Column(Text, comment='题目答案')
    option=Column(Text, comment='题目选项')
    detail=Column(Text, comment='题目解析')

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'genre','answer']
    @staticmethod
    def add(genre,questiontext,answer,option,detail=None,score=1):
        with db.auto_commit():
            course_question = CourseQuestion()
            course_question.genre = genre
            course_question.score = score
            course_question.questiontext = questiontext
            course_question.answer = answer
            course_question.option=option
            course_question.detail = detail
            db.session.add(course_question)
            return course_question

