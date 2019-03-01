# -*- coding: utf-8 -*-
# @Time    : 2019/1/27 22:21
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from sqlalchemy import Column, String, Integer, Text, orm, SmallInteger, ForeignKey,DateTime
from sqlalchemy.orm import relationship

from app.models.base import Base, db



class Subject(Base):
    __tablename__ = 'subject'
    id = Column(Integer, primary_key=True, comment='学科id')
    invitation=Column(String(6),unique=True, comment='邀请码')
    invi_qr=Column(Text,comment='邀请二维码')
    name = Column(String(255), comment='学科名称')
    picture_url = Column(Text,default='https://assets.ketangpai.com/theme/big/03.jpg', comment='学科图片')
    abstract=Column(String(255), comment='学科介绍(选填)')
    stu_number=Column(Integer, default=0,comment='学生总数')
    sub_status=Column(Integer, default=1,comment='科目状态,1：在上，2：归档自己，2：归档全部')
    # 与老师的一对多 孩子#
    user_id = Column(Integer, ForeignKey('teacher.user_id'), comment='外键用户id')
    teacherone = relationship("Teacher", back_populates="subjectes")

    # 与签到表的一对多 父亲#
    attendes = relationship("Attend", back_populates='subjectes', lazy='dynamic')

    #与选课中间表的一对多 父亲
    studentes_middle_subjectes = relationship("Studentes_Middle_Subject", back_populates='subjects', lazy='dynamic')

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'name','invitation','picture_url','abstract','invi_qr']
    @staticmethod
    def add(user_id,invitation,name,abstract,invi_qr,teacherone):
        with db.auto_commit():
            subject=Subject()
            subject.user_id=user_id
            subject.name = name
            subject.abstract = abstract
            subject.invitation=invitation
            subject.invi_qr =invi_qr
            subject.teacherone = teacherone
            db.session.add(subject)
            return subject
    def gui(self):
        self.sub_status=2



