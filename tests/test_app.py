import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data

def test_signup_and_unregister():
    activity = "Chess Club"
    email = "testuser@mergington.edu"

    # Ensure not already signed up
    client.delete(f"/activities/{activity}/unregister", params={"email": email})

    # Sign up
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]

    # Duplicate signup should fail
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 400

    # Unregister
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 200
    assert f"Unregistered {email} from {activity}" in response.json()["message"]

    # Unregister again should fail
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 404

@pytest.mark.parametrize("activity", [
    "Programming Class",
    "Gym Class",
    "Soccer Team",
    "Basketball Club",
    "Art Club",
    "Drama Society",
    "Math Olympiad",
    "Science Club"
])
def test_activity_exists(activity):
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert activity in data
