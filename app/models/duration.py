# -*- coding: utf-8 -*-
# @Time    : 2019/2/12 11:22
# @Author  : 昨夜
# @Email   : 903165495@qq.com

from sqlalchemy import Column, String, SmallInteger, Integer, orm
from app.models.base import Base, db


class Duration(Base):
    __tablename__ = 'duration'
    id = Column(Integer, primary_key=True, comment='资料区id')
    name = Column(String(255),comment='资料的名称')
    old_name=Column(String(255),comment='资料之前的名称')
    type=Column(String(255),comment='资料类型')
    userid=Column(Integer,nullable=False, comment='存储用户id')
    subject_id=Column(Integer,nullable=False, comment='课堂id')
    is_folder=Column(SmallInteger,default=0, comment='是否有文件夹')
    folder_id=Column(Integer,  comment='文件夹id')
    site=Column(SmallInteger, comment='分类 1 上课课件 2 资料')

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id','name','old_name','type','name','updated_time','create_time']

    @staticmethod
    def add(name,old_name,userid,subject_id,type,site,folder_id=0):
        with db.auto_commit():
            duration = Duration()
            duration.name=name
            duration.old_name=old_name
            duration.userid=userid
            duration.subject_id = subject_id
            duration.type = type
            duration.site = site
            duration.folder_id = folder_id
            if folder_id>0:
                duration.is_folder = 1
            db.session.add(duration)
            return duration
