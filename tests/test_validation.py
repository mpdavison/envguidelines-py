"""Tests for validation edge cases and boundary conditions."""

import pytest

from guidelinely import (
    calculate_batch,
    match_parameters,
)
from guidelinely.auth import get_api_base
from guidelinely.cache import cache
from guidelinely.exceptions import GuidelinelyAPIError

API_BASE = get_api_base()


class TestMatchParametersBoundaries:
    """Test boundary conditions for match_parameters."""

    def test_match_parameters_exactly_50(self, httpx_mock):
        """Test matching with exactly 50 parameters (boundary condition)."""
        cache.clear()

        # Create 50 parameter names
        params = [f"Parameter_{i}" for i in range(50)]

        # Mock response with 50 results
        mock_results = [
            {
                "query": param,
                "matches": [
                    {
                        "parameter": param,
                        "parameter_specification": f"{param}, Test",
                        "confidence": 0.95,
                        "media_types": ["surface_water"],
                        "match_type": "exact",
                        "strategy_used": "simple",
                    }
                ],
            }
            for param in params
        ]

        httpx_mock.add_response(
            method="POST",
            url=f"{API_BASE}/parameters/match",
            json={
                "results": mock_results,
                "total_queries": 50,
                "timestamp": "2025-12-16T10:30:00Z",
            },
            status_code=200,
        )

        result = match_parameters(params)
        assert result.total_queries == 50
        assert len(result.results) == 50

    def test_match_parameters_invalid_threshold_negative(self, httpx_mock):
        """Test that negative threshold is handled."""
        cache.clear()

        # Mock will still be called if validation doesn't catch it
        httpx_mock.add_response(
            method="POST",
            url=f"{API_BASE}/parameters/match",
            json={"detail": "threshold must be between 0 and 1"},
            status_code=422,
        )

        # API should return validation error
        with pytest.raises(GuidelinelyAPIError) as exc_info:
            match_parameters(["Copper"], threshold=-0.5)

        assert exc_info.value.status_code == 422

    def test_match_parameters_invalid_threshold_too_high(self, httpx_mock):
        """Test that threshold > 1.0 is handled."""
        cache.clear()

        httpx_mock.add_response(
            method="POST",
            url=f"{API_BASE}/parameters/match",
            json={"detail": "threshold must be between 0 and 1"},
            status_code=422,
        )

        with pytest.raises(GuidelinelyAPIError) as exc_info:
            match_parameters(["Copper"], threshold=1.5)

        assert exc_info.value.status_code == 422

    def test_match_parameters_invalid_strategy(self, httpx_mock):
        """Test that invalid strategy value is handled."""
        cache.clear()

        httpx_mock.add_response(
            method="POST",
            url=f"{API_BASE}/parameters/match",
            json={"detail": "strategy must be one of: fuzzy, exact, semantic"},
            status_code=422,
        )

        with pytest.raises(GuidelinelyAPIError) as exc_info:
            match_parameters(["Copper"], strategy="invalid_strategy")

        assert exc_info.value.status_code == 422

    def test_match_parameters_zero_threshold(self, httpx_mock):
        """Test matching with threshold=0 (boundary condition)."""
        cache.clear()

        httpx_mock.add_response(
            method="POST",
            url=f"{API_BASE}/parameters/match",
            json={
                "results": [
                    {
                        "query": "Copper",
                        "matches": [
                            {
                                "parameter": "Copper",
                                "parameter_specification": "Copper, Total",
                                "confidence": 1.0,
                                "media_types": ["surface_water"],
                                "match_type": "exact",
                                "strategy_used": "simple",
                            },
                            {
                                "parameter": "Copper, Dissolved",
                                "parameter_specification": "Copper, Dissolved",
                                "confidence": 0.8,
                                "media_types": ["surface_water"],
                                "match_type": "fuzzy",
                                "strategy_used": "simple",
                            },
                            {
                                "parameter": "Copper, Total",
                                "parameter_specification": "Copper, Total",
                                "confidence": 0.1,
                                "media_types": ["surface_water"],
                                "match_type": "fuzzy",
                                "strategy_used": "simple",
                            },
                        ],
                    }
                ],
                "total_queries": 1,
                "timestamp": "2025-12-16T10:30:00Z",
            },
            status_code=200,
        )

        result = match_parameters(["Copper"], threshold=0.0)
        # Should return all matches since threshold is 0
        assert len(result.results[0].matches) >= 1

    def test_match_parameters_threshold_one(self, httpx_mock):
        """Test matching with threshold=1.0 (boundary condition)."""
        cache.clear()

        httpx_mock.add_response(
            method="POST",
            url=f"{API_BASE}/parameters/match",
            json={
                "results": [
                    {
                        "query": "Copper",
                        "matches": [
                            {
                                "parameter": "Copper",
                                "parameter_specification": "Copper, Total",
                                "confidence": 1.0,
                                "media_types": ["surface_water"],
                                "match_type": "exact",
                                "strategy_used": "simple",
                            },
                        ],
                    }
                ],
                "total_queries": 1,
                "timestamp": "2025-12-16T10:30:00Z",
            },
            status_code=200,
        )

        result = match_parameters(["Copper"], threshold=1.0)
        # Should only return exact matches
        assert len(result.results[0].matches) == 1
        assert result.results[0].matches[0].confidence == 1.0


class TestCalculateBatchBoundaries:
    """Test boundary conditions for calculate_batch."""

    def test_calculate_batch_exactly_50(self, httpx_mock):
        """Test batch calculation with exactly 50 parameters (boundary)."""
        cache.clear()

        # Create 50 parameter names
        params = [f"Parameter_{i}" for i in range(50)]
        context = {"pH": "7.0 1", "hardness": "100 mg/L"}

        # Mock response with 50 results using correct structure
        mock_results = [
            {
                "id": i,
                "parameter": param,
                "parameter_specification": f"{param}, Test",
                "media": "surface_water",
                "value": "[10 μg/L,100 μg/L]",
                "lower": 10.0,
                "upper": 100.0,
                "unit": "μg/L",
                "is_calculated": False,
                "source": "Test Source",
                "receptor": "Aquatic Life",
                "exposure_duration": "chronic",
                "purpose": "protection",
                "table": "Table 1",
                "table_name": "Test Guidelines",
                "application": "Freshwater",
                "basis": "Chronic toxicity",
            }
            for i, param in enumerate(params)
        ]

        httpx_mock.add_response(
            method="POST",
            url=f"{API_BASE}/calculate/batch",
            json={
                "results": mock_results,
                "context": context,
                "total_count": 50,
                "timestamp": "2025-12-16T10:30:00Z",
            },
            status_code=200,
        )

        result = calculate_batch(params, "surface_water", context)
        assert result.total_count == 50
        assert len(result.results) == 50
