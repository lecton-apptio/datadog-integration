"""Tests for core functionality."""

import os
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError, URLError

from datadog_integration.core import (
    DatadogValidator,
    ValidationResult,
    build_curl_command,
    load_env_file,
    redact_secret,
    request_json,
    safe_request_json,
)


class TestValidationResult:
    """Tests for ValidationResult class."""

    def test_init_success(self) -> None:
        """Test ValidationResult initialization with success."""
        result = ValidationResult(
            ok=True,
            status=200,
            curl="curl command",
            data={"valid": True},
        )
        assert result.ok is True
        assert result.status == 200
        assert result.curl == "curl command"
        assert result.data == {"valid": True}
        assert result.error == {}

    def test_init_error(self) -> None:
        """Test ValidationResult initialization with error."""
        result = ValidationResult(
            ok=False,
            status=403,
            curl="curl command",
            error={"message": "Forbidden"},
        )
        assert result.ok is False
        assert result.status == 403
        assert result.error == {"message": "Forbidden"}
        assert result.data == {}

    def test_to_dict_success(self) -> None:
        """Test to_dict method with successful result."""
        result = ValidationResult(
            ok=True,
            status=200,
            curl="curl command",
            data={"valid": True},
        )
        result_dict = result.to_dict()
        assert result_dict["ok"] is True
        assert result_dict["status"] == 200
        assert result_dict["curl"] == "curl command"
        assert result_dict["data"] == {"valid": True}
        assert "error" not in result_dict

    def test_to_dict_error(self) -> None:
        """Test to_dict method with error result."""
        result = ValidationResult(
            ok=False,
            status=403,
            curl="curl command",
            error={"message": "Forbidden"},
        )
        result_dict = result.to_dict()
        assert result_dict["ok"] is False
        assert result_dict["status"] == 403
        assert result_dict["error"] == {"message": "Forbidden"}
        assert "data" not in result_dict


class TestLoadEnvFile:
    """Tests for load_env_file function."""

    def test_load_env_file_success(self, temp_env_file: str, clean_env: None) -> None:
        """Test loading environment variables from file."""
        load_env_file(temp_env_file)
        assert os.environ["DD_API_KEY"] == "test_api_key_12345678"
        assert os.environ["DD_APP_KEY"] == "test_app_key_87654321"
        assert os.environ["DD_SITE"] == "datadoghq.com"
        assert os.environ["DD_API_KEY_NAME"] == "Test API Key"

    def test_load_env_file_nonexistent(self, clean_env: None) -> None:
        """Test loading from nonexistent file does nothing."""
        load_env_file("nonexistent.env")
        assert "DD_API_KEY" not in os.environ

    def test_load_env_file_does_not_override(self, temp_env_file: str, clean_env: None) -> None:
        """Test that existing environment variables are not overridden."""
        os.environ["DD_API_KEY"] = "existing_key"
        load_env_file(temp_env_file)
        assert os.environ["DD_API_KEY"] == "existing_key"


class TestRedactSecret:
    """Tests for redact_secret function."""

    def test_redact_long_secret(self) -> None:
        """Test redacting a long secret."""
        secret = "1234567890abcdef"
        redacted = redact_secret(secret)
        assert redacted == "1234...cdef"

    def test_redact_short_secret(self) -> None:
        """Test redacting a short secret."""
        secret = "12345"
        redacted = redact_secret(secret)
        assert redacted == "*****"

    def test_redact_none(self) -> None:
        """Test redacting None."""
        assert redact_secret(None) is None

    def test_redact_empty_string(self) -> None:
        """Test redacting empty string."""
        assert redact_secret("") == ""

    def test_redact_exact_8_chars(self) -> None:
        """Test redacting exactly 8 characters."""
        secret = "12345678"
        redacted = redact_secret(secret)
        assert redacted == "********"


