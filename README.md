# dbt Discovery API

A Python service layer for interacting with the dbt Cloud Metadata API. This library provides a clean, typed interface for retrieving and analyzing metadata from dbt Cloud environments.

## Features

- **Environment Exploration**: Query environment details and retrieve all models in an environment
- **Model Analysis**: Examine model dependencies, lineage, and SQL definitions
- **Data Validation**: Type-safe responses using Pydantic models
- **Flexible Filtering**: Filter models by materialization type, tags, and other properties
- **Dependency Tracking**: Analyze upstream and downstream dependencies for any model

## Installation

```bash
pip install dbt-discovery-api
```

## Authentication

Set your dbt Cloud API token as an environment variable:

```bash
export DBT_SERVICE_TOKEN="your_dbt_cloud_token"
```

Alternatively, you can pass the token directly to service constructors.

## Usage Examples

### Exploring an Environment

```python
from src.services.EnvironmentService import EnvironmentService

# Create environment service with your environment ID
env_service = EnvironmentService(environment_id=123)

# Get environment details
env_details = env_service.get_environment_details()
print(f"Environment: {env_details.name}")

# Get all models in the environment
models = env_service.get_models()
print(f"Found {len(models)} models")

# Filter models by materialization type
table_models = env_service.get_models(materialized_types=["table"])
print(f"Found {len(table_models)} table models")

# Filter models by tag
tagged_models = env_service.get_models(tags=["finance"])
print(f"Found {len(tagged_models)} finance models")
```

### Analyzing Model Lineage

```python
from src.services.ModelService import ModelService

# Create model service with model unique ID and environment ID
model_service = ModelService(
    unique_id="model.project.model_name",
    environment_id=123
)

# Get model details
model_details = model_service.get_model_details()
print(f"Model: {model_details.name}")

# Get upstream dependencies
upstream = model_service.get_upstream_models()
print(f"Model depends on {len(upstream)} upstream models")

# Get downstream dependencies
downstream = model_service.get_downstream_models()
print(f"Model is used by {len(downstream)} downstream models")

# Print dependency tree
for model in upstream:
    print(f"  - {model.unique_id}")
```

### Retrieving Model SQL

```python
from src.services.ModelService import ModelService

model_service = ModelService(
    unique_id="model.project.model_name",
    environment_id=123
)

# Get raw SQL
raw_sql = model_service.get_raw_sql()
print(f"Raw SQL length: {len(raw_sql)}")

# Get compiled SQL
compiled_sql = model_service.get_compiled_sql()
print(f"Compiled SQL length: {len(compiled_sql)}")
```

## Architecture

The library is organized into several key components:

- **BaseQuery**: Foundation class for GraphQL interactions with the dbt Cloud API
- **EnvironmentService**: Service for environment-level operations and model discovery
- **ModelService**: Service for model-specific operations and lineage analysis
- **Pydantic Models**: Type-safe data structures for API responses

## Technical Details

- **GraphQL**: Uses the `sgqlc` library to interact with dbt Cloud's GraphQL API
- **Authentication**: Bearer token authentication via HTTP headers
- **Data Validation**: Pydantic models ensure type safety and data validation
- **Error Handling**: Comprehensive error handling for API interactions

## Development

When extending this service layer:

1. Add new query templates to `BaseQuery` for reusable operations
2. Create specialized services for new resource types following the pattern of `EnvironmentService` and `ModelService`
3. Define Pydantic models in `models.py` for any new data structures
4. Maintain consistent error handling and documentation

## API Limitations

Be aware of the following limitations when using the dbt Cloud API:

1. Rate limits may apply to API requests
2. Some operations may be computationally expensive for large dbt projects
3. API responses may be paginated for large result sets

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
