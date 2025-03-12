# DBT Discovery API Services

## Overview

The `services` package provides a collection of classes that interact with the dbt Cloud API. These services abstract the complexities of GraphQL queries and provide a clean interface for retrieving data from dbt Cloud.

## Logging Configuration

The dbt Discovery API has configurable logging through the `DBT_DISCOVERY_LOG_LEVEL` environment variable:

- **Default Level**: WARNING
- **Available Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL

**Usage:**
```bash
# Set logging level
export DBT_DISCOVERY_LOG_LEVEL=DEBUG

# Run tests with DEBUG logging
make test-debug

# Integration tests use real objects and show logs
make test-integration

# Regular tests use mock objects and may not show many logs
make test
```

## Service Classes

### BaseQuery

`BaseQuery` is the foundation for all service classes. It handles GraphQL operations, authentication, and execution.

**Key Features:**
- Authentication with dbt Cloud API
- GraphQL query execution with timing information
- Preconfigured queries for common operations
- Detailed logging of query performance

**Example:**
```python
from src.discovery_api.services.BaseQuery import BaseQuery

# Initialize with token (or will read from DBT_SERVICE_TOKEN env var)
base_query = BaseQuery(token="your_token")

# Create and execute a simple operation
op = base_query.create_operation()
environment = op.environment(id=123)
environment.name()
result = base_query.execute(op)
```

### EnvironmentService

`EnvironmentService` is responsible for retrieving environment data from dbt Cloud.

**Key Features:**
- Fetch environment metadata
- Get applied state information
- Get definition state information
- Automatic conversion of camelCase keys to snake_case

**Example:**
```python
from src.discovery_api.services.BaseQuery import BaseQuery
from src.discovery_api.services.EnvironmentService import EnvironmentService

base_query = BaseQuery()
env_service = EnvironmentService(base_query)

# Get environment metadata
env_metadata = env_service.get_environment_metadata(environment_id=123)

# Get applied state
applied_state = env_service.get_applied_state(environment_id=123)

# Get definition state
definition_state = env_service.get_definition_state(environment_id=123)
```

### JobService

[JobService](cci:2://file:///Users/doug/Documents/GitHub/dbt_discovery_api/src/discovery_api/services/JobService.py:6:0-372:77) provides methods for retrieving job data, including models and tests.

**Key Features:**
- Fetch job metadata
- Retrieve models and tests for a job
- Support for field selection through kwargs
- Get specific models or tests by unique ID

**Example:**
```python
from src.discovery_api.services.BaseQuery import BaseQuery
from src.discovery_api.services.JobService import JobService

base_query = BaseQuery()
job_service = JobService(base_query)

# Get job metadata
job_metadata = job_service.get_job_metadata(job_id=123)

# Get models for a job with selected fields
models = job_service.get_job_models(
    job_id=123,
    include_database=True,
    include_code=False
)

# Get tests for a job
tests = job_service.get_job_tests(job_id=123)

# Get combined job, models, and tests data
job_data = job_service.get_job_with_models_and_tests(job_id=123)
```

### ModelService

[ModelService](cci:2://file:///Users/doug/Documents/GitHub/dbt_discovery_api/src/discovery_api/services/ModelService.py:7:0-461:91) is designed for retrieving model data with support for historical runs.

**Key Features:**
- Fetch models from applied or definition state
- Get historical runs for specific models
- Support for batched queries with aliasing
- Transformations to Pydantic models for type safety

**Example:**
```python
from src.discovery_api.services.BaseQuery import BaseQuery
from src.discovery_api.services.ModelService import ModelService

base_query = BaseQuery()
model_service = ModelService(base_query)

# Get models from applied state
applied_models = model_service.get_models_applied(environment_id=123)

# Get models from definition state
definition_models = model_service.get_models_definition(environment_id=123)

# Get historical runs for a specific model
historical_runs = model_service.get_model_historical_runs(
    environment_id=123,
    model_name="example_model",
    last_run_count=10
)

# Get historical runs for multiple models in a single query
model_runs = model_service.get_multiple_models_historical_runs(
    environment_id=123,
    model_names=["model1", "model2", "model3"]
)

# Get a specific model by name
model = model_service.get_model_by_name(
    environment_id=123,
    model_name="example_model",
    state="applied"
)
```

## Best Practices

1. **Reuse BaseQuery Instances**: Create a single BaseQuery instance and pass it to all services to minimize authentication overhead.

2. **Selective Field Inclusion**: Use the field selection kwargs (e.g., `include_code=True`) to only retrieve the data you need and optimize query performance.

3. **Batched Queries**: Use methods like [get_multiple_models_historical_runs()](cci:1://file:///Users/doug/Documents/GitHub/dbt_discovery_api/src/discovery_api/services/ModelService.py:361:4-435:21) to reduce the number of API calls when retrieving similar data for multiple entities.

4. **Handle Response Data Carefully**: All methods return structured data with snake_case keys, which can be used directly or passed to Pydantic models.

5. **Configure Logging Appropriately**: Set the `DBT_DISCOVERY_LOG_LEVEL` environment variable based on your needs (DEBUG for development, WARNING for production).