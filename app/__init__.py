
from flask_cache import Cache
from .app import Flask
from app.api.v1 import create_blueprint_v1
import redis
from flask_session import Session
from flasgger import Swagger
from celery import Celery
#蓝图
def register_blueprints(app):
    app.register_blueprint(create_blueprint_v1(), url_prefix='/v1')
#数据库初始化
def register_plugin(app):
    from app.models.base import db
    db.init_app(app)
    with app.app_context():
        db.create_all()
#api文档
def register_swagger(app):

    app.config["SWAGGER"] = {
        "title": "Swagger Basic Auth App",
        "uiversion": 2,
    }
    Swagger(app,
            template={
                "swagger": "2.0",
                "info": {
                    "title": "Swagger Basic Auth App",
                    "version": "1.0",
                },
                "consumes": [
                    "application/json",
                ],
                "produces": [
                    "application/json",
                ],
            }, )
#session存在redis
def register_session(app):
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_REDIS'] = redis.Redis(host='47.110.251.32', port='6379',db=1,password='ihaveabigdream')
    app.config['SESSION_KEY_PREFIX'] = 'flask'
    Session(app)
# 页面缓存
def register_cache(app):

    cache = Cache(app, config={'CACHE_TYPE': 'redis',
                               'CACHE_REDIS_HOST': '47.110.251.32',
                               'CACHE_REDIS_PORT': 6379,
                               'CACHE_REDIS_PASSWORD': 'ihaveabigdream',
                               'CACHE_REDIS_DB': 0 })

#跨域
def register_cors(app):
    from flask_cors import CORS
    CORS(app, supports_credentials=True)
from app.celery import celery
def register_celery(app):
    celery.init_app(app=app)
def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.setting')
    app.config.from_object('app.config.secure')
    register_swagger(app)
    register_celery(app)
    register_blueprints(app)
    register_plugin(app)
    register_cors(app)
    register_session(app)
    register_cache(app)

    return app
