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
    genre = Column(Integer, comment='题目类型')
    score= Column(Integer,default=0, comment='题目分数')
    questiontext= Column(Text, comment='题目内容')
    answer= Column(Text, comment='题目答案')
    detail=Column(Text, comment='题目解析')
    order_num= Column(Integer, comment='排序序号')
    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'genre','score','questiontext','answer','detail','order_num']