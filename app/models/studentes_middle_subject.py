# -*- coding: utf-8 -*-
# @Time    : 2019/2/27 15:36
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from sqlalchemy import Column, String, Integer, Text, orm, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base, db


class Studentes_Middle_Subject(Base):
    __tablename__ = 'studentes_middle_subject'
    id = Column(Integer, primary_key=True, comment='上课id')
    teacher_id = Column(Integer, ForeignKey('teacher.user_id'), comment='外键老师id')
    sub_status = Column(Integer, default=1, comment='科目状态,1：在上，2：老师归档，2：学生归档')
    invitation = Column(String(6), comment='邀请码')
    # 签到中间表1对多关联 父亲
    attendes_middles = relationship("Attendes_Middle", back_populates="studentes_middle_subjectes", lazy='dynamic')
    # 学科的一对多 孩子#
    subject_id = Column(Integer, ForeignKey('subject.id'))
    subjects = relationship("Subject", back_populates="studentes_middle_subjectes")

    # 学生的一对多 孩子#
    student_id = Column(Integer, ForeignKey('student.id'))
    students = relationship("Student", back_populates="studentes_middle_subjectes")



    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'students','subjects','teacher_id','sub_status']


    #添加学生上课
    @staticmethod
    def addstusub(subjects, students,invitation):
        with db.auto_commit():
            stusub = Studentes_Middle_Subject()
            stusub.subjects = subjects
            stusub.students = students
            stusub.subject_id = subjects.id
            stusub.student_id = students.id
            stusub.teacher_id = subjects.user_id,
            stusub.invitation =invitation
            db.session.add(stusub)
            return stusub

