from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from database import db
from api.router import home_api, task_api
from config import config_map


def init_app(env=None):
    app = Flask(__name__)
    app.config.from_object(config_map[env or "test"])
    app.app_context().push()
    app.register_blueprint(home_api)
    app.register_blueprint(task_api)
    db.init_app(app)
    db.create_all()
    return app


def init_manager(app, db):
    migrate = Migrate(app, db)  # Initializing migrate.
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    return manager


if __name__ == "__main__":
    app = init_app()
    manager = init_manager(app, db)
    manager.run()
