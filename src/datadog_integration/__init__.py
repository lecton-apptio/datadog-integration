"""Datadog Integration Library.

A production-grade Python library for validating Datadog API and Application keys.
"""

from datadog_integration.core import (
    DatadogValidator,
    ValidationResult,
    build_curl_command,
    load_env_file,
    redact_secret,
)

__version__ = "0.1.0"
__all__ = [
    "DatadogValidator",
    "ValidationResult",
    "build_curl_command",
    "load_env_file",
    "redact_secret",
]

# Made with Bob
