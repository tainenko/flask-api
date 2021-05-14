from flask import Blueprint, request, jsonify
from http import HTTPStatus
from .constant import TASK_STATUS_INCOMPLETE, TASK_STATUS_COMPLETE
from api.model.task import Task
from database import db

task_api = Blueprint('task', __name__)


@task_api.route('/tasks', methods=['GET'])
def fetch():
    """
    Query the list of all tasks
    ---
    tags:
      - Task
    description:
        Query all task interfaces in JSON format
    responses:
      200:
          description: The query is successful
          example: {"result": [{"id": 1, "name": "name", "status": 0}]}
    """
    tasks = Task.query.all()
    all_tasks = [{"id": task.id, "name": task.name, "status": task.status} for task in tasks]
    return jsonify({"result": all_tasks})


@task_api.route('/task', methods=['POST'])
def add():
    """
    Create task
    ---
    tags:
      - Task
    description:
        Task creation interface, in JSON format
    parameters:
      - name: body
        in: body
        required: true
        schema:
          required:
            - name
          properties:
            name:
              type: string
              description: task name
    responses:
      201:
          description: Success
          example: {"result": {"name": "買晚餐", "status": 0, "id": 1}}
      406:
        description: Incorrect creation, incorrect parameters, etc

    """
    data = request.get_json()
    if data is None:
        return jsonify({"error message": "invalid request post must use json"})
    if "name" not in data:
        return jsonify({"error message": "Parameter is wrong"}), HTTPStatus.NOT_ACCEPTABLE
    name = data["name"]
    task = Task(name=name, status=TASK_STATUS_INCOMPLETE)
    db.session.add(task)
    db.session.commit()
    return jsonify({"result": {"name": task.name, "status": task.status, "id": task.id}}), HTTPStatus.CREATED


@task_api.route('/task/<id>', methods=["PUT"])
def edit(id):
    """
    Update task
    ---
    tags:
      - Task
    description:
        Task update interface, in JSON format
    parameters:
      - name: id
        in: path
        required: true
        type: integer
      - name: body
        in: body
        required: true
        schema:
          name: Task Update
          properties:
            name:
              type: string
              description: task name
            status:
              type: integer
              description: task status
    responses:
      200:
          description: Success
          example: {"result": {"name": "買晚餐", "status": 0, "id": 1}}
      406:
        description: Incorrect creation, incorrect parameters, etc
    """
    data = request.get_json()
    if data is None:
        return jsonify({"error message": "invalid request post must use json"})
    if "name" not in data and "status" not in data:
        return jsonify({"error message": 'Body must have a name or status parameter'}), HTTPStatus.NOT_ACCEPTABLE
    new_name = data.get("name", None)
    new_status = data.get("status", None)
    if new_status is not None and new_status not in [TASK_STATUS_INCOMPLETE, TASK_STATUS_COMPLETE]:
        return jsonify(
            {
                "error message": f'Only accepts {str([TASK_STATUS_INCOMPLETE, TASK_STATUS_COMPLETE])} for status'}), HTTPStatus.NOT_ACCEPTABLE
    task = Task.query.filter_by(id=id).first()
    if task is None:
        return jsonify({"error message": f"id {id} task does not exist."}), HTTPStatus.NOT_FOUND
    if new_name is not None or new_status is not None:
        if new_name is not None:
            task.name = new_name
        if new_status is not None:
            task.status = new_status
        db.session.commit()
    return jsonify({"result": {"name": task.name, "status": task.status, "id": task.id}})


@task_api.route('/task/<id>', methods=["DELETE"])
def remove(id):
    """
        Delete task
        ---
        tags:
          - Task
        description:
            Task deletion interface, in JSON format
        parameters:
          - name: id
            in: path
            required: true
            type: integer
        responses:
          200:
              description: Success
          404:
            description: task not found
        """
    task = Task.query.filter_by(id=id)
    if not task.scalar():
        return jsonify({"error message": f"id {id} task does not exist."}), HTTPStatus.NOT_FOUND
    task.delete()
    db.session.commit()
    return jsonify({"result": ""}), HTTPStatus.OK
