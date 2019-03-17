# -*- coding: utf-8 -*-
# @Time    : 2019/3/13 13:06
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from sqlalchemy import Column, String, Integer, Text, orm, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base, db



class ClassTeach(Base):
    __tablename__ = 'class_teach'
    id = Column(Integer, primary_key=True, comment='教学id')
    subject_id= Column(Integer,index=True, comment='班级id')
    teacher_id=Column(Integer,index=True, comment='老师id')
    user_id=Column(Integer,index=True, comment='老师id')
    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'subject_id', 'teacher_id']

    @staticmethod
    def add(subject_id, teacher_id,user_id):
        with db.auto_commit():
            class_teach = ClassTeach()
            class_teach.subject_id = subject_id
            class_teach.teacher_id = teacher_id
            class_teach.user_id = user_id
            db.session.add(class_teach)
            return class_teach