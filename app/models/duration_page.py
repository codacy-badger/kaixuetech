# -*- coding: utf-8 -*-
# @Time    : 2019/3/25 15:54
# @Author  : 昨夜
# @Email   : 903165495@qq.com

from sqlalchemy import Column, String, SmallInteger, Integer, orm, Text, ForeignKey
from app.models.base import Base, db

class DurationPage(Base):
    __tablename__ = 'duration_page'
    id = Column(Integer, primary_key=True, comment='id')
    duration_id = Column(Integer,comment='资料的名称',index=True)
    page= Column(Integer,comment='资料页码')
    url=Column(String(255),comment='页面缩略图')
    __mapper_args__ = {"order_by": page}
    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'duration_id', 'page', 'url']

    # @staticmethod
    # def add(duration_id,page,url):
