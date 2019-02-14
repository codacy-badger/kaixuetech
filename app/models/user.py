


from sqlalchemy import Column,String,SmallInteger,Integer,orm,Text
from werkzeug.security import generate_password_hash, check_password_hash

from app.libs.error_code import AuthFailed
from app.models.base import Base, db


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, comment='用户id')
    email = Column(String(24), unique=True, comment='用户邮箱')
    avatar_url =Column(Text, comment='头像url')
    comments=Column(Text, comment='备注')
    auth = Column(SmallInteger, default=1, comment='权限小于10为普通会员。大于10 为管理员')
    phone=Column(String(11), unique=True, comment='手机号')
    nickname = Column(String(24), default="未设置昵称", comment='用户昵称')
    wechat_open_id= Column(String(255), unique=True, comment='微信小程序唯一标识')
    _password = Column('password', String(100), comment='密码')


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

