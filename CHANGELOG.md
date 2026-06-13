# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-06-12

### Added
- Initial release of datadog-integration
- API key validation functionality
- Application key permission testing
- Dashboard read access verification
- Metrics read access verification
- Command-line interface (CLI) tool `datadog-key-check`
- Full type annotations with MyPy support
- Comprehensive test suite with 99% code coverage
- Modern Python packaging (PEP 621)
- CI/CD pipeline for Ubuntu, macOS, and Windows
- Support for Python 3.9, 3.10, 3.11, and 3.12
- Environment variable loading from `.env` files
- Redacted curl commands for debugging
- Configuration summary functionality

### Features
- **ValidationResult** class for structured validation responses
- **DatadogValidator** class for credential validation
- Utility functions for secret redaction and curl command building
- Safe HTTP request handling with comprehensive error reporting
- Support for multiple Datadog sites (datadoghq.com, datadoghq.eu, etc.)

### Documentation
- Comprehensive README with usage examples
- API reference documentation
- Contributing guidelines
- MIT License
- Production readiness assessment

### Development
- Black code formatting
- Ruff linting
- MyPy type checking
- Pytest testing framework
- Code coverage reporting
- Makefile with convenient commands including `make all-checks`

[0.1.0]: https://github.com/lecton-apptio/datadog-integration/releases/tag/v0.1.0