class TestBuildCurlCommand:
    """Tests for build_curl_command function."""

    def test_build_curl_command_with_api_key(self) -> None:
        """Test building curl command with API key."""
        url = "https://api.datadoghq.com/api/v1/validate"
        headers = {
            "Accept": "application/json",
            "DD-API-KEY": "1234567890abcdef",
        }
        curl = build_curl_command(url, headers)
        assert "curl -sS -X GET" in curl
        assert url in curl
        assert "DD-API-KEY: 1234...cdef" in curl
        assert "1234567890abcdef" not in curl

    def test_build_curl_command_without_secrets(self) -> None:
        """Test building curl command without secrets."""
        url = "https://api.datadoghq.com/api/v1/validate"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        curl = build_curl_command(url, headers)
        assert "Accept: application/json" in curl
        assert "Content-Type: application/json" in curl


class TestRequestJson:
    """Tests for request_json function."""

    @patch("datadog_integration.core.urlopen")
    def test_request_json_success(self, mock_urlopen: MagicMock) -> None:
        """Test successful JSON request."""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"valid": true}'
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_response

        status, data = request_json(
            "https://api.datadoghq.com/api/v1/validate",
            {"DD-API-KEY": "test_key"},
        )
        assert status == 200
        assert data == {"valid": True}


class TestSafeRequestJson:
    """Tests for safe_request_json function."""

    @patch("datadog_integration.core.request_json")
    def test_safe_request_json_success(self, mock_request: MagicMock) -> None:
        """Test safe request with success."""
        mock_request.return_value = (200, {"valid": True})
        result = safe_request_json(
            "https://api.datadoghq.com/api/v1/validate",
            {"DD-API-KEY": "test_key"},
        )
        assert result.ok is True
        assert result.status == 200
        assert result.data == {"valid": True}

    @patch("datadog_integration.core.request_json")
    def test_safe_request_json_http_error(self, mock_request: MagicMock) -> None:
        """Test safe request with HTTP error."""
        mock_error = HTTPError(
            "https://api.datadoghq.com/api/v1/validate",
            403,
            "Forbidden",
            {},
            None,
        )
        mock_error.read = MagicMock(return_value=b'{"errors": ["Forbidden"]}')
        mock_request.side_effect = mock_error

        result = safe_request_json(
            "https://api.datadoghq.com/api/v1/validate",
            {"DD-API-KEY": "test_key"},
        )
        assert result.ok is False
        assert result.status == 403
        assert "errors" in result.error

    @patch("datadog_integration.core.request_json")
    def test_safe_request_json_url_error(self, mock_request: MagicMock) -> None:
        """Test safe request with URL error."""
        mock_request.side_effect = URLError("Connection failed")
        result = safe_request_json(
            "https://api.datadoghq.com/api/v1/validate",
            {"DD-API-KEY": "test_key"},
        )
        assert result.ok is False
        assert result.status is None
        assert "message" in result.error


