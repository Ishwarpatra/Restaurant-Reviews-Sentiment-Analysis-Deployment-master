"""
test_api.py - Tests for the FastAPI API Endpoints
==================================================
Tests for main.py API routes including /health, /api/predict, and
error handling.

Run:
    pytest tests/test_api.py -v

Requires:
    pip install httpx pytest-asyncio
"""

import sys
import os

import pytest
import pytest_asyncio

# Ensure project root is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from httpx import AsyncClient, ASGITransport
from main import app


@pytest_asyncio.fixture
async def client():
    """Async test client for FastAPI."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


# ── Health Check ─────────────────────────────────────────────────────────


@pytest.mark.asyncio
class TestHealthEndpoint:
    """Tests for the /health endpoint."""

    async def test_health_returns_200(self, client):
        response = await client.get("/health")
        assert response.status_code == 200

    async def test_health_returns_status(self, client):
        response = await client.get("/health")
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"

    async def test_health_includes_debug_flag(self, client):
        response = await client.get("/health")
        data = response.json()
        assert "debug" in data


# ── Predict API ──────────────────────────────────────────────────────────


@pytest.mark.asyncio
class TestPredictAPI:
    """Tests for the /api/predict endpoint."""

    async def test_predict_positive_review(self, client):
        response = await client.post(
            "/api/predict",
            json={"message": "The food was absolutely delicious and the service was outstanding"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "prediction" in data
        assert "confidence" in data
        assert "custom_msg" in data
        assert data["prediction"] in (0, 1)
        assert 0 <= data["confidence"] <= 100

    async def test_predict_negative_review(self, client):
        response = await client.post(
            "/api/predict",
            json={"message": "Terrible food, rude staff, worst restaurant ever"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["prediction"] in (0, 1)

    async def test_predict_response_has_custom_msg(self, client):
        response = await client.post(
            "/api/predict",
            json={"message": "Amazing pasta and wonderful atmosphere"},
        )
        data = response.json()
        assert isinstance(data["custom_msg"], str)
        assert len(data["custom_msg"]) > 0

    async def test_predict_confidence_is_percentage(self, client):
        response = await client.post(
            "/api/predict",
            json={"message": "Good experience overall"},
        )
        data = response.json()
        assert isinstance(data["confidence"], (int, float))
        assert 0 <= data["confidence"] <= 100


# ── Error Handling ───────────────────────────────────────────────────────


@pytest.mark.asyncio
class TestErrorHandling:
    """Tests for API error handling."""

    async def test_empty_message_returns_422(self, client):
        """Empty message should trigger validation error."""
        response = await client.post(
            "/api/predict",
            json={"message": ""},
        )
        assert response.status_code == 422

    async def test_whitespace_message_returns_422(self, client):
        """Whitespace-only message should trigger validation error."""
        response = await client.post(
            "/api/predict",
            json={"message": "   "},
        )
        assert response.status_code == 422

    async def test_missing_field_returns_422(self, client):
        """Missing 'message' field should return 422."""
        response = await client.post(
            "/api/predict",
            json={},
        )
        assert response.status_code == 422

    async def test_wrong_content_type_returns_422(self, client):
        """Sending non-JSON should fail."""
        response = await client.post(
            "/api/predict",
            content="This is plain text",
            headers={"Content-Type": "text/plain"},
        )
        assert response.status_code == 422

    async def test_nonexistent_route_returns_404(self, client):
        """Unknown route should return 404."""
        response = await client.get("/api/nonexistent")
        assert response.status_code == 404

    async def test_get_on_predict_returns_405(self, client):
        """GET on /api/predict should return 405 Method Not Allowed."""
        response = await client.get("/api/predict")
        assert response.status_code == 405

    async def test_very_long_input(self, client):
        """Extremely long review should be handled gracefully."""
        long_review = "Great food " * 1000  # ~11000 chars, exceeds MAX_REVIEW_LENGTH
        response = await client.post(
            "/api/predict",
            json={"message": long_review},
        )
        # Should either process or return 422 for length limit
        assert response.status_code in (200, 422)


# ── Root Endpoint ────────────────────────────────────────────────────────


@pytest.mark.asyncio
class TestRootEndpoint:
    """Tests for the / root endpoint."""

    async def test_root_returns_response(self, client):
        """Root should return 200 (either frontend or JSON message)."""
        response = await client.get("/")
        assert response.status_code == 200
