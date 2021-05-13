from flask import Flask
from api.model import db
from api.router import home_api, task_api


def init_app():
    app = Flask(__name__)
    app.app_context().push()
    app.register_blueprint(home_api)
    app.register_blueprint(task_api)
    db.init_app(app)
    db.create_all()
    return app


if __name__ == "__main__":
    app = init_app()
    app.run(host='0.0.0.0')
