


from sqlalchemy import Column,String,SmallInteger,Integer,orm,Text
from werkzeug.security import generate_password_hash, check_password_hash

from app.libs.error_code import AuthFailed
from app.models.base import Base, db


class User(Base):
    id = Column(Integer, primary_key=True)
    email = Column(String(24), unique=True)
    nickname = Column(String(24), unique=True,default="未设置昵称")
    auth = Column(SmallInteger, default=1)
    phone=Column(String(11), unique=True, nullable=False)
    wechat_open_id= Column(String(255), unique=True)
    wechat_union_id= Column(String(255))
    _password = Column('password', String(100))


    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'nickname', 'auth','wechat_open_id','phone']
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    @staticmethod
    def verify(phone, password):
        user = User.query.filter_by(phone=phone).first_or_404()
        if not user.check_password(password):
            raise AuthFailed()
        if user.auth == 1:
            scope='StudentScope'
        elif  user.auth == 2:
            scope = 'TeacherScope'
        elif user.auth == 11:
            scope = 'AdminScope'
        return {'uid': user.id, 'scope': scope}

    @staticmethod
    def register_by_phone(account, secret):
        with db.auto_commit():
            user = User()
            user.phone = account
            user.password = secret
            db.session.add(user)

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)


    def change_password(self,raw):
        self._password = generate_password_hash(raw)

