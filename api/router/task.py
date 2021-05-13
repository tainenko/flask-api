from flask import Blueprint, request
from http import HTTPStatus
from api.model.task import Task
from database import db

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


@task_api.route('/task/<id>', methods=["PUT"])
def edit(id):
    data = request.get_json()
    new_name = data.get("name", None)
    new_status = data.get("status", None)
    task = Task.query.filter_by(id=id).first()
    if new_name:
        task.name = new_name
    if new_status:
        task.status = new_status
    if new_name or new_status:
        db.session.commit()
    return {"result": {"name": task.name, "status": task.status, "id": task.id}}


@task_api.route('/task/<id>', methods=["DELETE"])
def remove(id):
    Task.query.filter_by(id=id).delete()
    db.session.commit()
    return "OK", HTTPStatus.OK
