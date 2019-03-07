# -*- coding: utf-8 -*-
# @Time    : 2019/3/7 15:49
# @Author  : 昨夜
# @Email   : 903165495@qq.com
"""
课程的课件信息
"""
from sqlalchemy import Column, Integer, String, orm, SmallInteger
from app.models.base import Base, db

class CourseWare(Base):
    __tablename__ = 'course_ware'
    id = Column(Integer, primary_key=True, comment='课件互动id')
    course_info_id= Column(Integer, comment='课程id')
    ware_page = Column(Integer, comment='课件页码')
    paper_info_id= Column(Integer, comment='试卷id')

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'course_info_id','duration_id','ware_page','paper_info_id']

    @staticmethod
    def add(course_info,ware_page,paper_info):
        with db.auto_commit():
            course_ware=CourseWare()
            course_ware.course_info_id=course_info.id
            course_ware.ware_page = ware_page
            course_ware.paper_info_id = paper_info.id
            db.session.add(course_ware)
            return course_ware