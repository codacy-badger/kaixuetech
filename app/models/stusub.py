# -*- coding: utf-8 -*-
# @Time    : 2019/2/27 15:36
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from sqlalchemy import Column, String, Integer, Text, orm, SmallInteger, ForeignKey
from app.models.base import Base, db


class StuSub(Base):
    __tablename__ = 'stusub'
    id = Column(Integer, primary_key=True, comment='上课id')
    student_id = Column(Integer, ForeignKey('student.user_id'), comment='外键学生id')
    subject_id = Column(Integer, ForeignKey('subject.id'), comment='外键科目id')
    teacher_id = Column(Integer, ForeignKey('teacher.user_id'), comment='外键老师id')
    sub_status = Column(Integer, default=1, comment='科目状态,1：在上，2：老师归档，2：学生归档')
    invitation = Column(String(6), comment='邀请码')


    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'student_id','subject_id','teacher_id','sub_status']


    #添加课程
    @staticmethod
    def addstusub(student_id, subject_id,teacher_id,invitation):
        with db.auto_commit():

            stusub1 = StuSub()

            stusub1.student_id = student_id
            stusub1.subject_id = subject_id
            stusub1.teacher_id = teacher_id
            stusub1.invitation =invitation

            db.session.add(stusub1)


