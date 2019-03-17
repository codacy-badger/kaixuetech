# -*- coding: utf-8 -*-
# @Time    : 2019/3/12 11:00
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from datetime import datetime

from sqlalchemy import Column, String, Integer, Text, orm, SmallInteger, ForeignKey, DateTime
from sqlalchemy.orm import relationship


from app.models.base import Base, db


class AttendInfo(Base):
    __tablename__ = 'attend_info'
    id = Column(Integer, primary_key=True, comment='考勤id')
    attend_name = Column(String(255), comment='考勤名称')
    attend_number_secret=Column(String(14), comment='学校编号+年月日+4位随机码',index=True)
    attend_number = Column(String(4), comment='4位随机码')
    attend_state=Column(SmallInteger,default="1",comment='0:未开放，1：签到中，2：签到结束')
    start_time=Column(DateTime,default=datetime.now, comment='发起签到的时间')
    end_time=Column(DateTime, comment='结束签到的时间')
    attend_position = Column(String(255), default='0', comment='考勤坐标116.414617,39.943485')
    num_students=Column(Integer, comment='学生人数')

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'attend_name',  'attend_number', 'attend_state']

    @staticmethod
    def add(attend_name, attend_number):
        with db.auto_commit():
            attend_info = AttendInfo()
            attend_info.attend_name = attend_name
            attend_info.attend_number = attend_number[-4:]
            attend_info.attend_number_secret = attend_number

            db.session.add(attend_info)
            return attend_info