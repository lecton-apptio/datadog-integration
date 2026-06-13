"""Tests for CLI functionality."""

import os
from unittest.mock import MagicMock, patch

from datadog_integration.cli import get_optional_env, main, print_section
from datadog_integration.core import ValidationResult


class TestGetOptionalEnv:
    """Tests for get_optional_env function."""

    def test_get_first_available(self, clean_env: None) -> None:
        """Test getting first available environment variable."""
        os.environ["VAR2"] = "value2"
        os.environ["VAR3"] = "value3"
        result = get_optional_env("VAR1", "VAR2", "VAR3")
        assert result == "value2"

    def test_get_none_when_not_found(self, clean_env: None) -> None:
        """Test returning None when no variables found."""
        result = get_optional_env("NONEXISTENT_VAR1", "NONEXISTENT_VAR2", "NONEXISTENT_VAR3")
        assert result is None

    def test_get_empty_string_returns_none(self, clean_env: None) -> None:
        """Test that empty string is treated as not found."""
        os.environ["VAR1"] = ""
        os.environ["VAR2"] = "value2"
        result = get_optional_env("VAR1", "VAR2")
        assert result == "value2"


class TestPrintSection:
    """Tests for print_section function."""

    @patch("builtins.print")
    def test_print_section(self, mock_print: MagicMock) -> None:
        """Test printing section header."""
        print_section("Test Section")
        mock_print.assert_called_once_with("\n=== Test Section ===")


class TestMain:
    """Tests for main CLI function."""

    @patch("datadog_integration.cli.load_env_file")
    @patch("datadog_integration.cli.DatadogValidator")
    @patch("builtins.print")
    def test_main_with_api_key_only(
        self,
        mock_print: MagicMock,
        mock_validator_class: MagicMock,
        mock_load_env: MagicMock,
        clean_env: None,
    ) -> None:
        """Test main with only API key."""
        os.environ["DD_API_KEY"] = "test_api_key"
        os.environ["DD_SITE"] = "datadoghq.com"

        mock_validator = MagicMock()
        mock_validator.get_config_summary.return_value = {
            "api_key_present": True,
            "app_key_present": False,
        }
        mock_validator.validate_api_key.return_value = ValidationResult(
            ok=True,
            status=200,
            curl="curl command",
            data={"valid": True},
        )
        mock_validator_class.return_value = mock_validator

        main()

        mock_load_env.assert_called_once()
        mock_validator.validate_api_key.assert_called_once()

    @patch("datadog_integration.cli.load_env_file")
    @patch("datadog_integration.cli.DatadogValidator")
    @patch("builtins.print")
    def test_main_with_both_keys(
        self,
        mock_print: MagicMock,
        mock_validator_class: MagicMock,
        mock_load_env: MagicMock,
        clean_env: None,
    ) -> None:
        """Test main with both API and App keys."""
        os.environ["DD_API_KEY"] = "test_api_key"
        os.environ["DD_APP_KEY"] = "test_app_key"
        os.environ["DD_SITE"] = "datadoghq.com"

        mock_validator = MagicMock()
        mock_validator.get_config_summary.return_value = {
            "api_key_present": True,
            "app_key_present": True,
        }
        mock_validator.validate_api_key.return_value = ValidationResult(
            ok=True,
            status=200,
            curl="curl command",
            data={"valid": True},
        )
        mock_validator.test_dashboards_read.return_value = ValidationResult(
            ok=True,
            status=200,
            curl="curl command",
            data={"dashboards": []},
        )
        mock_validator.test_metrics_read.return_value = ValidationResult(
            ok=True,
            status=200,
            curl="curl command",
            data={"metrics": []},
        )
        mock_validator_class.return_value = mock_validator

        main()

        mock_validator.validate_api_key.assert_called_once()
        mock_validator.test_dashboards_read.assert_called_once()
        mock_validator.test_metrics_read.assert_called_once()

    @patch("datadog_integration.cli.load_env_file")
    @patch("datadog_integration.cli.DatadogValidator")
    @patch("builtins.print")
    def test_main_with_no_keys(
        self,
        mock_print: MagicMock,
        mock_validator_class: MagicMock,
        mock_load_env: MagicMock,
        clean_env: None,
    ) -> None:
        """Test main with no keys."""
        os.environ["DD_SITE"] = "datadoghq.com"

        mock_validator = MagicMock()
        mock_validator.get_config_summary.return_value = {
            "api_key_present": False,
            "app_key_present": False,
        }
        mock_validator_class.return_value = mock_validator

        main()

        mock_load_env.assert_called_once()
        mock_validator.validate_api_key.assert_not_called()

    @patch("datadog_integration.cli.load_env_file")
    @patch("datadog_integration.cli.DatadogValidator")
    @patch("builtins.print")
    def test_main_with_app_key_no_api_key(
        self,
        mock_print: MagicMock,
        mock_validator_class: MagicMock,
        mock_load_env: MagicMock,
        clean_env: None,
    ) -> None:
        """Test main with app key but no API key."""
        os.environ["DD_APP_KEY"] = "test_app_key"
        os.environ["DD_SITE"] = "datadoghq.com"

        mock_validator = MagicMock()
        mock_validator.get_config_summary.return_value = {
            "api_key_present": False,
            "app_key_present": True,
        }
        mock_validator.get_missing_api_key_error.return_value = {
            "ok": False,
            "error": {"message": "Missing API key"},
        }
        mock_validator_class.return_value = mock_validator

        main()

        mock_validator.get_missing_api_key_error.assert_called_once()
        mock_validator.test_dashboards_read.assert_not_called()

    @patch("datadog_integration.cli.load_env_file")
    @patch("datadog_integration.cli.DatadogValidator")
    @patch("builtins.print")
    def test_main_with_alternative_env_vars(
        self,
        mock_print: MagicMock,
        mock_validator_class: MagicMock,
        mock_load_env: MagicMock,
        clean_env: None,
    ) -> None:
        """Test main with alternative environment variable names."""
        os.environ["DD_API_KEY"] = "test_api_key"
        os.environ["DD_APPLICATION_KEY"] = "test_app_key"
        os.environ["DD_APP_ID"] = "key_id"
        os.environ["DD_SITE"] = "datadoghq.eu"

        mock_validator = MagicMock()
        mock_validator.get_config_summary.return_value = {
            "api_key_present": True,
            "app_key_present": True,
        }
        mock_validator.validate_api_key.return_value = ValidationResult(
            ok=True,
            status=200,
            curl="curl command",
            data={"valid": True},
        )
        mock_validator.test_dashboards_read.return_value = ValidationResult(
            ok=True,
            status=200,
            curl="curl command",
            data={"dashboards": []},
        )
        mock_validator.test_metrics_read.return_value = ValidationResult(
            ok=True,
            status=200,
            curl="curl command",
            data={"metrics": []},
        )
        mock_validator_class.return_value = mock_validator

        main()

        # Verify validator was initialized with correct values
        call_kwargs = mock_validator_class.call_args[1]
        assert call_kwargs["api_key"] == "test_api_key"
        assert call_kwargs["app_key"] == "test_app_key"
        assert call_kwargs["app_key_id"] == "key_id"
        assert call_kwargs["site"] == "datadoghq.eu"


# Made with Bob
