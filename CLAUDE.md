# DBT Discovery API - Developer Guide

## Build & Test Commands
```bash
# Install dependencies
uv pip install -e .

# Run linting (flake8 or ruff recommended)
ruff check .

# Run type checking
mypy .

# Run tests (if implemented)
pytest -xvs tests/
```

## Code Style Guidelines
- **Python Version**: 3.12+
- **Types**: Always use type annotations for function parameters and return values
- **Imports**: Group imports by stdlib, third-party, local
- **Naming**:
  - Classes: PascalCase (BaseQuery, ModelService)
  - Methods/functions: snake_case (create_operation)
  - Variables: snake_case (environment_id)
  - Constants: UPPER_SNAKE_CASE
- **Documentation**: Docstrings for all classes and public methods
- **Error Handling**: Use explicit exception handling with specific exception types
- **Class Structure**: Follow existing patterns with base classes and services
- **Libraries**: Leverage pydantic for models and sgqlc for GraphQL

This codebase provides a typed interface to the dbt Cloud GraphQL API.