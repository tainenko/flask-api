from flask import Blueprint, request
from http import HTTPStatus
import json
from api.model.task import Task
from api.model import db

task_api = Blueprint('task', __name__)


@task_api.route('/tasks', methods=['GET'])
def fetch():
    tasks = Task.query.all()
    all_tasks = [{"id": task.id, "name": task.name, "status": task.status} for task in tasks]
    return {"result": all_tasks}


@task_api.route('/task', methods=['POST'])
def add():
    data = request.get_json()
    name = data["name"]
    task = Task(name=name, status=0)
    db.session.add(task)
    db.session.commit()
    return {"result": {"name": task.name, "status": task.status, "id": task.id}}, HTTPStatus.CREATED
