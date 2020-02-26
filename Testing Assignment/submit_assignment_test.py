import pytest
import System


def test_submit_assignment(grading_system):
    username = "hdjsr7"
    password = "pass1234"
    grading_system.login(username, password)

    course = "cloud_computing"
    assignment = "assignment1"
    submission = "Blahhhhh"
    submission_date = "03/01/20"

    grading_system.usr.submit_assignment(course, assignment, submission, submission_date)

    # assert grading_system.usr.course == course
    # assert grading_system.usr.assignment == assignment
    # assert grading_system.usr.submission == submission
    # assert grading_system.usr.submission_date == submission_date

    users = grading_system.users

    assert users[username][course] == course
    assert users[username][course][assignment] == assignment
    assert users[username][course][assignment][submission] == submission
    assert users[username][course][assignment][submission_date] == submission_date

@pytest.fixture
def grading_system():
    gradingSystem = System.System()
    gradingSystem.load_data()
    return gradingSystem
