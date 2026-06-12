"""Core functionality for Datadog API validation."""

import json
import os
from typing import Any, Dict, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class ValidationResult:
    """Result of a validation operation."""

    def __init__(
        self,
        ok: bool,
        status: Optional[int] = None,
        curl: str = "",
        data: Optional[Dict[str, Any]] = None,
        error: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize validation result.

        Args:
            ok: Whether the validation succeeded
            status: HTTP status code
            curl: Redacted curl command for debugging
            data: Response data if successful
            error: Error information if failed
        """
        self.ok = ok
        self.status = status
        self.curl = curl
        self.data = data or {}
        self.error = error or {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        result: Dict[str, Any] = {"ok": self.ok, "status": self.status, "curl": self.curl}
        if self.data:
            result["data"] = self.data
        if self.error:
            result["error"] = self.error
        return result


def load_env_file(path: str = ".env") -> None:
    """Load environment variables from a .env file.

    Args:
        path: Path to the .env file
    """
    if not os.path.exists(path):
        return

    with open(path, "r", encoding="utf-8") as env_file:
        for raw_line in env_file:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")

            if key and key not in os.environ:
                os.environ[key] = value


def redact_secret(value: Optional[str]) -> Optional[str]:
    """Redact a secret value for safe display.

    Args:
        value: The secret value to redact

    Returns:
        Redacted version showing only first and last 4 characters
    """
    if not value:
        return value
    if len(value) <= 8:
        return "*" * len(value)
    return f"{value[:4]}...{value[-4:]}"


def build_curl_command(url: str, headers: Dict[str, str]) -> str:
    """Build a curl command with redacted secrets.

    Args:
        url: The URL to request
        headers: HTTP headers to include

    Returns:
        A formatted curl command string
    """
    parts = ["curl -sS -X GET", f'"{url}"']
    for key, value in headers.items():
        redacted_value = redact_secret(value) if "KEY" in key else value
        parts.append(f'-H "{key}: {redacted_value}"')
    return " \\\n  ".join(parts)


def request_json(url: str, headers: Dict[str, str], timeout: int = 20) -> Tuple[int, Any]:
    """Make an HTTP request and parse JSON response.

    Args:
        url: The URL to request
        headers: HTTP headers to include
        timeout: Request timeout in seconds

    Returns:
        Tuple of (status_code, parsed_json_data)
    """
    request = Request(url, headers=headers)
    with urlopen(request, timeout=timeout) as response:
        body = response.read().decode("utf-8")
        return response.status, json.loads(body)


def safe_request_json(url: str, headers: Dict[str, str]) -> ValidationResult:
    """Make a safe HTTP request with error handling.

    Args:
        url: The URL to request
        headers: HTTP headers to include

    Returns:
        ValidationResult with success or error information
    """
    curl_command = build_curl_command(url, headers)
    try:
        status, data = request_json(url, headers)
        return ValidationResult(ok=True, status=status, curl=curl_command, data=data)
    except HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            parsed = {"raw": body}
        return ValidationResult(ok=False, status=error.code, curl=curl_command, error=parsed)
    except URLError as error:
        return ValidationResult(
            ok=False,
            status=None,
            curl=curl_command,
            error={"message": str(error)},
        )


class DatadogValidator:
    """Validator for Datadog API and Application keys."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        app_key: Optional[str] = None,
        site: str = "datadoghq.com",
        api_key_name: Optional[str] = None,
        app_key_name: Optional[str] = None,
        app_key_id: Optional[str] = None,
    ) -> None:
        """Initialize Datadog validator.

        Args:
            api_key: Datadog API key
            app_key: Datadog Application key
            site: Datadog site (default: datadoghq.com)
            api_key_name: Name/description of the API key
            app_key_name: Name/description of the Application key
            app_key_id: Application key identifier
        """
        self.api_key = api_key
        self.app_key = app_key
        self.site = site
        self.api_key_name = api_key_name
        self.app_key_name = app_key_name
        self.app_key_id = app_key_id

    def get_config_summary(self) -> Dict[str, Any]:
        """Get a summary of configured credentials.

        Returns:
            Dictionary with credential configuration status
        """
        return {
            "site": self.site,
            "api_key_name": self.api_key_name,
            "api_key_present": bool(self.api_key),
            "app_key_name": self.app_key_name,
            "app_key_present": bool(self.app_key),
            "app_key_id": self.app_key_id,
        }

    def validate_api_key(self) -> Optional[ValidationResult]:
        """Validate the API key.

        Returns:
            ValidationResult if API key is present, None otherwise
        """
        if not self.api_key:
            return None

        headers = {
            "Accept": "application/json",
            "DD-API-KEY": self.api_key,
        }

        return safe_request_json(f"https://api.{self.site}/api/v1/validate", headers)

    def test_dashboards_read(self) -> Optional[ValidationResult]:
        """Test dashboard read permissions.

        Returns:
            ValidationResult if both keys are present, None otherwise
        """
        if not self.api_key or not self.app_key:
            return None

        headers = {
            "Accept": "application/json",
            "DD-API-KEY": self.api_key,
            "DD-APPLICATION-KEY": self.app_key,
        }

        return safe_request_json(f"https://api.{self.site}/api/v1/dashboard", headers)

    def test_metrics_read(self) -> Optional[ValidationResult]:
        """Test metrics read permissions.

        Returns:
            ValidationResult if both keys are present, None otherwise
        """
        if not self.api_key or not self.app_key:
            return None

        headers = {
            "Accept": "application/json",
            "DD-API-KEY": self.api_key,
            "DD-APPLICATION-KEY": self.app_key,
        }

        return safe_request_json(f"https://api.{self.site}/api/v1/metrics", headers)

    def get_missing_api_key_error(self) -> Dict[str, Any]:
        """Get error message for missing API key when app key is present.

        Returns:
            Error dictionary explaining the configuration issue
        """
        return {
            "ok": False,
            "status": None,
            "error": {
                "message": (
                    "Datadog application-key permission lookup requires both DD_API_KEY and DD_APP_KEY. "
                    "With only an application key, the Datadog API cannot authenticate these metadata requests."
                ),
                "type": "local_configuration_error",
                "missing_env": ["DD_API_KEY"],
                "blocked_endpoints": [
                    f"https://api.{self.site}/api/v2/current_user",
                    (
                        f"https://api.{self.site}/api/v2/application_keys/{self.app_key_id}"
                        if self.app_key_id
                        else f"https://api.{self.site}/api/v2/current_user/application_keys"
                    ),
                ],
            },
        }

# Made with Bob
