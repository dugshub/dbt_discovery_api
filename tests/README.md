# DBT Discovery API Testing

This directory contains tests for the DBT Discovery API client.

## Unit Tests

Run the unit tests with:

```bash
pytest -xvs tests/
```

Unit tests use mocks and don't require any real API credentials. Note that since unit tests use mock objects, they typically don't generate much log output.

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

## Logging Configuration

The DBT Discovery API client uses Python's logging module with configurable log levels. By default, logging is set to WARNING level for regular operations.

### Controlling Log Output

You can control the log level using the `DBT_DISCOVERY_LOG_LEVEL` environment variable:

```bash
# Set log level to DEBUG for detailed output
export DBT_DISCOVERY_LOG_LEVEL=DEBUG

# Set log level to INFO for less verbose output
export DBT_DISCOVERY_LOG_LEVEL=INFO

# Set log level to WARNING (default)
export DBT_DISCOVERY_LOG_LEVEL=WARNING
```

### Test Logging

For tests, you have several options:

```bash
# Run tests with default logging (WARNING level)
make test

# Run tests with DEBUG level logging
make test-debug

# Run integration tests (shows logs from real API calls)
make test-integration

# Run integration tests with detailed performance logging
make test-performance
```

Note that:
- Regular unit tests (`make test`) may not show many logs because they use mock objects
- Integration tests will show more logs because they use real objects making API calls
- The `test-debug` target sets both the application logging and pytest's log capture to DEBUG level

## Continuous Integration

For CI environments, you may want to:
- Always run unit tests
- Only run integration tests in specific environments where credentials are available
- Use environment-specific credentials for integration tests