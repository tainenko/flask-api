from api.model.task import Task
import pytest


@pytest.mark.parametrize("id", [1, 2, 3])
@pytest.mark.parametrize("name", ["買早餐", "買午餐", "買晚餐"])
@pytest.mark.parametrize("status", [0, 1])
def test_new_task(id, name, status):
    task = Task(id=id, name=name, status=status)
    assert task.id == id
    assert task.name == name
    assert task.status == status
