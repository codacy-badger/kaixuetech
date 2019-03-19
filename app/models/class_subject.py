# -*- coding: utf-8 -*-
# @Time    : 2019/3/13 13:06
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from sqlalchemy import Column, String, Integer, Text, orm, SmallInteger, ForeignKey,DateTime
from sqlalchemy.orm import relationship

from app.models.base import Base, db



class ClassSubject(Base):
    __tablename__ = 'class_subject'
    id = Column(Integer, primary_key=True, comment='学科id')
    invitation=Column(String(6),unique=True, comment='邀请码')
    invi_qr=Column(Text,comment='邀请二维码')
    name = Column(String(255), comment='学科名称')
    picture_url = Column(Text,default='https://assets.ketangpai.com/theme/big/03.jpg', comment='学科图片')
    abstract=Column(Text, comment='学科介绍(选填)')
    stu_number=Column(Integer, default=0,comment='学生总数')
    sub_status=Column(Integer, default=1,comment='科目状态,1：在上，2：归档自己，3：归档全部')

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'name', 'invitation', 'picture_url', 'abstract', 'invi_qr','sub_status','create_time']
    @staticmethod
    def add(invitation,name):
        with db.auto_commit():
            class_subject = ClassSubject()
            class_subject.invitation = invitation
            class_subject.name = name
            db.session.add(class_subject)
            return class_subject