class TestDatadogValidator:
    """Tests for DatadogValidator class."""

    def test_init_with_all_params(self) -> None:
        """Test initialization with all parameters."""
        validator = DatadogValidator(
            api_key="api_key",
            app_key="app_key",
            site="datadoghq.eu",
            api_key_name="My API Key",
            app_key_name="My App Key",
            app_key_id="key_id",
        )
        assert validator.api_key == "api_key"
        assert validator.app_key == "app_key"
        assert validator.site == "datadoghq.eu"
        assert validator.api_key_name == "My API Key"
        assert validator.app_key_name == "My App Key"
        assert validator.app_key_id == "key_id"

    def test_init_with_defaults(self) -> None:
        """Test initialization with default values."""
        validator = DatadogValidator()
        assert validator.api_key is None
        assert validator.app_key is None
        assert validator.site == "datadoghq.com"
        assert validator.api_key_name is None
        assert validator.app_key_name is None
        assert validator.app_key_id is None

    def test_get_config_summary(self) -> None:
        """Test get_config_summary method."""
        validator = DatadogValidator(
            api_key="api_key",
            app_key="app_key",
            site="datadoghq.com",
            api_key_name="My API Key",
            app_key_name="My App Key",
            app_key_id="key_id",
        )
        summary = validator.get_config_summary()
        assert summary["site"] == "datadoghq.com"
        assert summary["api_key_present"] is True
        assert summary["app_key_present"] is True
        assert summary["api_key_name"] == "My API Key"
        assert summary["app_key_name"] == "My App Key"
        assert summary["app_key_id"] == "key_id"

    def test_get_config_summary_no_keys(self) -> None:
        """Test get_config_summary with no keys."""
        validator = DatadogValidator()
        summary = validator.get_config_summary()
        assert summary["api_key_present"] is False
        assert summary["app_key_present"] is False

    def test_validate_api_key_no_key(self) -> None:
        """Test validate_api_key with no API key."""
        validator = DatadogValidator()
        result = validator.validate_api_key()
        assert result is None

    @patch("datadog_integration.core.safe_request_json")
    def test_validate_api_key_success(self, mock_request: MagicMock) -> None:
        """Test validate_api_key with success."""
        mock_request.return_value = ValidationResult(
            ok=True,
            status=200,
            curl="curl command",
            data={"valid": True},
        )
        validator = DatadogValidator(api_key="test_key")
        result = validator.validate_api_key()
        assert result is not None
        assert result.ok is True
        assert result.status == 200

    def test_test_dashboards_read_no_keys(self) -> None:
        """Test test_dashboards_read with no keys."""
        validator = DatadogValidator()
        result = validator.test_dashboards_read()
        assert result is None

    def test_test_dashboards_read_no_app_key(self) -> None:
        """Test test_dashboards_read with no app key."""
        validator = DatadogValidator(api_key="test_key")
        result = validator.test_dashboards_read()
        assert result is None

    @patch("datadog_integration.core.safe_request_json")
    def test_test_dashboards_read_success(self, mock_request: MagicMock) -> None:
        """Test test_dashboards_read with success."""
        mock_request.return_value = ValidationResult(
            ok=True,
            status=200,
            curl="curl command",
            data={"dashboards": []},
        )
        validator = DatadogValidator(api_key="api_key", app_key="app_key")
        result = validator.test_dashboards_read()
        assert result is not None
        assert result.ok is True

    def test_test_metrics_read_no_keys(self) -> None:
        """Test test_metrics_read with no keys."""
        validator = DatadogValidator()
        result = validator.test_metrics_read()
        assert result is None

    @patch("datadog_integration.core.safe_request_json")
    def test_test_metrics_read_success(self, mock_request: MagicMock) -> None:
        """Test test_metrics_read with success."""
        mock_request.return_value = ValidationResult(
            ok=True,
            status=200,
            curl="curl command",
            data={"metrics": []},
        )
        validator = DatadogValidator(api_key="api_key", app_key="app_key")
        result = validator.test_metrics_read()
        assert result is not None
        assert result.ok is True

    def test_get_missing_api_key_error(self) -> None:
        """Test get_missing_api_key_error method."""
        validator = DatadogValidator(app_key="app_key", site="datadoghq.com")
        error = validator.get_missing_api_key_error()
        assert error["ok"] is False
        assert error["status"] is None
        assert "error" in error
        assert "message" in error["error"]
        assert "DD_API_KEY" in error["error"]["message"]

    def test_get_missing_api_key_error_with_key_id(self) -> None:
        """Test get_missing_api_key_error with key ID."""
        validator = DatadogValidator(
            app_key="app_key",
            app_key_id="key_123",
            site="datadoghq.com",
        )
        error = validator.get_missing_api_key_error()
        assert "blocked_endpoints" in error["error"]
        assert any("key_123" in endpoint for endpoint in error["error"]["blocked_endpoints"])


# Made with Bob
