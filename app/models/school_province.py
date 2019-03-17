# -*- coding: utf-8 -*-
# @Time    : 2019/3/14 17:13
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from sqlalchemy import Column, String, Integer, orm, SmallInteger, ForeignKey, Boolean
from app.models.base import Base, db


class SchoolProvince(Base):
    __tablename__ = 'school_province'
    id = Column(Integer, primary_key=True, comment='省份id')
    province = Column(String(255), comment='学校省份')
    @orm.reconstructor
    def __init__(self):
        self.fields = ['id','province']
    @staticmethod
    def add(province):
        with db.auto_commit():
            school_province = SchoolProvince()
            school_province.province = province
            db.session.add(school_province)
            return school_province