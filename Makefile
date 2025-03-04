.PHONY: install lint typecheck test test-integration clean

install:
	uv pip install -e .

lint:
	ruff check .

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
	@echo "  make typecheck        - Run type checking with mypy"
	@echo "  make test             - Run tests with pytest"
	@echo "  make test-integration - Run integration tests only"
	@echo "  make clean            - Remove cache and build artifacts"
	@echo "  make all              - Run install, lint, typecheck, and test"