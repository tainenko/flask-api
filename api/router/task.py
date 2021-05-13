from flask import Blueprint
from http import HTTPStatus
import json
from api.model.task import Task

task_api = Blueprint('task', __name__)


@task_api.route('/tasks', methods=['GET'])
def fetch():
    tasks = Task.query.all()
    all_tasks = [{"id": task.id, "name": task.name, "status": task.status} for task in tasks]
    return json.dumps(all_tasks), HTTPStatus.OK
