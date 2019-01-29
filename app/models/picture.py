from sqlalchemy import Column,String,SmallInteger,Integer,orm,Text

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

