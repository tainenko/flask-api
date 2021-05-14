from ..conftest import app, client
from http import HTTPStatus
import json
from api.constant import MIMETYPE_JSON

headers = {
    'Content-Type': MIMETYPE_JSON,
    'Accept': MIMETYPE_JSON
}


def test_get_tasks(client):
    response = client.get('/tasks')
    assert response.status == f"{HTTPStatus.OK} OK"
    assert response.get_json() == {"result": []}


def test_create_task(client):
    data = {
        "name": "買晚餐"
    }
    url = '/task'
    response = client.post(url, data=json.dumps(data), headers=headers)
    assert response.content_type == MIMETYPE_JSON
    assert response.json['result'] == {"name": "買晚餐", "status": 0, "id": 1}
    assert response.status == f"{HTTPStatus.CREATED} CREATED"


def test_edit_task(client):
    id = 1
    data = {
        "status": 1,
        "name": "買早餐"
    }
    url = f'/task/{id}'
    response = client.put(url, data=json.dumps(data), headers=headers)
    assert response.content_type == MIMETYPE_JSON
    expected = {"name": "買早餐", "status": 1, "id": 1}
    assert response.json['result'] == expected
    assert response.status == f"{HTTPStatus.OK} OK"

    response = client.get('/tasks')
    assert response.status == f"{HTTPStatus.OK} OK"
    assert response.get_json() == {"result": [expected]}


def test_delete_task(client):
    id = 1
    url = f'/task/{id}'
    response = client.delete(url, headers=headers)
    assert response.content_type == MIMETYPE_JSON
    assert response.status == f"{HTTPStatus.OK} OK"

    response = client.get('/tasks')
    assert response.status == f"{HTTPStatus.OK} OK"
    assert response.get_json() == {"result": []}
