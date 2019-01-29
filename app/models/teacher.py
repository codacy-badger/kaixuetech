# -*- coding: utf-8 -*-
# @Time    : 2019/1/26 16:11
# @Author  : 昨夜
# @Email   : 903165495@qq.com

from sqlalchemy import Column, String, Integer, Text, orm, SmallInteger
from app.models.base import Base, db

class Teacher(Base):
    user_id = Column(Integer, primary_key=True)
    head_url = Column(Text)
    abstract=Column(String(255))
    school_name=Column(String(255))

    @orm.reconstructor
    def __init__(self):
        self.fields = ['user_id', 'school_name','head_url','school_name']

    @staticmethod
    def school(id, school):
        with db.auto_commit():
            teacher = Teacher()
            teacher.school_name = school
            teacher.user_id = id
            db.session.add(teacher)