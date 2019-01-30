# -*- coding: utf-8 -*-
# @Time    : 2019/1/30 1:05
# @Author  : 昨夜
# @Email   : 903165495@qq.com

from sqlalchemy import Column, String, Integer, Text, orm, SmallInteger, DateTime,Float
from app.models.base import Base, db

"""
章节id
章节名
上课时间
上课时长
课程资料
章节介绍
"""
class Section(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    subject_id= Column(Integer)
    class_time=Column(DateTime)
    duration=Column(Float)
    learn_data=Column(Text)
    abstract = Column(Text)