from fastapi.testclient import TestClient
from main import app



client = TestClient(app)

def test_create_comment():
    # Arrange
    expected = {
        "id": 1,
        "email": "maimiti.saint-marc@efrei.net",
        "phone_number": "02145674",
        "is_planner": False,
        "role": {
            "id": 1,
            "role": "ROLE_USER"
        },
        "account_id": None
    }
    response = client.post("/api/v1/authent/register/user",
                           json={
                               "email":"maimiti.saint-marc@efrei.net",
                               "password":"Password.123",
                               "first_name":"Maimiti",
                               "last_name":"Saint-Marc",
                               "phone_number":"02145674",
                                "photo": "default.jpeg"
                            }
                        )
    assert response.status_code == 201
    data = response.json()
    assert data == expected
