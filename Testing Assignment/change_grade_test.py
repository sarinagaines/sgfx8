import pytest
import System

def test_change_grade(grading_system):
        username = "cmhbf5"
        password = "bestTA"
        grading_system.login(username, password)

        user = "hdjsr7"
        course = "cloud_computing"
        assignment = "assignment1"
        grade = 50

        grading_system.usr.change_grade(username, course, assignment, grade)
        assert grading_system.urs.username.grade == grade

@pytest.fixture
def grading_system():
        gradingSystem = System.System()
        gradingSystem.load_data()
        return gradingSystem
