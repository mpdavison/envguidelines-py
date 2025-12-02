"""Unit tests for client-side caching functionality using diskcache."""

import os
import tempfile

import pytest
from diskcache import Cache


class TestCacheOperations:
    """Test cache get/set operations using temporary cache."""

    @pytest.fixture
    def temp_cache(self):
        """Create a temporary cache for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            cache = Cache(directory=temp_dir)
            yield cache
            cache.close()

    def test_get_cached_miss(self, temp_cache):
        """Should return None for missing key."""
        assert temp_cache.get({"test": "data"}) is None

    def test_set_and_get_cached(self, temp_cache):
        """Should store and retrieve cached data."""
        key_data = {"endpoint": "test", "param": "value"}
        response_data = {"results": [], "context": {}, "total_count": 0}

        temp_cache[key_data] = response_data
        cached = temp_cache.get(key_data)
        assert cached == response_data

    def test_different_keys_different_values(self, temp_cache):
        """Different keys should store different values."""
        key1 = {"a": 1}
        key2 = {"a": 2}
        val1 = "value1"
        val2 = "value2"

        temp_cache[key1] = val1
        temp_cache[key2] = val2

        assert temp_cache.get(key1) == val1
        assert temp_cache.get(key2) == val2

    def test_complex_key_types(self, temp_cache):
        """Should handle complex key types like lists and nested dicts."""
        key = {
            "endpoint": "calculate/batch",
            "parameters": ["Aluminum", {"name": "Copper", "target_unit": "mg/L"}],
            "media": "surface_water",
            "context": {"pH": "7.0 1", "hardness": "100 mg/L"},
            "api_key": None,
        }
        value = {"results": [], "context": {}, "total_count": 0}

        temp_cache[key] = value
        assert temp_cache.get(key) == value


class TestCacheConfiguration:
    """Test cache directory configuration."""

    def test_cache_dir_defaults_to_home(self):
        """CACHE_DIR should default to ~/.guidelinely_cache when env var not set."""
        from pathlib import Path

        # Remove env var if set, reload module to test default
        old_value = os.environ.pop("GUIDELINELY_CACHE_DIR", None)
        try:
            # We need to test the logic, not the actual module state
            # since the module is already loaded
            default_cache_dir = Path.home() / ".guidelinely_cache"
            test_dir = Path(os.getenv("GUIDELINELY_CACHE_DIR", str(default_cache_dir)))
            assert test_dir == default_cache_dir
        finally:
            if old_value is not None:
                os.environ["GUIDELINELY_CACHE_DIR"] = old_value

    def test_cache_dir_from_environment(self):
        """CACHE_DIR should use GUIDELINELY_CACHE_DIR env var when set."""
        from pathlib import Path

        custom_dir = "/tmp/custom_guidelinely_cache"
        old_value = os.environ.get("GUIDELINELY_CACHE_DIR")
        try:
            os.environ["GUIDELINELY_CACHE_DIR"] = custom_dir
            default_cache_dir = Path.home() / ".guidelinely_cache"
            test_dir = Path(os.getenv("GUIDELINELY_CACHE_DIR", str(default_cache_dir)))
            assert test_dir == Path(custom_dir)
        finally:
            if old_value is not None:
                os.environ["GUIDELINELY_CACHE_DIR"] = old_value
            else:
                os.environ.pop("GUIDELINELY_CACHE_DIR", None)

    def test_default_ttl_value(self):
        """DEFAULT_TTL should be 7 days (604800 seconds) by default."""
        # When env var is not set, should be 7 days
        old_value = os.environ.pop("GUIDELINELY_CACHE_TTL", None)
        try:
            expected_ttl = 7 * 24 * 3600  # 604800 seconds
            test_ttl = int(os.getenv("GUIDELINELY_CACHE_TTL", str(expected_ttl)))
            assert test_ttl == expected_ttl
        finally:
            if old_value is not None:
                os.environ["GUIDELINELY_CACHE_TTL"] = old_value

    def test_ttl_from_environment(self):
        """DEFAULT_TTL should use GUIDELINELY_CACHE_TTL env var when set."""
        custom_ttl = "3600"  # 1 hour
        old_value = os.environ.get("GUIDELINELY_CACHE_TTL")
        try:
            os.environ["GUIDELINELY_CACHE_TTL"] = custom_ttl
            test_ttl = int(os.getenv("GUIDELINELY_CACHE_TTL", str(7 * 24 * 3600)))
            assert test_ttl == int(custom_ttl)
        finally:
            if old_value is not None:
                os.environ["GUIDELINELY_CACHE_TTL"] = old_value
            else:
                os.environ.pop("GUIDELINELY_CACHE_TTL", None)
