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

# Run integration tests with performance logging
make test-performance
```

### Performance Testing

To diagnose integration test performance issues, use the `test-performance` make target:

```bash
make test-performance
```

This runs the integration tests with detailed performance logging enabled:

- All GraphQL operations are timed and logged
- Slow queries (>1 second) trigger warning messages with query details
- HTTP request timing is tracked separately from total execution time
- Performance logs are displayed in the console and saved to `logs/performance.log`

This helps identify which operations are slowest and may be causing performance bottlenecks in the test suite.

### Test Filters

The integration tests will be skipped by default unless:
- The `--run-integration` flag is provided
- The required environment variables are set

## Continuous Integration

For CI environments, you may want to:
- Always run unit tests
- Only run integration tests in specific environments where credentials are available
- Use environment-specific credentials for integration tests