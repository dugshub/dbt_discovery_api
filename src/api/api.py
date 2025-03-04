"""
DBT Discovery API Layer - User-friendly interface to the dbt Cloud API.

Provides intuitive access to dbt Cloud resources without the complexity of GraphQL.
"""

from typing import List, Dict, Optional, Any

from src.services.BaseQuery import BaseQuery
from src.services.EnvironmentService import EnvironmentService
from src.services.ModelService import ModelService
from src.api.models import (
    ModelMetadata, 
    RunStatus, 
    ProjectMetadata,
    ModelRuntimeMetrics,
    ModelWithRuntime
)


# API Core Classes
class Model:
    """Represents a dbt model with properties"""
    
    def __init__(self, project: 'Project', model_data: Any):
        self._project = project
        self._model_data = model_data
        # Cache computed properties
        self._metadata = None
        self._last_run = None
    
    @property
    def metadata(self) -> ModelMetadata:
        """Get model metadata."""
        if self._metadata is None:
            # Convert service model to API model using model_validate
            self._metadata = ModelMetadata.model_validate(self._model_data)
        assert self._metadata is not None
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
            "materialized": self.metadata.materialized,
            "tags": self.metadata.tags,
            "last_run": self.last_run.model_dump() if self.last_run else None,
        }


class Project:
    """Represents a dbt project with access to all resources"""
    
    def __init__(self, environment_id: int, environment_service: EnvironmentService, model_service: ModelService):
        self.environment_id = environment_id
        self._environment_service = environment_service
        self._model_service = model_service
        self._models_cache = None
    
    def get_metadata(self) -> ProjectMetadata:
        """Get project metadata."""
        # Get environment data
        environment = self._environment_service.get_environment_metadata(self.environment_id)
        
        # Add environment_id to the data
        environment['environment_id'] = self.environment_id
        
        # Convert to API model using model_validate
        return ProjectMetadata.model_validate(environment)
    
    def get_models(self, refresh: bool = False) -> List[Model]:
        """Get all models in the project."""
        # Use cache unless refresh is requested
        if self._models_cache is None or refresh:
            # Get models from service layer
            service_models = self._model_service.get_models_applied(self.environment_id)
            
            # Transform to API models
            self._models_cache = [
                Model(project=self, model_data=model)
                for model in service_models
            ]
        assert self._models_cache is not None
        return self._models_cache
    
    def get_model(self, model_name: str) -> Model:
        """Get a specific model by name."""
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
        """Get historical runs for a specific model."""
        # Get runs from service layer
        service_runs = self._model_service.get_model_historical_runs(
            self.environment_id, model_name, last_run_count=limit
        )
        
        # Convert to API models using model_validate
        return [RunStatus.model_validate(run) for run in service_runs]
    
    def get_models_with_runtime(self, refresh: bool = False) -> List[ModelWithRuntime]:
        """
        Get all models in the project with their runtime metrics.
        
        This method leverages the execution_info data that is already fetched
        with the models, eliminating the need for additional API calls.
        
        Args:
            refresh: Force refresh of model cache
            
        Returns:
            List of typed ModelWithRuntime objects containing metadata and runtime metrics
        """
        # Get all models with their execution_info
        models = self.get_models(refresh=refresh)
        result = []
        
        for model in models:
            # Get execution_info from the model's data
            execution_info = model._model_data.execution_info
            
            # Create RunStatus from execution_info
            most_recent_run = None
            if execution_info and 'last_run_id' in execution_info:
                # Convert run_id to string to match the RunStatus model definition
                run_id = execution_info.get('last_run_id')
                if run_id is not None:
                    run_id = str(run_id)
                    
                most_recent_run = RunStatus(
                    status=execution_info.get('last_run_status'),
                    run_id=run_id,
                    run_generated_at=execution_info.get('run_generated_at'),
                    execution_time=execution_info.get('execution_time'),
                    error=execution_info.get('last_run_error')
                )
            
            # Create runtime metrics
            runtime_metrics = ModelRuntimeMetrics(
                most_recent_run=most_recent_run,
                execution_info=execution_info
            )
            
            # Create full model with runtime data
            model_with_runtime = ModelWithRuntime(
                name=model.metadata.name,
                unique_id=model.metadata.unique_id,
                metadata=model.metadata,
                runtime_metrics=runtime_metrics
            )
            
            result.append(model_with_runtime)
            
        return result
    
    # Placeholder methods for future implementations
    def get_tests(self) -> List[Any]:
        """Get all tests in the project (not implemented yet)."""
        # Will be implemented when TestService is available
        raise NotImplementedError("Test retrieval not implemented yet")
    
    def get_jobs(self) -> List[Any]:
        """Get all jobs in the project (not implemented yet)."""
        # Will be implemented when JobService is available
        raise NotImplementedError("Job retrieval not implemented yet")


class DiscoveryAPI:
    """Main entry point for the API layer"""
    
    def __init__(self, token: Optional[str] = None, endpoint: str = "https://metadata.cloud.getdbt.com/graphql"):
        # Initialize service layer components
        base_query = BaseQuery(token, endpoint)
        self._environment_service = EnvironmentService(base_query)
        self._model_service = ModelService(base_query)
    
    def project(self, environment_id: int) -> Project:
        """Get a project by environment ID."""
        # Validate the environment exists by trying to get metadata
        try:
            self._environment_service.get_environment_metadata(environment_id)
        except Exception as e:
            raise ValueError(f"Environment with ID {environment_id} not found: {str(e)}")
        
        # Return a Project instance
        return Project(
            environment_id=environment_id,
            environment_service=self._environment_service,
            model_service=self._model_service
        )