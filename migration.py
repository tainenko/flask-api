from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from main import init_app
from database import db


def init_manager(app, db):
    migrate = Migrate(app, db)  # Initializing migrate.
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    return manager


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--env', action='store', default="test",
                        help="environment")
    args = parser.parse_args()

    app = init_app(args.env)
    manager = init_manager(app, db)
    manager.run()
