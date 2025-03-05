# DBT Discovery API Layer Plan


----- Model Runtime Averages ----- 
## Overview
The API layer provides a user-friendly interface on top of the service layer, abstracting away the complexity of GraphQL queries and data transformations. It offers logical, intuitive access to dbt Cloud resources.

## Models API Enhancement: Runtime by Project

### Feature Requirements
Add functionality to retrieve all models and their runtime metrics by project:
- Average run time for last N runs
- Most recent run details
- Complete list of last N runs for each model

### Current State Analysis
1. **Service Layer**:
   - `ModelService.get_models_applied()` retrieves all models for an environment
   - `ModelService.get_model_historical_runs()` retrieves historical runs for a specific model

2. **API Layer**:
   - `Project.get_models()` returns all models in a project
   - `Model.get_historical_runs()` gets run history for a single model
   - No existing method to get runtime metrics for all models in a project at once

### Implementation Plan

#### 1. Add Helper Method to API Layer
Create a new method in the `Project` class to process and aggregate runtime data:

```python
def get_models_with_runtime(self, last_n_runs: int = 5, refresh: bool = False) -> List[Dict[str, Any]]:
    """
    Get all models in the project with their runtime metrics.
    
    Args:
        last_n_runs: Number of historical runs to analyze
        refresh: Force refresh of model cache
        
    Returns:
        List of models with runtime metrics (name, metadata, average_runtime, 
        most_recent_run, historical_runs)
    """
```

#### 2. Implementation Approach
1. Leverage existing `get_models()` method to retrieve all models
2. For each model, fetch historical runs using `get_model_historical_runs()`
3. Calculate metrics (average runtime, last run details)
4. Return structured data with all required metrics

#### 3. Data Structure
Return a list of dictionaries with:
- Model metadata (name, unique_id, etc.)
- Average runtime (calculated from historical runs)
- Most recent run (detailed info on last execution)
- Historical runs (complete list of last N runs)

#### 4. Optional Optimization
- Consider adding batch fetching capability to `ModelService` to reduce API calls
- Implement caching to minimize redundant API requests

#### 5. Example Usage
```python
# Get all models with runtime metrics for a project
api = DiscoveryAPI(token="your_token")
project = api.project(environment_id=123)
models_with_runtime = project.get_models_with_runtime(last_n_runs=10)

----- Existing Plan -----

# Process and display results
for model in models_with_runtime:
    print(f"Model: {model['name']}")
    print(f"Average Runtime: {model['average_runtime']}s")
    print(f"Last Run Status: {model['most_recent_run']['status']}")
```

### Additional Considerations
- This implementation maintains separation of concerns - API layer for data transformation, Service layer for API interaction
- No changes needed to Service layer
- Method will be efficient by leveraging existing caching mechanisms
- Implementation can scale to handle large projects with many models

## Implementation Strategy

1. Enable ORM mode in existing service layer models
2. Create API-specific Pydantic models for user-facing interfaces
3. Use `from_orm` to convert service models to API models
4. Add computed properties for data that spans multiple service models

## Pydantic Data Types

```python
# Common Pydantic models for type safety and validation

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime

class ModelMetadata(BaseModel):
    """Model metadata information"""
    name: str
    unique_id: str
    database: Optional[str] = None
    schema: Optional[str] = None
    description: Optional[str] = None
    materialized: str
    tags: List[str] = Field(default_factory=list)
    
    class Config:
        orm_mode = True  # Enable ORM mode for conversion from service models

class RunStatus(BaseModel):
    """Run status information"""
    status: str  # success, error, running
    run_id: str
    run_time: datetime
    execution_time: Optional[float] = None
    error_message: Optional[str] = None
    
    class Config:
        orm_mode = True

class ProjectMetadata(BaseModel):
    """Project metadata information"""
    dbt_project_name: str
    adapter_type: str
    environment_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True
```

## Core Classes

### DiscoveryAPI
```python
class DiscoveryAPI:
    """Main entry point for the API layer"""
    
    def __init__(self, token: str = None, endpoint: str = "https://metadata.cloud.getdbt.com/graphql"):
        # Initialize service layer components
        self._environment_service = EnvironmentService(token, endpoint)
        self._model_service = ModelService(token, endpoint)
        # Future services will be added here
    
    def project(self, environment_id: int) -> 'Project':
        # Validate the environment exists
        environment = self._environment_service.get_environment(environment_id)
        if not environment:
            raise ValueError(f"Environment with ID {environment_id} not found")
        
        # Return a Project instance
        return Project(
            environment_id=environment_id,
            environment_service=self._environment_service,
            model_service=self._model_service
        )
```

