# -*- coding: utf-8 -*-
# @Time    : 2019/3/7 17:41
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from sqlalchemy import Column, Integer, Text,String, orm, SmallInteger,DateTime
from app.models.base import Base, db
from datetime import datetime
class CourseStudent(Base):
    __tablename__ = 'course_student'
    id = Column(Integer, primary_key=True, comment='id')
    student_id = Column(Integer, comment='学生id',index=True)
    paper_id= Column(Integer, comment='考卷id',index=True)
    answer=Column(Text, comment='考生答案')
    end_time=Column(DateTime, comment='完成时间')
    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'student_id', 'paper_id','answer']
    @staticmethod
    def add(student_id,paper_id,answer):
        with db.auto_commit():
            course_student = CourseStudent()
            course_student.student_id = student_id
            course_student.paper_id = paper_id
            course_student.answer = answer
            course_student.end_time = datetime.now()
            db.session.add(course_student)
            return course_student

