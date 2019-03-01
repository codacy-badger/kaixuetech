# -*- coding: utf-8 -*-
# @Time    : 2019/1/26 16:11
# @Author  : 昨夜
# @Email   : 903165495@qq.com

from sqlalchemy import Column, String, Integer, Text, orm, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base, db



class Teacher(Base):
    __tablename__ = 'teacher'
    id = Column(Integer, primary_key=True, comment='教师id')
    user_id = Column(Integer, ForeignKey('user.id'),unique=True, nullable=False, comment='外键用户id')
    head_url = Column(Text, comment='教师头像')
    abstract=Column(Text, comment='教师简介')
    name=Column(String(255), comment='教师名字')
    school_name=Column(String(255), comment='学校名称')

    #与学科的一对多关联 父亲#
    subjectes = relationship("Subject", back_populates="teacherone", lazy='dynamic')

    @orm.reconstructor
    def __init__(self):
        self.fields = ['name','head_url','school_name']

    """
    初始化字段并添加老师的基本信息
    """
    @staticmethod
    def addschool(id, school,name):
        with db.auto_commit():
            teacher = Teacher()
            teacher.school_name = school
            teacher.name = name
            teacher.user_id = id
            db.session.add(teacher)
            return teacher
    """
    修改头像和介绍
    """
    def updetail(self,head_url,abstract):
        if head_url is not None:
            self.head_url = head_url
        if abstract is not None:
            self.abstract = abstract
        return self

