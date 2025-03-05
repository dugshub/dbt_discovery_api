.PHONY: install lint typecheck test test-debug test-integration test-performance clean fix check-all super super-no-integration

install:
	uv pip install -e .

lint:
	ruff check .

fix:
	ruff check . --fix

check-all: lint typecheck

test-and-check: test check-all

test-and-check-integration: test-integration check-all

typecheck:
	mypy .

test:
	pytest -xvs tests/

test-debug:
	DBT_DISCOVERY_LOG_LEVEL=DEBUG pytest -xvs tests/ --log-cli-level=DEBUG

test-integration:
	pytest -xvs tests/  --run-integration

test-performance:
	@echo "Running integration tests with detailed performance logging..."
	pytest -xvs tests/ --run-integration --log-cli-level=DEBUG
	@echo "Performance logs saved to logs/performance.log"

clean:
	find . -name "__pycache__" -type d -exec rm -rf {} +;
	rm -rf dist build *.egg-info

all: install lint typecheck test

help:
	@echo "Available commands:"
	@echo "  make install          - Install dependencies with uv"
	@echo "  make lint             - Run linting with ruff"
	@echo "  make fix              - Run linting with ruff and fix issues"
	@echo "  make typecheck        - Run type checking with mypy"
	@echo "  make test             - Run tests with pytest"
	@echo "  make test-debug       - Run tests with DEBUG level logging"
	@echo "  make test-integration - Run integration tests only"
	@echo "  make test-performance - Run integration tests with detailed performance logging"
	@echo "  make clean            - Remove cache and build artifacts"
	@echo "  make all              - Run install, lint, typecheck, and test"
	@echo "  make check-all        - Run linting and type checking"
	@echo "  make super            - Run tests, checks, and linting"
	@echo "  make super-no-integration - Run tests, checks, and linting without integration tests"