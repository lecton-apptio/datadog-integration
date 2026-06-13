"""Pytest configuration and fixtures."""

import os
import tempfile
from collections.abc import Generator

import pytest


@pytest.fixture
def temp_env_file() -> Generator[str, None, None]:
    """Create a temporary .env file for testing.

    Yields:
        Path to the temporary .env file
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
        f.write("DD_API_KEY=test_api_key_12345678\n")
        f.write("DD_APP_KEY=test_app_key_87654321\n")
        f.write("DD_SITE=datadoghq.com\n")
        f.write("# Comment line\n")
        f.write("DD_API_KEY_NAME=Test API Key\n")
        temp_path = f.name

    yield temp_path

    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def clean_env() -> Generator[None, None, None]:
    """Clean environment variables before and after test.

    Yields:
        None
    """
    # Store original values
    original_env = {}
    dd_keys = [
        "DD_API_KEY",
        "DD_APP_KEY",
        "DD_APPLICATION_KEY",
        "DD_SITE",
        "DD_API_KEY_NAME",
        "DD_APP_KEY_NAME",
        "DD_KEY_ID",
        "DD_APP_ID",
    ]

    for key in dd_keys:
        if key in os.environ:
            original_env[key] = os.environ[key]
            del os.environ[key]

    yield

    # Restore original values
    for key in dd_keys:
        if key in os.environ:
            del os.environ[key]
    for key, value in original_env.items():
        os.environ[key] = value


@pytest.fixture
def mock_api_key() -> str:
    """Return a mock API key for testing.

    Returns:
        Mock API key string
    """
    return "test_api_key_1234567890abcdef"


@pytest.fixture
def mock_app_key() -> str:
    """Return a mock Application key for testing.

    Returns:
        Mock Application key string
    """
    return "test_app_key_fedcba0987654321"


# Made with Bob
