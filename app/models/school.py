# -*- coding: utf-8 -*-
# @Time    : 2019/2/28 11:32
# @Author  : 昨夜
# @Email   : 903165495@qq.com

from sqlalchemy import Column, String, Integer, orm, SmallInteger, ForeignKey, Boolean
from app.models.base import Base, db


class School(Base):
    __tablename__ = 'school'
    id = Column(Integer, primary_key=True, comment='学校id')
    schoolcode = Column(String(4), unique=True, comment='学校编号4位数')
    name = Column(String(255), comment='学校名字')
    province = Column(String(255), comment='学校省份')
    show= Column(Boolean (255), comment='是否展示')

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id','schoolcode', 'name', 'province', 'show']

    def to_json(self):
        json_data = {
            "id": self.id,
            "value": self.schoolcode,
            "label": self.name,
            "province": self.province,
            "show": self.show
        }

        return json_data
    @staticmethod
    def add(schoolcode, name, province, show=0):
        with db.auto_commit():
            school = School()
            school.schoolcode = schoolcode
            school.name = name
            school.province = province
            school.show = show
            db.session.add(school)