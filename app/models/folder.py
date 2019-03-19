# -*- coding: utf-8 -*-
# @Time    : 2019/3/5 14:24
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from sqlalchemy import Column, Integer, String, ForeignKey

from app.models.base import Base, db


class Folder(Base):
    __tablename__ = 'folder'
    id = Column(Integer, primary_key=True, comment='文件夹id')
    name = Column(String(255), comment='文件夹的名称')
    userid=Column(Integer, ForeignKey('user.id'),nullable=False, comment='存储用户id')
    subject_id=Column(Integer,nullable=False, comment='课堂id')

    def __init__(self):
        self.fields = ['id','name','subject_id']

    @staticmethod
    def add( name, userid, subject_id):
        with db.auto_commit():
            folder = Folder()
            folder.name = name
            folder.userid = userid
            folder.subject_id = subject_id
            db.session.add(folder)
            return folder