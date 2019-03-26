# -*- coding: utf-8 -*-
# @Time    : 2019/3/13 13:05
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from sqlalchemy import Column, String, Integer, Text, orm, SmallInteger

from app.libs.error_code import RepeatException1, ParameterException
from app.libs.redis_method import code_to_school
from app.models.base import Base, db


class ClassStudent(Base):
    __tablename__ = 'class_student'
    id = Column(Integer, primary_key=True, comment='学生id')
    user_id = Column(Integer,unique=True, nullable=False,index=True, comment='外键用户id')
    auth_url = Column(Text, comment='学生头像')
    sno = Column(String(255), unique=True, comment='学生学号')
    school_name = Column(String(255), comment='学生学校')
    name = Column(String(255), comment='学生姓名')
    major= Column(String(255), comment='学生专业')
    grade= Column(String(255), comment='学生年级')
    classno= Column(String(255), comment='学生班级')
    school_id = Column(String(4), comment='学校编号')
    isauth=Column(SmallInteger,default=0, comment='是否认证，0 未认证 1已经认证  2未审核')
    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'isauth','auth_url', 'sno', 'school_name', 'name', 'major', 'grade', 'classno','school_id','create_time']
    def admin(self,auth_url,sno,school_id,name,major,grade,classno):
        self.auth_url = auth_url
        self.sno = sno
        self.school_id = school_id
        self.name = name
        self.major = major
        self.grade = grade
        self.classno = classno
        if school_id is not None and school_id is not '':
            self.school_name = code_to_school(school_id)
        return self
    @staticmethod
    def create(user_id, school_id):
        with db.auto_commit():
            student = ClassStudent()
            student.user_id = user_id
            student.school_id = school_id
            if school_id is not None and school_id is not '':
                student.school_name = code_to_school(school_id)
            db.session.add(student)
            return student
    def upauth(self,sno,name,grade):
        if self.sno is None and self.sno is None and self.grade is None :
            self.sno  = sno
            self.name = name
            self.grade= grade
            self.isauth=2
            return self
        raise RepeatException1("不可更改！")
    def detail(self,auth_url=None,major=None,classno=None):
        a=0
        if auth_url is not None:
            a = 1
            self.auth_url = auth_url
        if major is not None:
            a = 1
            self.major = major
        if classno is not None:
            a = 1
            self.classno = classno

        if a==0:
            raise ParameterException()
        else:
            return self
