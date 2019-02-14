from app import create_app
from app.models.base import db
from app.models.user import User

app = create_app()
with app.app_context():
    with db.auto_commit():
        # 创建一个超级管理员
        user = User()
        user.password = '123456'
        user.phone ='17864180048'
        user.auth = 11
        db.session.add(user)