# -*- coding: utf-8 -*-
# @Time    : 2019/2/28 13:49
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from sqlalchemy import Column, String, Integer, Text, orm, SmallInteger, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.models.base import Base, db


class Attendes_Middle(Base):
    __tablename__ = 'attendes_middle'

    id = Column(Integer, primary_key=True, comment='学生签到id')
    attend_state=Column(SmallInteger,default=0,comment='0:未签到，1：出勤，2：旷课，3：请假，4：迟到，5：早退，6：事假，7：病假，8：公假')
    attend_position= Column(String(255),default='0', comment='考勤坐标')
    attend_position_state=Column(SmallInteger,default=0,comment='0:未分享坐标，1：坐标合理，2：坐标异常')
    attend_change = Column(Integer,default=0, comment='修改次数')
    attend_time = Column(DateTime,default=None, comment='签到的时间')

    # 与签到的多对一关联 孩子#
    attend_id = Column(Integer, ForeignKey('attend.id'), comment='考勤id')
    attendes = relationship("Attend", back_populates="attendes_middles")
    # 与学生选课的一对多 孩子#
    studentes_middle_subject_id = Column(Integer, ForeignKey('studentes_middle_subject.id'), comment='选课中间表id')
    studentes_middle_subjectes = relationship("Studentes_Middle_Subject", back_populates="attendes_middles")



    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'attend_id','subject_id','attend_state','attend_position','attend_change','students','attend_time']
    @staticmethod
    def add(attendes,studentes_middle_subjectes):
        with db.auto_commit():
            attstu=Attendes_Middle()
            attstu.attendes=attendes
            attstu.studentes_middle_subjectes = studentes_middle_subjectes
            attstu.attend_id = attendes.id
            attstu.studentes_middle_subject_id = studentes_middle_subjectes.id
            db.session.add(attstu)
