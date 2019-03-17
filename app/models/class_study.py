# -*- coding: utf-8 -*-
# @Time    : 2019/3/13 13:07
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from sqlalchemy import Column, String, Integer, Text, orm, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base, db


class ClassStudy(Base):
    __tablename__ = 'class_study'
    id = Column(Integer, primary_key=True, comment='上课id')
    student_id = Column(Integer,index=True)
    subject_id = Column(Integer,index=True)
    user_id= Column(Integer,index=True)
    sub_status = Column(Integer, default=1, comment='科目状态,1：在上，2：老师归档，2：学生归档')



    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'student_id','subject_id','sub_status']

    @staticmethod
    def add(student_id,subject_id,user_id):
        with db.auto_commit():
            study = ClassStudy()
            study.student_id = student_id
            study.subject_id = subject_id
            study.user_id = user_id
            db.session.add(study)
            return study
