# -*- coding: utf-8 -*-
# @Time    : 2019/3/7 15:34
# @Author  : 昨夜
# @Email   : 903165495@qq.com
"""
课程信息数据库
"""
from sqlalchemy import Column, Integer, String, orm, SmallInteger
from app.models.base import Base, db


class CourseInfo(Base):
    __tablename__ = 'course_info'
    id = Column(Integer, primary_key=True, comment='课程id')
    name = Column(String(255), comment='课程名称')
    kind= Column(SmallInteger, default=0, comment='课程类型 0 为互动课件 1 为互动测试 ')
    change_num= Column(Integer, default=0, comment='修改次数')
    duration_id = Column(Integer, comment='资料id')
    subject_id= Column(Integer, comment='班级id',index=True)
    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'name','subject_id']

    @staticmethod
    def add(name,duration_id,subject_id):
        with db.auto_commit():
            course_info=CourseInfo()
            course_info.name=name
            course_info.duration_id = duration_id
            course_info.subject_id = subject_id

            db.session.add(course_info)
            return course_info

