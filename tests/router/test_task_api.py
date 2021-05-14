from http import HTTPStatus
import json
import pytest
from api.constant import MIMETYPE_JSON
from api.router.constant import TASK_STATUS_INCOMPLETE, TASK_STATUS_COMPLETE
from tests.conftest import app, client

headers = {
    'Content-Type': MIMETYPE_JSON,
    'Accept': MIMETYPE_JSON
}

test_data = {"name": "買晚餐"}
expected = {"id": 1, "name": "買晚餐", "status": TASK_STATUS_INCOMPLETE}


def test_get_tasks(client):
    response = client.get('/tasks')
    assert response.status == f"{HTTPStatus.OK} OK"
    assert response.get_json() == {"result": []}


def test_create_task(client):
    url = '/task'
    response = client.post(url, data=json.dumps(test_data), headers=headers)
    assert response.content_type == MIMETYPE_JSON
    assert response.json['result'] == expected
    assert response.status == f"{HTTPStatus.CREATED} CREATED"


def test_create_task_without_json(client):
    data = {
        "name": "買晚餐"
    }
    url = '/task'
    response = client.post(url, data=json.dumps(data))
    assert response.json == {"error message": "invalid request post must use json"}
    assert response.status == f"{HTTPStatus.UNSUPPORTED_MEDIA_TYPE} UNSUPPORTED MEDIA TYPE"


def test_query_task_by_id(client):
    url = '/task/1'
    response = client.get(url, headers=headers)
    assert response.content_type == MIMETYPE_JSON
    assert response.json['result'] == expected
    assert response.status == f"{HTTPStatus.OK} OK"


def test_query_task_id_unexisted(client):
    url = '/task/2'
    response = client.get(url, headers=headers)
    assert response.status == f"{HTTPStatus.NOT_FOUND} NOT FOUND"


@pytest.mark.parametrize("name", ["買早餐", "買午餐", "買晚餐"])
@pytest.mark.parametrize("status", [0, 1])
def test_edit_task(client, name, status):
    id = 1
    data = {
        "status": status,
        "name": name
    }
    url = f'/task/{id}'
    response = client.put(url, data=json.dumps(data), headers=headers)
    assert response.content_type == MIMETYPE_JSON
    expected = {"name": name, "status": status, "id": id}
    assert response.json['result'] == expected
    assert response.status == f"{HTTPStatus.OK} OK"

    response = client.get(url)
    assert response.status == f"{HTTPStatus.OK} OK"
    assert response.get_json() == {"result": expected}


def test_delete_task(client):
    id = 1
    url = f'/task/{id}'
    response = client.delete(url, headers=headers)
    assert response.content_type == MIMETYPE_JSON
    assert response.status == f"{HTTPStatus.OK} OK"

    response = client.get(f'/task/{id}')
    assert response.status == f"{HTTPStatus.NOT_FOUND} NOT FOUND"


def test_delete_not_found_task(client):
    id = 1
    url = f'/task/{id}'
    response = client.delete(url, headers=headers)
    assert response.content_type == MIMETYPE_JSON
    assert response.status == f"{HTTPStatus.NOT_FOUND} NOT FOUND"
