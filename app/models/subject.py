# -*- coding: utf-8 -*-
# @Time    : 2019/1/27 22:21
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from sqlalchemy import Column, String, Integer, Text, orm, SmallInteger
from app.models.base import Base, db

"""
id 课程编号
课程名称
课程老师
课程图片
课程年份
课程学期
课程介绍
课程类型   面对面建课  老师导入课
"""

class Subject(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    user_id = Column(Integer)
    picture_url = Column(Text)
    year=Column(String(255))
    semester = Column(String(255))
    abstract=Column(String(255))
    sub_type=Column(SmallInteger,default=1)

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'name','user_id','year','semester','abstract']

    @staticmethod
    def add(name, user_id,year,semester,picture_url,abstract,sub_type=1):
        with db.auto_commit():
            subject = Subject()
            subject.name = name
            subject.user_id = user_id
            subject.year = year
            subject.semester = semester
            subject.abstract = abstract
            subject.picture_url = picture_url

            subject.sub_type = sub_type
            db.session.add(subject)