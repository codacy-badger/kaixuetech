from .app import Flask



def register_blueprints(app):
    from app.api.v1 import create_blueprint_v1
    app.register_blueprint(create_blueprint_v1(), url_prefix='/v1')
def register_plugin(app):
    from app.models.base import db
    db.init_app(app)
    with app.app_context():
        db.create_all()
def register_swagger(app):
    from flasgger import Swagger
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

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.setting')
    app.config.from_object('app.config.secure')

    register_swagger(app)
    register_blueprints(app)
    register_plugin(app)
    return app
