# -*- coding: utf-8 -*-
# @Time    : 2019/3/7 16:47
# @Author  : 昨夜
# @Email   : 903165495@qq.com
"""
课程的考卷信息
"""
from sqlalchemy import Column, Integer, String, orm, SmallInteger,DateTime
from app.models.base import Base, db

class CoursePaper(Base):
    __tablename__ = 'course_paper'
    id = Column(Integer, primary_key=True, comment='考卷id')
    name = Column(String(255), comment='考试卷名称')
    paper_state=Column(SmallInteger,default=0,comment='试卷状态，0：未开始，1：已开始，2：已结束')
    start_time = Column(DateTime, comment='开始时间')
    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'name','paper_state','create_time']

    @staticmethod
    def add(name):
        with db.auto_commit():
            course_paper = CoursePaper()
            course_paper.name = name
            db.session.add(course_paper)
            return course_paper
