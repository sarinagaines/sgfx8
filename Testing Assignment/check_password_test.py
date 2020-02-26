import pytest
import System


def test_check_password(grading_system):
	username = "akend3"
	password = "123454321"

	grading_system.login(username, password)

	grading_system.check_password(username, password)
	assert grading_system.usr.password == password

@pytest.fixture
def grading_system():
    gradingSystem = System.System()
    gradingSystem.load_data()
    return gradingSystem