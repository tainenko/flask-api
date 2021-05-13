from api.model.task import Task


def test_new_task():
    task = Task(id=1, name="買晚餐", status=0)
    assert task.id == 1
    assert task.name == "買晚餐"
    assert task.status == 0
