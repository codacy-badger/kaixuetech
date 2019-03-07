# -*- coding: utf-8 -*-
# @Time    : 2019/2/27 17:39
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from datetime import datetime

from sqlalchemy import Column, String, Integer, Text, orm, SmallInteger, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.models.attendes_middle import Attendes_Middle
from app.models.base import Base, db


class Attend(Base):
    __tablename__ = 'attend'
    id = Column(Integer, primary_key=True, comment='考勤id')
    attend_name = Column(String(255), comment='考勤名称')
    attend_number_secret=Column(String(14), comment='学校编号+年月日+4位随机码')
    attend_number = Column(String(4), comment='4位随机码')
    attend_state=Column(SmallInteger,default="1",comment='0:未开放，1：签到中，2：签到结束')
    start_time=Column(DateTime,default=datetime.now, comment='发起签到的时间')
    end_time=Column(DateTime, comment='结束签到的时间')
    attend_position = Column(String(255), default='0', comment='考勤坐标116.414617,39.943485')
    num_students=Column(Integer, comment='学生人数')
    num_attendance=Column(Integer, default=0,comment='签到人数')
    num_no_attendance = Column(Integer,default=0, comment='未签到人数')
    #签到表与学科的多对一关联 孩子#
    subject_id = Column(Integer, ForeignKey('subject.id'), comment='课堂id')
    subjectes = relationship("Subject", back_populates="attendes")

    #与签到中心表多对一关联 父亲#
    attendes_middles = relationship("Attendes_Middle",order_by=Attendes_Middle.attend_time, back_populates="attendes", lazy='dynamic')

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'attend_name','subject_id','attend_number','attend_state']
    @staticmethod
    def add(attend_name,subjectes,attend_number):
        with db.auto_commit():
            attend = Attend()
            attend.attend_name = attend_name
            attend.subjectes = subjectes
            attend.subject_id = subjectes.id
            attend.attend_number_secret = attend_number
            attend.attend_number = attend_number[-4:]
            db.session.add(attend)
            return attend