import pytest
import System


def test_add_student(grading_system):
    username = "goggins"
    password = "augurrox"
    grading_system.login(username, password)

    name = "yted91"
    course = "databases"

    grading_system.usr.add_student(name, course)
    grading_system.reload_data()
    users = grading_system.users
    assert users[name] == name

@pytest.fixture
def grading_system():
    gradingSystem = System.System()
    gradingSystem.load_data()
    return gradingSystem
