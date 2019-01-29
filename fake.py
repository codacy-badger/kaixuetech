from app import create_app
from app.models.base import db
from app.models.user import User

app = create_app()
with app.app_context():
    with db.auto_commit():
        # 创建一个超级管理员
        user = User()
        user.nickname = 'Super'
        user.password = '123456'
        user.email = '99999@qq.com'
        user.phone ='17864195206'
        user.auth = 1
        db.session.add(user)