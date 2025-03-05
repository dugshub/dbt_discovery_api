"""
DBT Discovery API Layer - User-friendly interface to the dbt Cloud API.

Provides intuitive access to dbt Cloud resources without the complexity of GraphQL.
"""

import os
import yaml
from typing import List, Dict, Optional, Any, cast

from src.discovery_api.services.BaseQuery import BaseQuery
from src.discovery_api.services.EnvironmentService import EnvironmentService
from src.discovery_api.services.ModelService import ModelService
from src.discovery_api.api.models import (
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
    
    def __init__(self, environment_id: int, environment_service: EnvironmentService, model_service: ModelService, return_query: bool = False):
        self.environment_id = environment_id
        self._environment_service = environment_service
        self._model_service = model_service
        self._models_cache: Optional[List[Model]] = None
        self.return_query = return_query
    
    def get_metadata(self, return_query: bool = None) -> ProjectMetadata:
        """
        Get project metadata.
        
        Args:
            return_query: If True, include the GraphQL query in the response.
                         Defaults to the Project's return_query setting.
        """
        # Determine if we should return the query
        include_query = self.return_query if return_query is None else return_query
        
        # Get environment data with query if requested
        environment = self._environment_service.get_environment_metadata(
            self.environment_id, 
            return_query=include_query
        )
        
        # Add environment_id to the data
        environment['environment_id'] = self.environment_id
        
        # Convert to API model using model_validate
        return ProjectMetadata.model_validate(environment)
    
    def get_models(self, refresh: bool = False, return_query: bool = None) -> List[Model]:
        """
        Get all models in the project.
        
        Args:
            refresh: Force refresh of model cache
            return_query: If True, include the GraphQL query in the response.
                         Defaults to the Project's return_query setting.
        """
        # Determine if we should return the query
        include_query = self.return_query if return_query is None else return_query
        
        # Use cache unless refresh is requested
        if self._models_cache is None or refresh:
            # Get models from service layer
            service_models = self._model_service.get_models_applied(
                self.environment_id,
                return_query=include_query
            )
            
            # Transform to API models
            self._models_cache = [
                Model(project=self, model_data=model)
                for model in service_models
            ]
        return cast(List[Model], self._models_cache)
    
    def get_model(self, model_name: str, return_query: bool = None) -> Model:
        """
        Get a specific model by name.
        
        Args:
            model_name: The name of the model to fetch
            return_query: If True, include the GraphQL query in the response.
                         Defaults to the Project's return_query setting.
        """
        # Determine if we should return the query
        include_query = self.return_query if return_query is None else return_query
        
        # First check cache if available
        if self._models_cache:
            model = next((m for m in self._models_cache if m.metadata.name == model_name), None)
            if model:
                return model
        
        # If not in cache, fetch directly
        service_model = self._model_service.get_model_by_name(
            self.environment_id, model_name, state="applied", return_query=include_query
        )
        
        if not service_model:
            raise ValueError(f"Model '{model_name}' not found")
            
        return Model(project=self, model_data=service_model)
    
    def get_model_historical_runs(self, model_name: str, limit: int = 5, return_query: bool = None) -> List[RunStatus]:
        """
        Get historical runs for a specific model.
        
        Args:
            model_name: The name of the model to fetch runs for
            limit: Maximum number of runs to fetch
            return_query: If True, include the GraphQL query in the response.
                         Defaults to the Project's return_query setting.
        """
        # Determine if we should return the query
        include_query = self.return_query if return_query is None else return_query
        
        # Get runs from service layer
        service_runs = self._model_service.get_model_historical_runs(
            self.environment_id, model_name, last_run_count=limit, return_query=include_query
        )
        
        # Convert to API models using model_validate
        return [RunStatus.model_validate(run) for run in service_runs]
    
    def get_models_with_runtime(self, refresh: bool = False, descending: bool = True, limit: int = 0, return_query: bool = None) -> List[ModelWithRuntime]:
        """
        Get all models in the project with their runtime metrics.
        
        This method leverages the execution_info data that is already fetched
        with the models, eliminating the need for additional API calls.
        
        Args:
            refresh: Force refresh of model cache
            descending: Sort by runtime in descending order if True, ascending if False
            limit: Maximum number of models to return (0 means no limit)
            return_query: If True, include the GraphQL query in the response.
                         Defaults to the Project's return_query setting.
            
        Returns:
            List of typed ModelWithRuntime objects containing metadata and runtime metrics
        """
        # Determine if we should return the query
        include_query = self.return_query if return_query is None else return_query
        
        # Get all models with their execution_info
        models = self.get_models(refresh=refresh, return_query=include_query)
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
    
    def get_historical_models_runtimes(self, models: Optional[List[str]] = None, fastest: bool = False, slowest: bool = False, limit: int = 10, return_query: bool = None) -> List[ModelRuntimeMetrics]:
        """Get historical models runtimes with optimized batch querying.
        
        This method uses a batched GraphQL query to fetch historical runs for multiple models
        in a single API call, improving performance significantly.
        
        Args:
            models: Optional list of model names to get historical runtimes for.
                   If None, will use fastest or slowest to determine which models to fetch.
            fastest: If True and models is None, returns historical runs for the fastest models.
            slowest: If True and models is None, returns historical runs for the slowest models.
            limit: Maximum number of models to return (capped at 10).
            return_query: If True, include the GraphQL query in the response.
                         Defaults to the Project's return_query setting.
                  
        Returns:
            List of ModelRuntimeMetrics objects containing runtime data for each model.
        """
        # Determine if we should return the query
        include_query = self.return_query if return_query is None else return_query
        
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
            self.environment_id, model_names_to_fetch, last_run_count=5, return_query=include_query
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
    
    def __init__(self, token: Optional[str] = None, endpoint: str = "https://metadata.cloud.getdbt.com/graphql", 
                 config_file: str = "config.yml", return_query: bool = False):
        """
        Initialize the Discovery API.
        
        Args:
            token: The authentication token for the dbt Cloud API. 
                  If None, will try to use the DBT_SERVICE_TOKEN environment variable.
            endpoint: The GraphQL endpoint to use.
            config_file: Path to YAML configuration file containing environment IDs for projects.
                        Defaults to config.yml in the current directory.
            return_query: If True, all API responses will include the raw GraphQL query that was executed.
                         This is useful for debugging or understanding the underlying queries.
        """
        # Initialize service layer components
        base_query = BaseQuery(token, endpoint)
        self._environment_service = EnvironmentService(base_query)
        self._model_service = ModelService(base_query)
        self.return_query = return_query
        
        # Dictionary to store Project instances
        self._projects: Dict[str, Project] = {}
        
        # Load configuration
        self._config = self._load_config(config_file)
        
        # Initialize projects from config
        self._initialize_projects()
    
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """
        Load configuration from YAML file.
        
        Args:
            config_file: Path to the YAML config file
            
        Returns:
            Dictionary containing the parsed configuration
        """
        if not os.path.exists(config_file):
            return {"projects": {}}
            
        with open(config_file, "r") as f:
            config = yaml.safe_load(f)
            return config if config else {"projects": {}}
    
    def _initialize_projects(self) -> None:
        """Initialize project instances from the configuration."""
        if "projects" not in self._config:
            return
            
        for project_name, project_config in self._config["projects"].items():
            if "prod_env_id" in project_config:
                env_id = project_config["prod_env_id"]
                try:
                    self._projects[project_name] = self.project(env_id)
                except ValueError:
                    # Skip if environment doesn't exist or is inaccessible
                    pass
    
    @property
    def projects(self) -> Dict[str, Project]:
        """Get all initialized projects."""
        return self._projects
    
    def project(self, environment_id: int, return_query: bool = None) -> Project:
        """
        Get a project by environment ID.
        
        Args:
            environment_id: The dbt Cloud environment ID
            return_query: If True, include the GraphQL query in the response.
                         Defaults to the API's return_query setting.
        """
        # Determine if we should return the query
        include_query = self.return_query if return_query is None else return_query
        
        # Validate the environment exists by trying to get metadata
        try:
            self._environment_service.get_environment_metadata(environment_id)
        except Exception as e:
            raise ValueError(f"Environment with ID {environment_id} not found: {str(e)}")
        
        # Return a Project instance
        return Project(
            environment_id=environment_id,
            environment_service=self._environment_service,
            model_service=self._model_service,
            return_query=include_query
        )