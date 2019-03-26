# -*- coding: utf-8 -*-
# @Time    : 2019/2/27 17:39
# @Author  : 昨夜
# @Email   : 903165495@qq.com
from sqlalchemy import Column,String,Integer,Text

from app.models.base import Base, db

class File(Base):
    id = Column(Integer, primary_key=True)
    avatar_url = Column(Text)
    type = Column(String(24))
    userid=Column(Integer)

    @staticmethod
    def add(avatar_url,type,userid):
        with db.auto_commit():
            file = File()
            file.avatar_url = avatar_url
            file.type = type
            file.userid = userid
            db.session.add(file)
            return {'avatar_url': avatar_url, 'type': type, 'userid': userid}

