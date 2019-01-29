# -*- coding: utf-8 -*-
# @Time    : 2019/1/30 1:05
# @Author  : 昨夜
# @Email   : 903165495@qq.com

from sqlalchemy import Column, String, Integer, Text, orm, SmallInteger
from app.models.base import Base, db

"""
章节id
章节名
上课日期
上课时间
上课时长
章节介绍
课程资料
章节介绍
"""
class Section(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    subject_id= Column(Integer)