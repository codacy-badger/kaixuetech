from flask_script import Manager
from app import create_app
from flask_migrate import MigrateCommand, Migrate
from app.models.base import db
app=create_app()
manager = Manager(app)
Migrate(app, db)
manager.add_command("db", MigrateCommand)


if __name__ == "__main__":
     manager.run()