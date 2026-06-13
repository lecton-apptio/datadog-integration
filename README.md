# datadog-integration

[![CI](https://github.com/lecton-apptio/datadog-integration/actions/workflows/ci.yml/badge.svg)](https://github.com/lecton-apptio/datadog-integration/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

A production-grade Python library for validating Datadog API and Application keys with comprehensive permission testing.

## Features

- 🔑 **API Key Validation**: Verify Datadog API keys are valid and active
- 🔐 **Application Key Testing**: Test application key permissions and scopes
- 📊 **Permission Verification**: Validate read access to dashboards and metrics
- 🛡️ **Type-Safe**: Full type annotations with MyPy support
- 🧪 **Well-Tested**: Comprehensive test coverage
- 📝 **Production-Ready**: Follows modern Python packaging standards (PEP 621)
- 🔧 **CLI Tool**: Command-line interface for quick validation
- 🐍 **Python 3.9+**: Supports Python 3.9, 3.10, 3.11, and 3.12

## Installation

```bash
pip install datadog-integration
```

For development:

```bash
pip install -e ".[dev]"
```

## Quick Start

### Command Line Interface

The easiest way to validate your Datadog credentials:

```bash
# Set environment variables
export DD_API_KEY="your-api-key"
export DD_APP_KEY="your-app-key"
export DD_SITE="datadoghq.com"  # Optional, defaults to datadoghq.com

# Run validation
datadog-key-check
```

Or use a `.env` file:

```bash
# Create .env file with your credentials
cat > .env << EOF
DD_API_KEY=your-api-key
DD_APP_KEY=your-app-key
DD_SITE=datadoghq.com
EOF

# Run validation (automatically loads .env)
datadog-key-check
```

### Python Library

Use the library programmatically in your Python code:

```python
from datadog_integration import DatadogValidator

# Initialize validator
validator = DatadogValidator(
    api_key="your-api-key",
    app_key="your-app-key",
    site="datadoghq.com"
)

# Get configuration summary
config = validator.get_config_summary()
print(config)

# Validate API key
api_result = validator.validate_api_key()
if api_result and api_result.ok:
    print("API key is valid!")
else:
    print(f"API key validation failed: {api_result.error}")

# Test dashboard read permissions
dashboard_result = validator.test_dashboards_read()
if dashboard_result and dashboard_result.ok:
    print("Dashboard read access confirmed!")

# Test metrics read permissions
metrics_result = validator.test_metrics_read()
if metrics_result and metrics_result.ok:
    print("Metrics read access confirmed!")
```

### Environment Variables

The library supports the following environment variables:

- `DD_API_KEY`: Your Datadog API key (required for API validation)
- `DD_APP_KEY` or `DD_APPLICATION_KEY`: Your Datadog Application key
- `DD_SITE`: Datadog site (default: `datadoghq.com`)
- `DD_API_KEY_NAME`: Optional name/description for the API key
- `DD_APP_KEY_NAME`: Optional name/description for the Application key
- `DD_KEY_ID` or `DD_APP_ID`: Optional Application key identifier

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/lecton-apptio/datadog-integration.git
cd datadog-integration

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
make install-dev
```

### Available Make Commands

```bash
make help          # Show all available commands
make format        # Format code with Black
make lint          # Lint code with Ruff
make type-check    # Type check with MyPy
make test          # Run tests
make test-cov      # Run tests with coverage
make clean         # Remove build artifacts
make build         # Build distribution packages
```

### Running Tests

```bash
# Run all tests
make test

# Run with coverage report
make test-cov

# Run specific test file
pytest tests/test_core.py
```

### Code Quality

This project uses several tools to maintain code quality:

- **Black**: Code formatting (line length: 100)
- **Ruff**: Fast Python linter
- **MyPy**: Static type checking
- **Pytest**: Testing framework

All checks run automatically in CI/CD on Ubuntu, macOS, and Windows for Python 3.9-3.12.

## API Reference

### `DatadogValidator`

Main class for validating Datadog credentials.

**Constructor Parameters:**
- `api_key` (str, optional): Datadog API key
- `app_key` (str, optional): Datadog Application key
- `site` (str): Datadog site (default: "datadoghq.com")
- `api_key_name` (str, optional): Name/description of the API key
- `app_key_name` (str, optional): Name/description of the Application key
- `app_key_id` (str, optional): Application key identifier

**Methods:**
- `get_config_summary()`: Returns configuration status
- `validate_api_key()`: Validates the API key
- `test_dashboards_read()`: Tests dashboard read permissions
- `test_metrics_read()`: Tests metrics read permissions

### `ValidationResult`

Result object returned by validation methods.

**Attributes:**
- `ok` (bool): Whether the validation succeeded
- `status` (int | None): HTTP status code
- `curl` (str): Redacted curl command for debugging
- `data` (dict): Response data if successful
- `error` (dict): Error information if failed

**Methods:**
- `to_dict()`: Convert result to dictionary

### Utility Functions

- `load_env_file(path: str = ".env")`: Load environment variables from file
- `redact_secret(value: str)`: Redact sensitive values for safe display
- `build_curl_command(url: str, headers: dict)`: Build curl command with redacted secrets

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/lecton-apptio/datadog-integration/issues)
- **Documentation**: [README.md](README.md)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)

## Versioning

This project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html):

- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality in a backward compatible manner
- **PATCH** version for backward compatible bug fixes

Current version: **0.1.0**

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes.

### Latest Release: Version 0.1.0 (2026-06-12)

- Initial release with API key validation
- Application key permission testing
- Dashboard and metrics read verification
- CLI tool with environment variable support
- Full type annotations and comprehensive test coverage

For complete release history, see [CHANGELOG.md](CHANGELOG.md).