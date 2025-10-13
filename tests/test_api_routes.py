"""
Tests for API routes
--------------------

tests/test_api_routes.py
"""

import pytest
from fermi_paradox import create_app
from bs4 import BeautifulSoup


@pytest.fixture()
def client():
    """Flask test client for making requests."""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
    })
    with app.test_client() as client:
        yield client


def test_home_route(client):
    """Ensure the home page renders successfully."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Drake" in response.data or b"Fermi" in response.data


def test_drake_route_get(client):
    """Ensure the Drake Equation page renders with parameters."""
    response = client.get("/api/drake")
    assert response.status_code == 200
    # The page should mention something about civilization or parameters
    assert b"Drake Equation" in response.data or b"civilization" in response.data


def test_drake_route_post(client):
    """POST form data to Drake endpoint and ensure it recalculates."""
    data = {
        "R_": 2,
        "f_p": 0.8,
        "n_e": 0.2,
        "f_l": 0.5,
        "f_i": 1,
        "f_c": 0.1,
        "L": 1000000,
    }
    response = client.post("/api/drake", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Drake Equation" in response.data


def test_drake_value_displayed(client):
    response = client.get("/api/drake")
    soup = BeautifulSoup(response.data, "html.parser")
    assert soup.find("h2", class_="display-4 text-success") is not None
