"""
conftest.py - Shared Test Fixtures
====================================
Provides reusable fixtures for the test suite, including a FastAPI test
client and sample data.
"""

import os
import sys
import pytest

# Ensure the project root is importable
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


@pytest.fixture
def sample_reviews():
    """Return a list of sample review strings for testing."""
    return [
        "The food was absolutely delicious and the service was outstanding!",
        "Terrible experience. Cold food, rude staff, waited 2 hours.",
        "It was okay, nothing special. Average food.",
        "Best restaurant in town! Amazing pasta and great ambiance.",
        "Worst meal I've ever had. Never coming back.",
    ]


@pytest.fixture
def empty_inputs():
    """Return edge-case empty/invalid inputs."""
    return ["", "   ", "\n\t", None]


@pytest.fixture
def special_character_reviews():
    """Return reviews with unusual characters."""
    return [
        "Great food!!! 5/5 stars *****",
        "The fajitas were $$$$ but worth it!!!",
        "Service was <terrible> & slow... #neveragain",
        "Love the pizza 10/10",
    ]


@pytest.fixture
def test_client():
    """Create a FastAPI test client for API testing."""
    from httpx import AsyncClient, ASGITransport
    from main import app
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")
