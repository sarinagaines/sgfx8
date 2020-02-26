import pytest
import System

def test_check_ontime(grading_system):
    username = "hdjsr7"
    password = "pass1234"

    grading_system.login(username,password)

    submission_date1 = "2/3/2020"
    submission_date2 = "2/1/2020"
    due_date = "2/2/2020"


    assert grading_system.usr.check_ontime(submission_date1,due_date) == False
    assert grading_system.usr.check_ontime(submission_date2,due_date) == True


@pytest.fixture
def grading_system():
    gradingSystem = System.System()
    gradingSystem.load_data()
    return gradingSystem
