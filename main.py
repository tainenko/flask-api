from flask import Flask
from flasgger import Swagger

from database import db
from api.router import home_api, task_api
from config import config_map


def init_app(env="dev"):
    app = Flask(__name__)
    app.config.from_object(config_map[env])
    app.app_context().push()
    app.register_blueprint(home_api)
    app.register_blueprint(task_api)
    swagger_config = Swagger.DEFAULT_CONFIG
    swagger_config['title'] = "The Task swagger API"
    swagger_config['description'] = "A detailed documentation of the Task API"

    Swagger(app, config=swagger_config)
    db.init_app(app)
    db.create_all()
    return app


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--env', action='store', default="test",
                        help="environment")
    args = parser.parse_args()
    app = init_app()
    app.run()
