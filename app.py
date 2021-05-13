from flask import Flask
from api.model.task import Task
from api.model import db
import json


def init_app():
    app = Flask(__name__)
    app.app_context().push()
    db.init_app(app)
    db.create_all()
    return app


app = init_app()


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/tasks', methods=['GET'])
def fetch():
    tasks = Task.query.all()
    all_tasks = [{"id": task.id, "name": task.name, "status": task.status} for task in tasks]
    return json.dumps(all_tasks), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0')
