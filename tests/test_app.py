import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

def reset_activities():
    # Reset the in-memory activities for test isolation
    for activity in activities.values():
        activity["participants"].clear()

def test_list_activities():
    # Arrange
    reset_activities()
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_signup_for_activity():
    # Arrange
    reset_activities()
    email = "student1@example.com"
    activity = list(activities.keys())[0]
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert email in activities[activity]["participants"]

def test_prevent_duplicate_signup():
    # Arrange
    reset_activities()
    email = "student2@example.com"
    activity = list(activities.keys())[0]
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_unregister_from_activity():
    # Arrange
    reset_activities()
    email = "student3@example.com"
    activity = list(activities.keys())[0]
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert email not in activities[activity]["participants"]

def test_unregister_nonexistent_participant():
    # Arrange
    reset_activities()
    email = "ghost@example.com"
    activity = list(activities.keys())[0]
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 404
    assert "not signed up" in response.json()["detail"]

def test_signup_invalid_activity():
    # Arrange
    reset_activities()
    email = "student4@example.com"
    activity = "NonExistentActivity"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_unregister_invalid_activity():
    # Arrange
    reset_activities()
    email = "student5@example.com"
    activity = "NonExistentActivity"
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
