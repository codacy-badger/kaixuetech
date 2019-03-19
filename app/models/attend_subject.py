# -*- coding: utf-8 -*-
# @Time    : 2019/3/12 11:04
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from sqlalchemy import Column, String, Integer, Text, orm, SmallInteger, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base, db

class AttendSubject(Base):
    __tablename__ = 'attend_subject'
    id = Column(Integer, primary_key=True, comment='课程签到id')
    attend_id = Column(Integer, comment='考勤id', index=True)
    subject_id = Column(Integer, comment='班级id', index=True)
    teacher_id= Column(Integer, comment='老师id', index=True)
    user_id= Column(Integer, comment='老师用户id', index=True)
    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'attend_id',  'subject_id']
    @staticmethod
    def add(attend_id, subject_id,teacher_id,uid):
        with db.auto_commit():
            attend_subject = AttendSubject()
            attend_subject.attend_id = attend_id
            attend_subject.subject_id = subject_id
            attend_subject.teacher_id = teacher_id
            attend_subject.user_id = uid
            db.session.add(attend_subject)
            return attend_subject