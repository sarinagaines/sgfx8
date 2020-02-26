import pytest
import System

def test_check_grades(grading_system):
    username = "hdjsr7"
    password = "pass1234"

    grading_system.login(username, password)

    course = "cloud_computing"

    grade = grading_system.usr.check_grades(course);

    users = grading_system.users

    assert users[username][course]["assignment1"]["grade"] == grade[0]
    assert users[username][course]["assignment2"]["grade"] == grade[1]



@pytest.fixture
def grading_system():
    gradingSystem = System.System()
    gradingSystem.load_data()
    return gradingSystem