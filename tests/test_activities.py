"""Tests for the GET /activities endpoint."""

import pytest


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all available activities."""
    response = client.get("/activities")
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify all 9 activities are returned
    expected_activities = {
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Tennis Club",
        "Art Studio",
        "Drama Club",
        "Debate Team",
        "Science Club"
    }
    assert set(data.keys()) == expected_activities


def test_get_activities_returns_correct_structure(client):
    """Test that each activity has the required fields."""
    response = client.get("/activities")
    
    assert response.status_code == 200
    data = response.json()
    
    # Check structure of first activity
    activity = data["Chess Club"]
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    
    # Verify data types
    assert isinstance(activity["description"], str)
    assert isinstance(activity["schedule"], str)
    assert isinstance(activity["max_participants"], int)
    assert isinstance(activity["participants"], list)


def test_get_activities_participants_are_emails(client):
    """Test that participants are stored as email strings."""
    response = client.get("/activities")
    
    assert response.status_code == 200
    data = response.json()
    
    # Check that participants in Chess Club are emails
    activity = data["Chess Club"]
    assert len(activity["participants"]) > 0
    for participant in activity["participants"]:
        assert isinstance(participant, str)
        assert "@" in participant  # Basic email format check


def test_get_activities_has_positive_max_participants(client):
    """Test that all activities have positive max_participants."""
    response = client.get("/activities")
    
    assert response.status_code == 200
    data = response.json()
    
    for activity_name, activity_data in data.items():
        assert activity_data["max_participants"] > 0
