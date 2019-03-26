# -*- coding: utf-8 -*-
# @Time    : 2019/3/13 13:06
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from sqlalchemy import Column, String, Integer, Text, orm, SmallInteger, ForeignKey

from app.libs.error_code import ParameterException
from app.libs.redis_method import code_to_school
from app.models.base import Base, db



class ClassTeacher(Base):
    __tablename__ = 'class_teacher'
    id = Column(Integer, primary_key=True, comment='教师id')
    user_id = Column(Integer,index=True,unique=True, nullable=False, comment='外键用户id')
    head_url = Column(Text, comment='教师头像')
    abstract=Column(Text, comment='教师简介')
    name=Column(String(255), comment='教师名字')
    school_name=Column(String(255), comment='学校名称')
    school_id=Column(String(4), comment='学校编号')
    @orm.reconstructor
    def __init__(self):
        self.fields = ['id','name','head_url','school_name','create_time','school_id','abstract']

    def to_json(self):
        dict = self.__dict__
        print(dict)
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict



    def admin(self,head_url,abstract,name,school_id):

        self.head_url = head_url
        self.abstract = abstract
        self.name = name
        self.school_id = school_id

        try:
            if school_id is not None and school_id is not  '':
                self.school_name = code_to_school(school_id)
        except:
            raise ParameterException("学校有误！")
        return self
    @staticmethod
    def create(user_id, school_id):
        with db.auto_commit():
            teacher = ClassTeacher()
            teacher.user_id = user_id
            teacher.school_id = school_id
            teacher.school_name = code_to_school(school_id)
            db.session.add(teacher)
            return teacher
    def detail(self,head_url=None,abstract=None,name=None):
        a=0
        if head_url is not None:
            a = 1
            self.head_url = head_url
        if abstract is not None:
            a = 1
            self.abstract = abstract
        if name is not None:
            a = 1
            self.name = name
        if a==0:
            raise ParameterException()
        else:
            return self
