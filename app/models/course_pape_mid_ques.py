# -*- coding: utf-8 -*-
# @Time    : 2019/3/7 17:35
# @Author  : 昨夜
# @Email   : 903165495@qq.com
"""
考卷的问题
"""
from sqlalchemy import Column, Integer,orm
from app.models.base import Base, db

class PaperMidQuestion(Base):
    __tablename__ = 'course_pape_mid_ques'
    id = Column(Integer, primary_key=True, comment='考卷问题中间表id')
    paper_id=Column(Integer, comment='考卷id')
    question_id=Column(Integer, comment='问题id')

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'paper_id', 'question_id']