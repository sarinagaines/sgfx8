import pytest
import System

def test_login(grading_system):
    username = 'akend3'
    password =  '123454321'
    grading_system.login(username, password)
    assert  grading_system.usr.name == username


@pytest.fixture
def grading_system():
    gradingSystem = System.System()
    gradingSystem.load_data()
    return gradingSystem