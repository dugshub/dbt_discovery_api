# dbt Discovery API

A Python service layer and user-friendly API for interacting with the dbt Cloud Metadata API. This library provides a clean, typed interface for retrieving and analyzing metadata from dbt Cloud environments.

## Features

- **User-Friendly API Layer**: Simple, intuitive access to dbt Cloud resources
- **Service Layer**: Low-level access to GraphQL API with type safety
- **Environment Exploration**: Query environment details and retrieve all models in an environment
- **Model Analysis**: Examine model metadata, historical runs, and properties
- **Performance Metrics**: Retrieve and analyze model runtime statistics across a project
- **Data Validation**: Type-safe responses using Pydantic models
- **Caching**: Efficient caching to minimize API calls
- **Computed Properties**: Easy access to derived data that spans multiple service calls
- **Lazy Loading**: Properties are loaded on-demand for better performance
- **Optimized Batch Queries**: Uses GraphQL aliasing to fetch multiple models in a single query

```

## Authentication

Set your dbt Cloud API token as an environment variable:

```bash
export DBT_SERVICE_TOKEN="your_dbt_cloud_token"
```

Alternatively, you can pass the token directly when initializing the API.

## Usage Examples

### Using the API Layer (Recommended)

```python
from src.api import DiscoveryAPI

# Initialize the API
api = DiscoveryAPI(token="your_dbt_cloud_token")

# Get project
project = api.project(environment_id=123456)

# Get project metadata
metadata = project.get_metadata()
print(f"Project name: {metadata.dbt_project_name}")
print(f"Adapter type: {metadata.adapter_type}")

# Get all models
models = project.get_models()
print(f"Found {len(models)} models")

# Get specific model
model = project.get_model("my_model")

# Access model properties
print(f"Model: {model.metadata.name}")
print(f"Database: {model.metadata.database}")
print(f"Schema: {model.metadata.schema}")
print(f"Tags: {', '.join(model.metadata.tags)}")
print(f"Last run status: {model.last_run.status if model.last_run else 'No runs'}")

# Get historical runs
runs = model.get_historical_runs(limit=10)
for run in runs:
    print(f"Run status: {run.status}, Time: {run.run_time}")

# Convert model to dictionary
model_dict = model.to_dict()

# Get models with runtime metrics
models_with_runtime = project.get_models_with_runtime(last_n_runs=5)
for model in models_with_runtime:
    print(f"Model: {model.name}")
    print(f"  Average runtime: {model.average_runtime or 'N/A'} seconds")
    
    if model.most_recent_run:
        print(f"  Last run status: {model.most_recent_run['status']}")
        print(f"  Last run time: {model.most_recent_run['execution_time']} seconds")
    
    print(f"  Historical runs: {len(model.runtime_metrics.historical_runs)}")

# Get historical runtimes for the slowest models (optimized batch query)
slowest_models = project.get_historical_models_runtimes(slowest=True, limit=5)
for model_metrics in slowest_models:
    print(f"Model runtime: {model_metrics.execution_info.get('execution_time')} seconds")
    if model_metrics.most_recent_run:
        print(f"Last run status: {model_metrics.most_recent_run.status}")

# Get historical runtimes for specific models (optimized batch query)
model_names = ["model_1", "model_2", "model_3"]
model_metrics = project.get_historical_models_runtimes(models=model_names)
```

### Using the Service Layer (Advanced)

```python
from src.services.BaseQuery import BaseQuery
from src.services.EnvironmentService import EnvironmentService
from src.services.ModelService import ModelService

# Create base query with your token
base_query = BaseQuery(token="your_dbt_cloud_token")

# Create services
env_service = EnvironmentService(base_query)
model_service = ModelService(base_query)

# Get environment metadata
env_metadata = env_service.get_environment_metadata(environment_id=123456)
print(f"Project name: {env_metadata['dbt_project_name']}")

# Get models
models = model_service.get_models_applied(environment_id=123456)
print(f"Found {len(models)} models")

# Get specific model
model = model_service.get_model_by_name(
    environment_id=123456,
    model_name="my_model",
    state="applied"
)
print(f"Model: {model.name}")

# Get model historical runs
runs = model_service.get_model_historical_runs(
    environment_id=123456,
    model_name="my_model",
    last_run_count=5
)
for run in runs:
    print(f"Status: {run.status}, Time: {run.run_generated_at}")
```

## Architecture

The library is organized into two main layers:

### API Layer (High-Level)
- **DiscoveryAPI**: Main entry point for the API layer
- **Project**: Represents a dbt project with access to resources
- **Model**: Represents a dbt model with properties
- **Pydantic Models**: API-specific models with conversion from service layer models

### Service Layer (Low-Level)
- **BaseQuery**: Foundation class for GraphQL interactions with the dbt Cloud API
- **EnvironmentService**: Service for environment-level operations
- **ModelService**: Service for model-specific operations
- **Pydantic Models**: Type-safe data structures for API responses

## Technical Details

- **GraphQL**: Uses the `sgqlc` library to interact with dbt Cloud's GraphQL API
- **Type Safety**: Pydantic v2 models ensure type safety and data validation
- **ORM Mode**: Uses Pydantic's `from_attributes` feature for model conversion
- **Caching**: Implements caching strategies to minimize service calls
- **Lazy Loading**: Properties that require service calls are loaded on-demand
- **Batch Querying**: Utilizes GraphQL aliasing to fetch multiple models' historical runs in a single API call

## Development

When extending this library:

1. For new features, start by extending the service layer
2. Create corresponding API layer classes to provide a user-friendly interface
3. Enable ORM mode in service models for easy conversion to API models
4. Add computed properties for data that spans multiple service models
5. Implement proper caching to minimize service calls
6. Add comprehensive tests for both layers

### Running Tests

```bash
# Run unit tests
pytest tests/test_api_models.py tests/test_api_classes.py

# Run integration tests (requires API token)
pytest tests/test_api_integration.py --run-integration
```

## API Limitations

Be aware of the following limitations when using the dbt Cloud API:

1. Rate limits may apply to API requests
2. Some operations may be computationally expensive for large dbt projects
3. API responses may be paginated for large result sets

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
