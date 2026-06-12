# Contributing to datadog-integration

Thank you for your interest in contributing to datadog-integration! This document provides guidelines and instructions for contributing to this project.

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/lecton-apptio/datadog-integration.git
cd datadog-integration
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
make install-dev
```

## Development Workflow

### Code Style

This project uses several tools to maintain code quality:

- **Black**: Code formatting (line length: 100)
- **Ruff**: Fast Python linter
- **MyPy**: Static type checking

Format your code before committing:
```bash
make format
```

### Linting

Run the linter to check for code issues:
```bash
make lint
```

### Type Checking

Ensure type annotations are correct:
```bash
make type-check
```

### Testing

Run the test suite:
```bash
make test
```

Run tests with coverage:
```bash
make test-cov
```

### Pre-commit Checklist

Before submitting a pull request, ensure:

1. All tests pass: `make test`
2. Code is formatted: `make format`
3. No linting errors: `make lint`
4. Type checking passes: `make type-check`
5. Coverage is maintained or improved

## Pull Request Process

1. Fork the repository and create a new branch from `main`
2. Make your changes following the code style guidelines
3. Add or update tests as needed
4. Update documentation if you're changing functionality
5. Run the full test suite and ensure all checks pass
6. Submit a pull request with a clear description of your changes

### Pull Request Guidelines

- Use clear, descriptive commit messages
- Reference any related issues in your PR description
- Keep PRs focused on a single feature or fix
- Update the README.md if you're adding new features
- Ensure CI/CD checks pass before requesting review

## Code Review

All submissions require review before merging. Reviewers will check:

- Code quality and style compliance
- Test coverage
- Documentation completeness
- Adherence to project conventions

## Reporting Issues

When reporting issues, please include:

- A clear description of the problem
- Steps to reproduce the issue
- Expected vs actual behavior
- Python version and environment details
- Relevant error messages or logs

## Feature Requests

We welcome feature requests! Please:

- Check if the feature has already been requested
- Provide a clear use case for the feature
- Describe the expected behavior
- Consider submitting a PR if you can implement it

## Questions?

If you have questions about contributing, feel free to:

- Open an issue for discussion
- Reach out to the maintainers

Thank you for contributing to datadog-integration!