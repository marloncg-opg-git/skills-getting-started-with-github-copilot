"""Tests for the GET / root endpoint."""


def test_root_redirects_to_static_index(client):
    """Test that GET / redirects to /static/index.html."""
    response = client.get("/", follow_redirects=False)
    
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_root_follows_redirect_to_static(client):
    """Test that following the redirect returns the HTML page."""
    response = client.get("/", follow_redirects=True)
    
    assert response.status_code == 200
    # Verify it's HTML content
    assert "<!DOCTYPE html>" in response.text or "<html" in response.text
