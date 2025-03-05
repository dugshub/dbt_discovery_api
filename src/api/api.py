"""
DBT Discovery API Layer - User-friendly interface to the dbt Cloud API.

Provides intuitive access to dbt Cloud resources without the complexity of GraphQL.
"""

from typing import List, Dict, Optional, Any, cast

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
        self._metadata: Optional[ModelMetadata] = None
        self._last_run: Optional[RunStatus] = None
    
    @property
    def metadata(self) -> ModelMetadata:
        """Get model metadata."""
        if self._metadata is None:
            # Convert service model to API model using model_validate
            self._metadata = ModelMetadata.model_validate(self._model_data)
        return cast(ModelMetadata, self._metadata)
    
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
        self._models_cache: Optional[List[Model]] = None
    
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
        return cast(List[Model], self._models_cache)
    
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
    
    def get_models_with_runtime(self, refresh: bool = False, descending: bool = True, limit: int = 0) -> List[ModelWithRuntime]:
        """
        Get all models in the project with their runtime metrics.
        
        This method leverages the execution_info data that is already fetched
        with the models, eliminating the need for additional API calls.
        
        Args:
            refresh: Force refresh of model cache
            descending: Sort by runtime in descending order if True, ascending if False
            limit: Maximum number of models to return (0 means no limit)
            
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
        
        # Sort by execution_time
        result.sort(
            key=lambda m: (m.runtime_metrics.execution_info.get('execution_time') or 0),
            reverse=descending
        )
        
        # Apply limit if specified
        if limit > 0:
            result = result[:limit]
            
        return result
    
    def get_historical_models_runtimes(self, models: Optional[List[str]] = None, fastest: bool = False, slowest: bool = False, limit: int = 10) -> List[ModelRuntimeMetrics]:
        """Get historical models runtimes with optimized batch querying.
        
        This method uses a batched GraphQL query to fetch historical runs for multiple models
        in a single API call, improving performance significantly.
        
        Args:
            models: Optional list of model names to get historical runtimes for.
                   If None, will use fastest or slowest to determine which models to fetch.
            fastest: If True and models is None, returns historical runs for the fastest models.
            slowest: If True and models is None, returns historical runs for the slowest models.
            limit: Maximum number of models to return (capped at 10).
                  
        Returns:
            List of ModelRuntimeMetrics objects containing runtime data for each model.
        """
        # Enforce hard limit
        if limit > 10:
            limit = 10
            
        # Get model names based on parameters
        model_names_to_fetch = []
        
        if models is not None:
            # Use provided model names list
            model_names_to_fetch = models[:limit]  # Apply limit
        else:
            # Set default behavior to slowest=True unless fastest is explicitly True
            is_descending = not fastest  # True for slowest (default), False for fastest
            sorted_models = self.get_models_with_runtime(descending=is_descending, limit=limit)
            model_names_to_fetch = [model.name for model in sorted_models]
        
        if not model_names_to_fetch:
            return []
            
        # Use batch query to fetch all historical runs at once
        historical_runs_by_model = self._model_service.get_multiple_models_historical_runs(
            self.environment_id, model_names_to_fetch, last_run_count=5
        )
        
        # Pre-fetch all models metadata in one go
        models_data = {
            model.metadata.name: model 
            for model in self.get_models() 
            if model.metadata.name in model_names_to_fetch
        }
        
        # Create runtime metrics for each model
        result = []
        for model_name in model_names_to_fetch:
            # Get historical runs for this model
            historical_runs = historical_runs_by_model.get(model_name, [])
            
            # Get the model to access its execution_info
            model = models_data.get(model_name)
            execution_info = model._model_data.execution_info if model else {}
            
            # Create most_recent_run from first historical run if available
            most_recent_run = historical_runs[0] if historical_runs else None
            
            # Create runtime metrics
            runtime_metrics = ModelRuntimeMetrics(
                most_recent_run=most_recent_run,
                execution_info=execution_info
            )
            
            result.append(runtime_metrics)
            
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