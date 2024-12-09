import pytest
from rest_framework.test import APIClient



url = "http://localhost:8000/api/user/create"
req = APIClient()

def make_post_requests(password="commompassword", email="commomemail@gmail.com", username="commomusername"):
    data = req.post(
        path=url,
        data={
            "username": username,
            "email": email,
            "password": password,
        }
    )
    return data





@pytest.mark.django_db
def test_password_is_not_valid_by_validators():
    """checking if password's validators -CHARACTER- is ok"""
    data = make_post_requests(password="passwo@rd0914")
    assert data.status_code == 400

@pytest.mark.django_db
def test_password_is_not_valid_by_string_length():
    """checking if password's validators -LENGTH- is ok"""
    data = make_post_requests(password="WQE321s")
    assert data.status_code == 400

@pytest.mark.django_db
def test_password_is_valid_by_length_and_validators():
    """checking if password  - length and validators- is valid"""
    data = make_post_requests(password="WQE321s2")
    assert data.status_code == 201

@pytest.mark.django_db
def test_email_is_valid():
    """ TESTING IF EMAIL IS VALID """
    data = make_post_requests(email="testingpassword@gmail.com")
    assert data.status_code == 201

@pytest.mark.django_db
def test_email_is_not_valid():
    """TESTING @ CHARACTER IN EMAIL, and it serves for the others"""
    data = make_post_requests(email="testingpasswordgmail.com")
    assert data.status_code == 400

@pytest.mark.django_db
def test_email_is_not_valid_2():
    """TESTING . CHARACTER IN EMAIL"""
    data = make_post_requests(email="testingpassword@gmailcom")
    assert data.status_code == 400

@pytest.mark.django_db
def test_username_is_not_valid():
    """TESTING NOT ALLOWED CHARACTERS IN USERNAME"""
    data = make_post_requests(username="testing@password")
    assert data.status_code == 400

@pytest.mark.django_db
def test_username_is_valid():
    """TESTING ALLOWED CHARACTERS IN USERNAME"""
    data = make_post_requests(username="acbsdwerqa23DWDQDasS2")
    assert data.status_code == 201

@pytest.mark.django_db
def test_email_unique_validation():
    """CHECKING IF RETURNS ERROR IF ALREADY EXISTS AN EMAIL. ALERT: USING DEFAULT EMAIL FROM THE FUNCTION"""
    make_post_requests()
    data = make_post_requests(username="randomstring")
    assert data.status_code == 400

@pytest.mark.django_db
def test_username_unique_validation():
    """CHECKING IF RETURNS ERROR IF ALREADY EXISTS AN USERNAME. ALERT: USING DEFAULT USERNAME FROM THE FUNCTION"""
    make_post_requests()
    data = make_post_requests(email="randomemail@gmail.com")
    assert data.status_code == 400
