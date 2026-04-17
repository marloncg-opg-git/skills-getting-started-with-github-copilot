"""Tests for the POST /activities/{activity_name}/signup endpoint."""

import pytest


def test_signup_successfully_adds_participant(client, sample_activity, sample_email):
    """Test that signing up a new student adds them to the activity."""
    # Get initial participant count
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()[sample_activity]["participants"])
    
    # Sign up the student
    response = client.post(
        f"/activities/{sample_activity}/signup",
        params={"email": sample_email}
    )
    
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {sample_email} for {sample_activity}"
    
    # Verify participant count increased
    updated_response = client.get("/activities")
    updated_count = len(updated_response.json()[sample_activity]["participants"])
    assert updated_count == initial_count + 1
    
    # Verify the email is in participants
    assert sample_email in updated_response.json()[sample_activity]["participants"]


def test_signup_nonexistent_activity_returns_404(client, sample_email, nonexistent_activity):
    """Test that signing up for a non-existent activity returns 404."""
    response = client.post(
        f"/activities/{nonexistent_activity}/signup",
        params={"email": sample_email}
    )
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_participant_returns_400(client, sample_activity, sample_email):
    """Test that signing up a participant twice returns 400 error."""
    # First signup
    client.post(
        f"/activities/{sample_activity}/signup",
        params={"email": sample_email}
    )
    
    # Attempt duplicate signup
    response = client.post(
        f"/activities/{sample_activity}/signup",
        params={"email": sample_email}
    )
    
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_signup_different_students_same_activity(client, sample_activity):
    """Test that multiple different students can sign up for the same activity."""
    email1 = "student1@mergington.edu"
    email2 = "student2@mergington.edu"
    
    # Sign up first student
    response1 = client.post(
        f"/activities/{sample_activity}/signup",
        params={"email": email1}
    )
    assert response1.status_code == 200
    
    # Sign up second student
    response2 = client.post(
        f"/activities/{sample_activity}/signup",
        params={"email": email2}
    )
    assert response2.status_code == 200
    
    # Verify both are in participants
    activities_response = client.get("/activities")
    participants = activities_response.json()[sample_activity]["participants"]
    assert email1 in participants
    assert email2 in participants


def test_signup_same_student_different_activities(client, sample_email):
    """Test that the same student can sign up for multiple activities."""
    activity1 = "Chess Club"
    activity2 = "Programming Class"
    
    # Sign up for first activity
    response1 = client.post(
        f"/activities/{activity1}/signup",
        params={"email": sample_email}
    )
    assert response1.status_code == 200
    
    # Sign up for second activity
    response2 = client.post(
        f"/activities/{activity2}/signup",
        params={"email": sample_email}
    )
    assert response2.status_code == 200
    
    # Verify student is in both activities
    activities_response = client.get("/activities")
    data = activities_response.json()
    assert sample_email in data[activity1]["participants"]
    assert sample_email in data[activity2]["participants"]
