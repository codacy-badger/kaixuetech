from sqlalchemy import Column, String, Integer, Text, orm, SmallInteger
from app.models.base import Base, db


class Student(Base):
    user_id = Column(Integer, primary_key=True)
    sno = Column(String(255), unique=True)
    school_name = Column(String(255))
    name = Column(String(255))
    auth_url = Column(Text)
    examine = Column(SmallInteger, default=1)

    @orm.reconstructor
    def __init__(self):
        self.fields = ['user_id', 'school_name']

    @staticmethod
    def school(id, school):
        with db.auto_commit():
            student = Student()
            student.school_name = school
            student.user_id = id
            db.session.add(student)

    def auth(self, name, auth_url, sno):
        self.name = name
        self.auth_url = auth_url

        self.sno = sno
        self.examine = 2
