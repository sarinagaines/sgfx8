import Staff
import System
import pytest


def test_create_assignment(grading_system):
    username = "cmhbf5"
    password ="bestTA"
    grading_system.login(username, password)

    assignment_name = 'assignment3'
    due_date = '2/25/2020'
    course = 'comp_sci'

    grading_system.usr.create_assignment(assignment_name, due_date, course)
    grading_system.reload_data()
    courses = grading_system.courses

    assert courses[course]["assignments"][assignment_name]["due_date"] == due_date

@pytest.fixture
def grading_system():
    gradingSystem = System.System()
    gradingSystem.load_data()
    return gradingSystem