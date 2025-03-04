# DBT Discovery API Testing

This directory contains tests for the DBT Discovery API client.

## Unit Tests

Run the unit tests with:

```bash
pytest -xvs tests/
```

Unit tests use mocks and don't require any real API credentials.

## Integration Tests

Integration tests interact with the real dbt Cloud API and require:

1. A valid dbt Cloud service token
2. Environment ID(s) to test against

### Setup Environment Variables

Set up your environment variables before running the tests:

```bash
export DBT_SERVICE_TOKEN="your_dbt_service_token"
export ENV_ID_MART_PRODUCTION="123456"  # Replace with your actual environment ID
```

### Running Integration Tests

Run integration tests with the `--run-integration` flag:

```bash
# Run all tests including integration tests
pytest -xvs tests/ --run-integration

# Run only integration tests
pytest -xvs tests/ -m integration --run-integration

# Run integration tests for a specific service
pytest -xvs tests/query_layer/test_environment_service_integration.py --run-integration
```

### Test Filters

The integration tests will be skipped by default unless:
- The `--run-integration` flag is provided
- The required environment variables are set

## Continuous Integration

For CI environments, you may want to:
- Always run unit tests
- Only run integration tests in specific environments where credentials are available
- Use environment-specific credentials for integration tests