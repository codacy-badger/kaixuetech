# -*- coding: utf-8 -*-
# @Time    : 2019/1/26 16:11
# @Author  : 昨夜
# @Email   : 903165495@qq.com

from sqlalchemy import Column, String, Integer, Text, orm, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base, db
from app.models.subject import Subject


class Teacher(Base):
    __tablename__ = 'teacher'
    id = Column(Integer, primary_key=True, comment='教师id')
    user_id = Column(Integer, ForeignKey('user.id'),unique=True, nullable=False, comment='外键用户id')
    head_url = Column(Text, comment='教师头像')
    abstract=Column(Text, comment='教师简介')
    school_name=Column(String(255), comment='学校名称')
    label=Column(String(255), comment='教师标签')
    subjectes = relationship("Subject", order_by=Subject.id, back_populates="teacheres", lazy='dynamic')

    @orm.reconstructor
    def __init__(self):
        self.fields = ['user_id', 'school_name','head_url','school_name','subjectes']

    """
    初始化字段并添加学校内容
    """
    @staticmethod
    def addschool(id, school):
        with db.auto_commit():
            teacher = Teacher()
            teacher.school_name = school
            teacher.user_id = id
            db.session.add(teacher)
    """
    修改头像和介绍
    """
    def updetail(self,head_url,abstract):
        if head_url is not None:
            self.head_url = head_url
        if abstract is not None:
            self.abstract = abstract

