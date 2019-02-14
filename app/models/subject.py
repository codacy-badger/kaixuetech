# -*- coding: utf-8 -*-
# @Time    : 2019/1/27 22:21
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from sqlalchemy import Column, String, Integer, Text, orm, SmallInteger, ForeignKey,DateTime
from sqlalchemy.orm import relationship


from app.models.base import Base, db



class Subject(Base):
    id = Column(Integer, primary_key=True, comment='学科id')
    user_id = Column(Integer, ForeignKey('teacher.user_id'), comment='外键用户id')
    teacher = relationship("Teacher", back_populates="subjectes")
    name = Column(String(255), comment='学科名称')
    picture_url = Column(Text, comment='学科图片')
    year=Column(String(255) , comment='学科年份')
    abstract=Column(String(255), comment='学科介绍')
    sub_type=Column(SmallInteger,default=1, comment='学科类型')

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'name','year','picture_url','abstract']
    @staticmethod
    def add(user_id,name,picture_url,year,abstract,sub_type=1):
        with db.auto_commit():
            subject=Subject()
            subject.user_id=user_id
            subject.name = name
            subject.picture_url = picture_url
            subject.year = year
            subject.abstract = abstract
            subject.sub_type = sub_type
            db.session.add(subject)
            return subject


