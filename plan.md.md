# DBT Discovery API Layer Plan

## Overview
The API layer provides a user-friendly interface on top of the service layer, abstracting away the complexity of GraphQL queries and data transformations. It offers logical, intuitive access to dbt Cloud resources.

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

class RunStatus(BaseModel):
    """Run status information"""
    status: str  # success, error, running
    run_id: str
    run_time: datetime
    execution_time: Optional[float] = None
    error_message: Optional[str] = None

class ProjectMetadata(BaseModel):
    """Project metadata information"""
    dbt_project_name: str
    adapter_type: str
    environment_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
```

## Core Classes

### DiscoveryAPI
```python
class DiscoveryAPI:
    """Main entry point for the API layer"""
    
    def __init__(self, token: str = None, endpoint: str = "https://metadata.cloud.getdbt.com/graphql"):
        """Initialize with authentication token and endpoint."""
        self._token = token
        self._endpoint = endpoint
        # Initialize service layer components
        self._environment_service = EnvironmentService(token, endpoint)
        self._model_service = ModelService(token, endpoint)
        # Future services will be added here
        # self._job_service = JobService(token, endpoint)
        # self._test_service = TestService(token, endpoint)
    
    def project(self, environment_id: int) -> 'Project':
        """Get a project by environment ID."""
        # Validate the environment exists via service layer
        environment = self._environment_service.get_environment(environment_id)
        if not environment:
            raise ValueError(f"Environment with ID {environment_id} not found")
        
        # Return a Project instance with access to the services
        return Project(
            environment_id=environment_id,
            environment_service=self._environment_service,
            model_service=self._model_service
            # Add other services as they become available
        )
```

### Project
```python
class Project:
    """Represents a dbt project with access to all resources"""
    
    def __init__(self, environment_id: int, environment_service: EnvironmentService, 
                 model_service: ModelService):
        """Initialize with environment ID and service layer components."""
        self.environment_id = environment_id
        self._environment_service = environment_service
        self._model_service = model_service
        # Cache for models to avoid repeated service calls
        self._models_cache = None
    
    def get_metadata(self) -> ProjectMetadata:
        """Get project metadata."""
        # Use environment service to fetch metadata
        environment = self._environment_service.get_environment(self.environment_id)
        return ProjectMetadata(
            dbt_project_name=environment.dbt_project_name,
            adapter_type=environment.adapter_type,
            environment_id=self.environment_id,
            created_at=environment.created_at,
            updated_at=environment.updated_at
        )
    
    def get_models(self, refresh: bool = False) -> List['Model']:
        """Get all models in the project."""
        # Use cache unless refresh is requested
        if self._models_cache is None or refresh:
            # Get models from service layer
            service_models = self._model_service.get_models_applied(self.environment_id)
            # Transform service models to API models
            self._models_cache = [
                Model(
                    project=self,
                    model_data=model
                ) for model in service_models
            ]
        return self._models_cache
    
    def get_model(self, model_name: str) -> 'Model':
        """Get a specific model by name."""
        # First check cache if available
        if self._models_cache:
            model = next((m for m in self._models_cache if m.metadata.name == model_name), None)
            if model:
                return model
        
        # If not in cache or cache not initialized, fetch directly
        service_model = self._model_service.get_model_by_name(
            self.environment_id, model_name, state="applied"
        )
        
        if not service_model:
            raise ValueError(f"Model '{model_name}' not found")
            
        return Model(project=self, model_data=service_model)
    
    def get_model_historical_runs(self, model_name: str, limit: int = 5) -> List[RunStatus]:
        """Get historical runs for a specific model."""
        # Use model service to fetch historical runs
        runs = self._model_service.get_model_historical_runs(
            self.environment_id, model_name, limit=limit
        )
        
        # Transform to user-friendly format
        return [RunStatus(
            status=run.status,
            run_id=run.run_id,
            run_time=run.run_time,
            execution_time=run.execution_time,
            error_message=run.error_message
        ) for run in runs]
    
    # Future methods
    def get_tests(self) -> List['Test']:
        """Get all tests in the project."""
        # Will be implemented when TestService is available
        pass
    
    def get_jobs(self) -> List['Job']:
        """Get all jobs in the project."""
        # Will be implemented when JobService is available
        pass
```

### Model
```python
class Model:
    """Represents a dbt model with properties"""
    
    def __init__(self, project: Project, model_data: Any):
        """Initialize with reference to parent project and model data."""
        self._project = project
        self._model_data = model_data
        # Cache computed properties
        self._metadata = None
        self._last_run = None
    
    @property
    def metadata(self) -> ModelMetadata:
        """Get model metadata."""
        if self._metadata is None:
            self._metadata = ModelMetadata(
                name=self._model_data.name,
                unique_id=self._model_data.unique_id,
                database=self._model_data.database,
                schema=self._model_data.schema,
                description=self._model_data.description,
                materialized=self._model_data.materialized,
                tags=self._model_data.tags
            )
        return self._metadata
    
    @property
    def last_run(self) -> Optional[RunStatus]:
        """Get last run status."""
        if self._last_run is None:
            # Get historical runs from project
            runs = self._project.get_model_historical_runs(self.metadata.name, limit=1)
            if runs:
                self._last_run = runs[0]
            else:
                self._last_run = None
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
            # Add other relevant properties
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

1. The API layer should handle all error cases gracefully, providing clear error messages.
2. Caching strategies should be implemented to minimize service calls.
3. All properties should be lazy-loaded when possible to improve performance.
4. Future extensions should include:
   - Test management
   - Job scheduling and monitoring
   - Source management
   - Lineage exploration
