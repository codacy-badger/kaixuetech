# -*- coding: utf-8 -*-
# @Time    : 2019/2/27 17:39
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from sqlalchemy import Column, String, Integer, Text, orm, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base, db


class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True, comment='学生id')
    user_id = Column(Integer, ForeignKey('user.id'),unique=True, nullable=False, comment='外键用户id')
    auth_url = Column(Text, comment='学生头像')
    sno = Column(String(255), unique=True, comment='学生学号')
    school_name = Column(String(255), comment='学生学校')
    name = Column(String(255), comment='学生姓名')
    major= Column(String(255), comment='学生专业')
    grade= Column(String(255), comment='学生年级')
    classno= Column(String(255), comment='学生班级')
    enrolltime= Column(String(255), comment='学生入学时间')
    # 与学生选课中心表的一对多 父亲#
    studentes_middle_subjectes = relationship("Studentes_Middle_Subject", back_populates='students', lazy='dynamic')

    @orm.reconstructor
    def __init__(self):
        self.fields = ['user_id', 'auth_url','sno','school_name','name','major','grade','classno','enrolltime']

    @staticmethod
    def add(user_id,name, sno,school_name,auth_url):
        with db.auto_commit():
            student = Student()
            student.user_id = user_id
            student.name = name
            student.sno = sno
            student.school_name = school_name
            student.auth_url = auth_url
            db.session.add(student)
            return student

