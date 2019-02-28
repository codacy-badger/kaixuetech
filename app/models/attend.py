# -*- coding: utf-8 -*-
# @Time    : 2019/2/27 17:39
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from sqlalchemy import Column, String, Integer, Text, orm, SmallInteger, ForeignKey
from app.models.base import Base, db


class Attend(Base):
    __tablename__ = 'attend'
    id = Column(Integer, primary_key=True, comment='考勤id')
    attend_name = Column(String(255), comment='考勤名称')
    subject_id = Column(Integer, ForeignKey('subject.id'), comment='课堂id')
    attend_number=Column(String(16), comment='学校编号+年月日+4位随机码')
    attend_state=Column(SmallInteger,comment='0:未开放，1：签到中，2：签到结束')



    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'attend_name','subject_id','attend_number','attend_state']
