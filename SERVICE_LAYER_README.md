# dbt Discovery API Service Layer

## Overview

The dbt Discovery API is a Python-based service layer that interacts with dbt Cloud's metadata API to retrieve and process information about dbt environments, models, and related resources. This service layer abstracts the complexities of GraphQL queries and provides a clean interface for working with dbt Cloud metadata.

## Core Components

### 1. Base Query Service (`BaseQuery.py`)

The foundation of the service layer that handles all GraphQL interactions with the dbt Cloud API.

- **Key Features**:
  - Authentication with dbt Cloud API using service tokens
  - GraphQL operation execution
  - Pre-configured query templates for common operations (environments, applied state, definition state)
  - Utility functions for creating customized queries

- **Usage**:
  ```python
  from src.services.BaseQuery import BaseQuery
  
  # Initialize with token (or uses DBT_SERVICE_TOKEN environment variable)
  query_service = BaseQuery(token="your_token")
  
  # Execute pre-configured queries
  op, env = query_service.create_environment_query(environment_id=123)
  result = query_service.execute(op)
  ```

### 2. Environment Service (`EnvironmentService.py`)

Provides specialized functionality for working with dbt environments.

- **Key Features**:
  - Retrieve environment details
  - Get environment resources (models, sources, tests, etc.)
  - Access environment state information (applied and definition states)
  - Query environment models with filtering capabilities

- **Usage**:
  ```python
  from src.services.EnvironmentService import EnvironmentService
  
  # Initialize with environment ID and optional token
  env_service = EnvironmentService(environment_id=123, token="your_token")
  
  # Get environment details
  env_details = env_service.get_environment()
  
  # Get models with optional filtering
  models = env_service.get_models(materialized_types=["table", "view"])
  ```

### 3. Model Service (`ModelService.py`)

Specialized service for working with dbt models, providing detailed information and relationships.

- **Key Features**:
  - Retrieve detailed model information
  - Get model lineage (upstream/downstream dependencies)
  - Access model run history
  - Query model tests and test results
  - Retrieve model SQL code (raw and compiled)

- **Usage**:
  ```python
  from src.services.ModelService import ModelService
  
  # Initialize with model unique ID, environment ID, and optional token
  model_service = ModelService(
      unique_id="model.project.model_name",
      environment_id=123,
      token="your_token"
  )
  
  # Get model details
  model_details = model_service.get_model()
  
  # Get model lineage
  upstream = model_service.get_upstream_models()
  downstream = model_service.get_downstream_models()
  
  # Get model tests
  tests = model_service.get_tests()
  ```

## Data Models (`models.py`)

The service layer uses Pydantic models to represent dbt resources with proper typing and validation.

- **Key Models**:
  - `Environment`: Represents a dbt environment
  - `Project`: Represents a dbt project
  - `ModelBase`: Base class for all model-related data structures
  - `ModelDefinition`: Represents a model's definition state
  - `ModelApplied`: Represents a model's applied state
  - `ModelHistoricalRun`: Represents a historical run of a model

## Authentication

The service layer supports authentication with dbt Cloud via service tokens:

1. **Direct token provision**: Pass a token directly to service constructors
2. **Environment variable**: Set the `DBT_SERVICE_TOKEN` environment variable

## Common Workflows

### Getting All Models in an Environment

```python
from src.services.EnvironmentService import EnvironmentService

env_service = EnvironmentService(environment_id=123)
models = env_service.get_models()

# Filter models by type
table_models = env_service.get_models(materialized_types=["table"])
```

### Analyzing Model Lineage

```python
from src.services.ModelService import ModelService

model_service = ModelService(
    unique_id="model.project.model_name",
    environment_id=123
)

# Get upstream dependencies
upstream = model_service.get_upstream_models()

# Get downstream dependencies
downstream = model_service.get_downstream_models()

# Print dependency tree
print(f"Model {model_service.unique_id} depends on {len(upstream)} models")
print(f"Model {model_service.unique_id} is used by {len(downstream)} models")
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

# Get compiled SQL
compiled_sql = model_service.get_compiled_sql()
```

## Technical Details

- **GraphQL**: The service layer uses the `sgqlc` library to interact with dbt Cloud's GraphQL API
- **Authentication**: Bearer token authentication via HTTP headers
- **Data Validation**: Pydantic models ensure type safety and data validation
- **Error Handling**: Comprehensive error handling for API interactions

## Development Notes

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
