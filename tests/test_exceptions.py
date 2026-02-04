"""Tests for exception classes."""

import pytest

from guidelinely.exceptions import (
    GuidelinelyAPIError,
    GuidelinelyConnectionError,
    GuidelinelyError,
    GuidelinelyTimeoutError,
)


class TestExceptionHierarchy:
    """Test exception class hierarchy and behavior."""

    def test_guidelinely_error_base(self):
        """Test base exception class."""
        error = GuidelinelyError("Test error message")
        assert str(error) == "Test error message"
        assert isinstance(error, Exception)

    def test_guidelinely_api_error(self):
        """Test API error with status code."""
        error = GuidelinelyAPIError("Not found", status_code=404)
        assert str(error) == "[404] Not found"
        assert error.status_code == 404
        assert error.message == "Not found"
        assert isinstance(error, GuidelinelyError)

    def test_guidelinely_api_error_attributes(self):
        """Test API error attributes are accessible."""
        error = GuidelinelyAPIError("Generic error", status_code=500)
        assert error.message == "Generic error"
        assert error.status_code == 500

    def test_guidelinely_timeout_error(self):
        """Test timeout error."""
        error = GuidelinelyTimeoutError("Request timed out")
        assert str(error) == "Request timed out"
        assert isinstance(error, GuidelinelyError)

    def test_guidelinely_connection_error(self):
        """Test connection error."""
        error = GuidelinelyConnectionError("Connection failed")
        assert str(error) == "Connection failed"
        assert isinstance(error, GuidelinelyError)

    def test_api_error_repr(self):
        """Test __repr__ method of GuidelinelyAPIError."""
        error = GuidelinelyAPIError("Test message", status_code=404)
        repr_str = repr(error)

        # Verify repr contains class name, message, and status code
        assert "GuidelinelyAPIError" in repr_str
        assert "Test message" in repr_str
        assert "404" in repr_str
        assert "message=" in repr_str
        assert "status_code=" in repr_str

    def test_error_inheritance_chain(self):
        """Test that all exceptions inherit from GuidelinelyError."""
        api_error = GuidelinelyAPIError("API error", 500)
        timeout_error = GuidelinelyTimeoutError("Timeout")
        connection_error = GuidelinelyConnectionError("Connection failed")

        # All should be instances of GuidelinelyError
        assert isinstance(api_error, GuidelinelyError)
        assert isinstance(timeout_error, GuidelinelyError)
        assert isinstance(connection_error, GuidelinelyError)

        # All should be instances of Exception
        assert isinstance(api_error, Exception)
        assert isinstance(timeout_error, Exception)
        assert isinstance(connection_error, Exception)

    def test_api_error_with_empty_message(self):
        """Test API error with empty message."""
        error = GuidelinelyAPIError("", status_code=500)
        assert str(error) == "[500] "
        assert error.status_code == 500
        assert error.message == ""

    def test_exception_can_be_raised_and_caught(self):
        """Test that exceptions can be raised and caught properly."""
        with pytest.raises(GuidelinelyAPIError) as exc_info:
            raise GuidelinelyAPIError("Test error", status_code=400)

        assert exc_info.value.status_code == 400
        assert str(exc_info.value) == "[400] Test error"
        assert exc_info.value.message == "Test error"

    def test_exception_catch_by_base_class(self):
        """Test that specific exceptions can be caught by base class."""
        with pytest.raises(GuidelinelyError):
            raise GuidelinelyAPIError("API error", status_code=500)

        with pytest.raises(GuidelinelyError):
            raise GuidelinelyTimeoutError("Timeout")

        with pytest.raises(GuidelinelyError):
            raise GuidelinelyConnectionError("Connection error")
