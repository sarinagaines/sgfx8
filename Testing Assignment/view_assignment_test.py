import pytest
import System

def test_view_assignments(grading_system):
    username = "hdjsr7"
    password = "pass1234"

    grading_system.login(username, password)

    course = "cloud_computing"

    assignments= grading_system.usr.view_assignments(course);
    print(assignments)

    users = grading_system.users

    assert users[username][course]["assignment1"]["grade"] == assignments[0]
    assert users[username][course]["assignment1"]["grade"] == assignments[0]
    assert users[username][course]["assignment1"]["grade"] == assignments[0]
    assert users[username][course]["assignment1"]["grade"] == assignments[0]



@pytest.fixture
def grading_system():
    gradingSystem = System.System()
    gradingSystem.load_data()
    return gradingSystem