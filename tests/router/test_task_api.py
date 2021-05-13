from ..conftest import app, client
from http import HTTPStatus


def test_get_tasks(client):
    response = client.get('/tasks')
    assert response.status == f"{HTTPStatus.OK} OK"
    assert response.get_json() == {"result": []}
