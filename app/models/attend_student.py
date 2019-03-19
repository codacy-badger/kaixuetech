# -*- coding: utf-8 -*-
# @Time    : 2019/3/12 11:04
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from sqlalchemy import Column, String, Integer, Text, orm, SmallInteger, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base, db


class AttendStudent(Base):
    __tablename__ = 'attend_student'

    id = Column(Integer, primary_key=True, comment='学生签到id')
    attend_id = Column(Integer,  comment='考勤id',index=True)
    student_id = Column(Integer, comment='学生id',index=True)
    user_id= Column(Integer, comment='学生的用户id', index=True)
    attend_state = Column(SmallInteger, default=0, comment='0:未签到，1：出勤，2：旷课，3：请假，4：迟到，5：早退，6：事假，7：病假，8：公假')
    attend_position = Column(String(255), default='0', comment='考勤坐标116.414617,39.943485')
    attend_ipattend_ip = Column(String(255), default='0', comment='考勤ip 112.17.240.35')
    attend_position_state = Column(SmallInteger, default=0, comment='0:未分享坐标，1:分享了坐标未分析，2：坐标合理，3：坐标异常')
    attend_change = Column(Integer, default=0, comment='修改次数')
    attend_time = Column(DateTime, default=None, comment='签到的时间')

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'attend_id', 'attend_state', 'attend_position', 'attend_change', 'attend_time','attend_position_state']

    @staticmethod
    def add(attend_id, student_id,user_id):
        with db.auto_commit():
            attend_student = AttendStudent()
            attend_student.attend_id = attend_id
            attend_student.student_id = student_id
            attend_student.user_id=user_id
            db.session.add(attend_student)
            return attend_student