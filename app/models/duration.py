# -*- coding: utf-8 -*-
# @Time    : 2019/2/12 11:22
# @Author  : 昨夜
# @Email   : 903165495@qq.com

from sqlalchemy import Column,String,SmallInteger,Integer,orm,Text
from app.models.base import Base, db
"""
资料id
资料链接
资料名称
上传用户
"""

class Duration(Base):
    id = Column(Integer, primary_key=True)
    url = Column(Text)
    name = Column(Text)
    userid=Column(Integer)

    def __init__(self):
        self.fields = ['id', 'url','name']

    @staticmethod
    def add(url,name,userid):
        with db.auto_commit():
            duration = Duration()
            duration.url=url
            duration.name=name
            duration.userid=userid
            db.session.add(duration)
            return duration
