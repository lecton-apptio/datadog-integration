.PHONY: help install install-dev format lint type-check test test-cov clean build

help:
	@echo "Available targets:"
	@echo "  install      - Install package in production mode"
	@echo "  install-dev  - Install package with development dependencies"
	@echo "  format       - Format code with Black"
	@echo "  lint         - Lint code with Ruff"
	@echo "  type-check   - Type check with MyPy"
	@echo "  test         - Run tests with pytest"
	@echo "  test-cov     - Run tests with coverage report"
	@echo "  clean        - Remove build artifacts and cache files"
	@echo "  build        - Build distribution packages"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

format:
	black src tests

lint:
	ruff check src tests

type-check:
	mypy src

test:
	pytest

test-cov:
	pytest --cov=datadog_integration --cov-report=term-missing --cov-report=html

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

# Made with Bob
