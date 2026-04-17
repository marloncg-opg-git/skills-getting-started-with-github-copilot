"""Tests for the DELETE /activities/{activity_name}/participants/{email} endpoint."""

import pytest


def test_delete_successfully_removes_participant(client, sample_activity, sample_email):
    """Test that deleting a participant removes them from the activity."""
    # First, sign up the student
    client.post(
        f"/activities/{sample_activity}/signup",
        params={"email": sample_email}
    )
    
    # Verify they're in the activity
    response = client.get("/activities")
    assert sample_email in response.json()[sample_activity]["participants"]
    initial_count = len(response.json()[sample_activity]["participants"])
    
    # Delete the participant
    delete_response = client.delete(
        f"/activities/{sample_activity}/participants/{sample_email}"
    )
    
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == f"Removed {sample_email} from {sample_activity}"
    
    # Verify they're no longer in the activity
    updated_response = client.get("/activities")
    assert sample_email not in updated_response.json()[sample_activity]["participants"]
    assert len(updated_response.json()[sample_activity]["participants"]) == initial_count - 1


def test_delete_nonexistent_activity_returns_404(client, sample_email, nonexistent_activity):
    """Test that deleting from a non-existent activity returns 404."""
    response = client.delete(
        f"/activities/{nonexistent_activity}/participants/{sample_email}"
    )
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_delete_nonexistent_participant_returns_400(client, sample_activity, nonexistent_email):
    """Test that deleting a non-existent participant returns 400."""
    response = client.delete(
        f"/activities/{sample_activity}/participants/{nonexistent_email}"
    )
    
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"].lower()


def test_delete_removes_only_specified_participant(client, sample_activity):
    """Test that deleting one participant doesn't affect others."""
    email1 = "student1@mergington.edu"
    email2 = "student2@mergington.edu"
    
    # Sign up both students
    client.post(
        f"/activities/{sample_activity}/signup",
        params={"email": email1}
    )
    client.post(
        f"/activities/{sample_activity}/signup",
        params={"email": email2}
    )
    
    # Delete first participant
    response = client.delete(
        f"/activities/{sample_activity}/participants/{email1}"
    )
    assert response.status_code == 200
    
    # Verify only first is removed, second remains
    activities_response = client.get("/activities")
    participants = activities_response.json()[sample_activity]["participants"]
    assert email1 not in participants
    assert email2 in participants


def test_delete_twice_returns_error(client, sample_activity, sample_email):
    """Test that deleting the same participant twice returns an error on the second attempt."""
    # Sign up student
    client.post(
        f"/activities/{sample_activity}/signup",
        params={"email": sample_email}
    )
    
    # First delete succeeds
    response1 = client.delete(
        f"/activities/{sample_activity}/participants/{sample_email}"
    )
    assert response1.status_code == 200
    
    # Second delete fails
    response2 = client.delete(
        f"/activities/{sample_activity}/participants/{sample_email}"
    )
    assert response2.status_code == 400
    assert "not signed up" in response2.json()["detail"].lower()


def test_delete_allows_same_student_to_rejoin(client, sample_activity, sample_email):
    """Test that a deleted participant can sign up again."""
    # Sign up
    client.post(
        f"/activities/{sample_activity}/signup",
        params={"email": sample_email}
    )
    
    # Delete
    client.delete(
        f"/activities/{sample_activity}/participants/{sample_email}"
    )
    
    # Sign up again
    response = client.post(
        f"/activities/{sample_activity}/signup",
        params={"email": sample_email}
    )
    assert response.status_code == 200
    
    # Verify they're back in the activity
    activities_response = client.get("/activities")
    assert sample_email in activities_response.json()[sample_activity]["participants"]
