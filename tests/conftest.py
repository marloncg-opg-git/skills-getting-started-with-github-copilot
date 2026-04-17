"""Pytest configuration and fixtures for FastAPI tests."""

import pytest
import copy
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Provide a TestClient with a fresh copy of activities for each test.
    This ensures test isolation and prevents tests from affecting each other.
    """
    # Create a deep backup of the original activities
    original_activities = copy.deepcopy(activities)
    
    yield TestClient(app)
    
    # Reset activities to original state after test completes
    activities.clear()
    activities.update(copy.deepcopy(original_activities))


@pytest.fixture
def sample_email():
    """Fixture providing a sample student email for testing."""
    return "testuser@mergington.edu"


@pytest.fixture
def sample_activity():
    """Fixture providing a sample activity name for testing."""
    return "Chess Club"


@pytest.fixture
def nonexistent_activity():
    """Fixture providing a non-existent activity name for testing."""
    return "Nonexistent Activity"


@pytest.fixture
def nonexistent_email():
    """Fixture providing a non-existent email for testing."""
    return "nonexistent@mergington.edu"
