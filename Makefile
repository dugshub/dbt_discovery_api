.PHONY: install lint typecheck test test-integration clean fix check-all super super-no-integration

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

test-integration:
	pytest -xvs tests/  --run-integration

clean:
	rm -rf .ruff_cache .mypy_cache .pytest_cache __pycache__ */__pycache__ */*/__pycache__
	rm -rf dist build *.egg-info

all: install lint typecheck test

help:
	@echo "Available commands:"
	@echo "  make install          - Install dependencies with uv"
	@echo "  make lint             - Run linting with ruff"
	@echo "  make fix              - Run linting with ruff and fix issues"
	@echo "  make typecheck        - Run type checking with mypy"
	@echo "  make test             - Run tests with pytest"
	@echo "  make test-integration - Run integration tests only"
	@echo "  make clean            - Remove cache and build artifacts"
	@echo "  make all              - Run install, lint, typecheck, and test"
	@echo "  make check-all        - Run linting and type checking"
	@echo "  make super            - Run tests, checks, and linting"
	@echo "  make super-no-integration - Run tests, checks, and linting without integration tests"