### Project
```python
class Project:
    """Represents a dbt project with access to all resources"""
    
    def __init__(self, environment_id: int, environment_service, model_service):
        self.environment_id = environment_id
        self._environment_service = environment_service
        self._model_service = model_service
        self._models_cache = None
    
    def get_metadata(self) -> ProjectMetadata:
        # Get environment data
        environment = self._environment_service.get_environment(self.environment_id)
        
        # Convert to API model using from_orm
        return ProjectMetadata.from_orm(environment)
    
    def get_models(self, refresh: bool = False) -> List['Model']:
        # Use cache unless refresh is requested
        if self._models_cache is None or refresh:
            # Get models from service layer
            service_models = self._model_service.get_models_applied(self.environment_id)
            
            # Transform to API models
            self._models_cache = [
                Model(project=self, model_data=model)
                for model in service_models
            ]
        return self._models_cache
    
    def get_model(self, model_name: str) -> 'Model':
        # First check cache if available
        if self._models_cache:
            model = next((m for m in self._models_cache if m.metadata.name == model_name), None)
            if model:
                return model
        
        # If not in cache, fetch directly
        service_model = self._model_service.get_model_by_name(
            self.environment_id, model_name, state="applied"
        )
        
        if not service_model:
            raise ValueError(f"Model '{model_name}' not found")
            
        return Model(project=self, model_data=service_model)
    
    def get_model_historical_runs(self, model_name: str, limit: int = 5) -> List[RunStatus]:
        # Get runs from service layer
        service_runs = self._model_service.get_model_historical_runs(
            self.environment_id, model_name, limit=limit
        )
        
        # Convert to API models using from_orm
        return [RunStatus.from_orm(run) for run in service_runs]
    
    # Future methods
    def get_tests(self) -> List['Test']:
        # Will be implemented when TestService is available
        pass
    
    def get_jobs(self) -> List['Job']:
        # Will be implemented when JobService is available
        pass
```

### Model
```python
class Model:
    """Represents a dbt model with properties"""
    
    def __init__(self, project: Project, model_data: Any):
        self._project = project
        self._model_data = model_data
        # Cache computed properties
        self._metadata = None
        self._last_run = None
    
    @property
    def metadata(self) -> ModelMetadata:
        """Get model metadata."""
        if self._metadata is None:
            # Convert service model to API model using from_orm
            self._metadata = ModelMetadata.from_orm(self._model_data)
        return self._metadata
    
    @property
    def last_run(self) -> Optional[RunStatus]:
        """Get last run status."""
        if self._last_run is None:
            # Get historical runs from project
            runs = self._project.get_model_historical_runs(self.metadata.name, limit=1)
            self._last_run = runs[0] if runs else None
        return self._last_run
    
    def get_historical_runs(self, limit: int = 5) -> List[RunStatus]:
        """Get historical runs for this model."""
        return self._project.get_model_historical_runs(self.metadata.name, limit=limit)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary representation."""
        return {
            "name": self.metadata.name,
            "unique_id": self.metadata.unique_id,
            "database": self.metadata.database,
            "schema": self.metadata.schema,
            "description": self.metadata.description,
            "last_run": self.last_run.dict() if self.last_run else None,
        }
```

## Example Usage

```python
# Initialize API
api = DiscoveryAPI(token="your_dbt_cloud_token")

# Get project
project = api.project(environment_id=123456)

# Get project metadata
metadata = project.get_metadata()
print(f"Project name: {metadata.dbt_project_name}")
print(f"Adapter type: {metadata.adapter_type}")

# Get all models
models = project.get_models()

# Get specific model
model = project.get_model("my_model")

# Access model properties
print(f"Model: {model.metadata.name}")
print(f"Database: {model.metadata.database}")
print(f"Last run status: {model.last_run.status if model.last_run else 'No runs'}")

# Get historical runs
runs = model.get_historical_runs(limit=10)
```

## Implementation Notes

### Service Layer Updates

Update the existing service layer models in `src/models.py` to enable ORM mode:

```python
class ModelBase(BaseModel):
    """Base model for all dbt-tools models."""
    
    class Config:
        orm_mode = True  # Enable ORM mode for all derived models
```

### Testing Strategy

1. **Service Layer Tests**
   ```python
   def test_model_orm_mode():
       """Test that service models work with ORM mode."""
       model = Model(name="test_model", unique_id="model.test.test_model")
       model_dict = model.dict()
       new_model = Model.parse_obj(model_dict)
       assert new_model.name == model.name
   ```

2. **API Model Tests**
   ```python
   def test_api_model_from_service_model():
       """Test creating API model from service model using from_orm."""
       service_model = Model(name="test_model", unique_id="model.test.test_model")
       api_model = ModelMetadata.from_orm(service_model)
       assert api_model.name == service_model.name
   ```

3. **API Layer Tests**
   ```python
   def test_api_get_model():
       """Test getting a model through the API layer."""
       api = DiscoveryAPI(token="test_token")
       project = api.project(environment_id=123)
       model = project.get_model("test_model")
       assert model.metadata.name == "test_model"
   ```

### Risks and Mitigations

1. **Risk**: Field name mismatches between service and API models
   **Mitigation**: Ensure API model field names match service model field names for direct properties

2. **Risk**: Performance impact from model conversion
   **Mitigation**: Implement caching strategies to minimize conversions

3. **Risk**: Complexity in handling computed fields
   **Mitigation**: Keep computed field logic simple and well-documented

### Best Practices

1. Handle all error cases gracefully with clear error messages
2. Implement caching to minimize service calls
3. Use lazy-loading for properties that require additional service calls
4. Maintain clear separation between service and API layers
