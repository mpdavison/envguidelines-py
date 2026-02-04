"""Tests for error handling in metadata API endpoints."""

import pytest

from guidelinely import (
    get_stats,
    list_media,
    list_sources,
    readiness_check,
)
from guidelinely.auth import get_api_base
from guidelinely.exceptions import GuidelinelyAPIError

API_BASE = get_api_base()


class TestReadinessCheckErrors:
    """Test error handling for readiness_check endpoint."""

    def test_readiness_check_service_unavailable(self, httpx_mock):
        """Test readiness check when service is not ready."""
        httpx_mock.add_response(
            method="GET",
            url=f"{API_BASE}/ready",
            json={"status": "not_ready", "reason": "Database unavailable"},
            status_code=503,
        )

        with pytest.raises(GuidelinelyAPIError) as exc_info:
            readiness_check()

        assert exc_info.value.status_code == 503
        assert "not_ready" in str(exc_info.value) or "503" in str(exc_info.value)

    def test_readiness_check_internal_error(self, httpx_mock):
        """Test readiness check with internal server error."""
        httpx_mock.add_response(
            method="GET",
            url=f"{API_BASE}/ready",
            json={"detail": "Internal error"},
            status_code=500,
        )

        with pytest.raises(GuidelinelyAPIError) as exc_info:
            readiness_check()

        assert exc_info.value.status_code == 500


class TestListMediaErrors:
    """Test error handling for list_media endpoint."""

    def test_list_media_internal_error(self, httpx_mock):
        """Test list_media with internal server error."""
        httpx_mock.add_response(
            method="GET",
            url=f"{API_BASE}/media",
            json={"detail": "Database error"},
            status_code=500,
        )

        with pytest.raises(GuidelinelyAPIError) as exc_info:
            list_media()

        assert exc_info.value.status_code == 500
        assert "Database error" in str(exc_info.value) or "500" in str(exc_info.value)

    def test_list_media_service_unavailable(self, httpx_mock):
        """Test list_media when service is unavailable."""
        httpx_mock.add_response(
            method="GET",
            url=f"{API_BASE}/media",
            json={"detail": "Service temporarily unavailable"},
            status_code=503,
        )

        with pytest.raises(GuidelinelyAPIError) as exc_info:
            list_media()

        assert exc_info.value.status_code == 503


class TestListSourcesErrors:
    """Test error handling for list_sources endpoint."""

    def test_list_sources_internal_error(self, httpx_mock):
        """Test list_sources with internal server error."""
        httpx_mock.add_response(
            method="GET",
            url=f"{API_BASE}/sources",
            json={"detail": "Failed to fetch sources"},
            status_code=500,
        )

        with pytest.raises(GuidelinelyAPIError) as exc_info:
            list_sources()

        assert exc_info.value.status_code == 500

    def test_list_sources_bad_gateway(self, httpx_mock):
        """Test list_sources with bad gateway error."""
        httpx_mock.add_response(
            method="GET",
            url=f"{API_BASE}/sources",
            json={"detail": "Bad gateway"},
            status_code=502,
        )

        with pytest.raises(GuidelinelyAPIError) as exc_info:
            list_sources()

        assert exc_info.value.status_code == 502


class TestGetStatsErrors:
    """Test error handling for get_stats endpoint."""

    def test_get_stats_internal_error(self, httpx_mock):
        """Test get_stats with internal server error."""
        httpx_mock.add_response(
            method="GET",
            url=f"{API_BASE}/stats",
            json={"detail": "Statistics computation failed"},
            status_code=500,
        )

        with pytest.raises(GuidelinelyAPIError) as exc_info:
            get_stats()

        assert exc_info.value.status_code == 500

    def test_get_stats_service_unavailable(self, httpx_mock):
        """Test get_stats when service is unavailable."""
        httpx_mock.add_response(
            method="GET",
            url=f"{API_BASE}/stats",
            json={"detail": "Statistics service down"},
            status_code=503,
        )

        with pytest.raises(GuidelinelyAPIError) as exc_info:
            get_stats()

        assert exc_info.value.status_code == 503

    def test_get_stats_gateway_timeout(self, httpx_mock):
        """Test get_stats with gateway timeout."""
        httpx_mock.add_response(
            method="GET",
            url=f"{API_BASE}/stats",
            json={"detail": "Gateway timeout"},
            status_code=504,
        )

        with pytest.raises(GuidelinelyAPIError) as exc_info:
            get_stats()

        assert exc_info.value.status_code == 504
