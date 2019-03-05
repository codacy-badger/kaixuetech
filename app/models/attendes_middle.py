# -*- coding: utf-8 -*-
# @Time    : 2019/2/28 13:49
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from sqlalchemy import Column, String, Integer, Text, orm, SmallInteger, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base, db


class Attendes_Middle(Base):
    __tablename__ = 'attendes_middle'

    id = Column(Integer, primary_key=True, comment='学生签到id')
    attend_state=Column(SmallInteger,default=0,comment='0:未签到，1：出勤，2：旷课，3：请假，4：迟到，5：早退，6：事假，7：病假，8：公假')
    attend_position= Column(String(255),default='0', comment='考勤坐标116.414617,39.943485')
    attend_ipattend_ip= Column(String(255),default='0', comment='考勤ip 112.17.240.35')
    attend_position_state=Column(SmallInteger,default=0,comment='0:未分享坐标，1:分享了坐标未分析，2：坐标合理，3：坐标异常')
    attend_change = Column(Integer,default=0, comment='修改次数')
    attend_time = Column(DateTime,default=None, comment='签到的时间')

    # 与签到的多对一关联 孩子#
    attend_id = Column(Integer, ForeignKey('attend.id'), comment='考勤id')
    attendes = relationship("Attend", back_populates="attendes_middles")
    # 与学生选课的一对多 孩子#
    studentes_middle_subject_id = Column(Integer, ForeignKey('studentes_middle_subject.id'), comment='选课中间表id')
    studentes_middle_subjectes = relationship("Studentes_Middle_Subject", back_populates="attendes_middles")

    student_id= Column(Integer, ForeignKey('student.id'), comment='学生id')

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'attend_id','attend_state','attend_position','attend_change','attend_time']
    @staticmethod
    def add(attendes,studentes_middle_subjectes):
        with db.auto_commit():
            attstu=Attendes_Middle()
            attstu.attendes=attendes
            attstu.studentes_middle_subjectes = studentes_middle_subjectes
            attstu.attend_id = attendes.id
            attstu.studentes_middle_subject_id = studentes_middle_subjectes.id
            attstu.student_id= studentes_middle_subjectes.student_id
            db.session.add(attstu)

    def up(self,attend_position,attend_ip,attend_state=1):
        self.attend_position=attend_position
        if attend_position=='0,0':
            self.attend_position_state=0
        else:
            self.attend_position_state = 1
        self.attend_change = self.attend_change+1
        self.attend_ip = attend_ip
        self.attend_time = datetime.now()
        self.attend_state = attend_state





