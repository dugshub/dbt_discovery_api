"""Project implementation for the discovery API."""

from typing import List, Optional, Dict, Any
import logging
from functools import lru_cache

from src.discovery_api.services.BaseQuery import BaseQuery
from src.discovery_api.services.EnvironmentService import EnvironmentService
from src.discovery_api.services.ModelService import ModelService
from src.discovery_api.services.JobService import JobService
from src.discovery_api.models.filters import SearchFilter, ModelFilter
from src.discovery_api.api.resources.model import Model
from src.discovery_api.api.resources.job import Job


logger = logging.getLogger("dbt_discovery_api")


class Project:
    """
    Represents a dbt project (environment in dbt Cloud).
    
    A project in this context is an environment in dbt Cloud. It provides methods
    to query models and jobs within the environment.
    """
    
    def __init__(self, environment_id: str, name: Optional[str] = None, base_query: Optional[BaseQuery] = None):
        """
        Initialize a Project.
        
        Args:
            environment_id: The environment ID in dbt Cloud.
            name: Optional project name. If not provided, will try to fetch from environment.
            base_query: Optional BaseQuery instance. If not provided, will create a new one.
        """
        self.environment_id = environment_id
        self.name = name
        
        # Initialize services
        self.base_query = base_query or BaseQuery()
        self.environment_service = EnvironmentService(self.base_query)
        self.model_service = ModelService(self.base_query)
        self.job_service = JobService(self.base_query)
        
        # Lazy-loaded properties
        self._models: Optional[List[Model]] = None
        self._jobs: Optional[List[Job]] = None
        self._model_count: Optional[int] = None
        self._job_count: Optional[int] = None
        
        # If name not provided, try to fetch it
        if not self.name:
            try:
                env_data = self.environment_service.get_environment_metadata(int(self.environment_id))
                self.name = env_data.get('dbt_project_name', f"project_{self.environment_id}")
            except Exception as e:
                logger.warning(f"Failed to fetch project name for environment {environment_id}: {str(e)}")
                self.name = f"project_{self.environment_id}"
    
    @property
    def model_count(self) -> int:
        #TODO: Check this - we quickly swapped to definition state
        """Get the number of models in the project."""
        if self._model_count is None:
            try:
                # Try to get from definition state which has resource_counts
                definition_state = self.environment_service.get_definition_state(int(self.environment_id))
                self._model_count = definition_state.get('resource_counts', {}).get('model', 0)
            except Exception as e:
                logger.warning(f"Failed to fetch model count for project {self.name}: {str(e)}")
                self._model_count = 0
        return self._model_count
    
    @property
    def job_count(self) -> int:
        """Get the number of jobs in the project."""
        if self._job_count is None:
            # We don't have a direct API call to count jobs, so we'll use len(self.get_jobs())
            # but we'll try to avoid actually loading all job details
            self._job_count = len(self.get_jobs())
        return self._job_count
    
    @lru_cache(maxsize=32)
    def get_models(self, filter: Optional[SearchFilter] = None) -> List[Model]:
        """
        Get all models in the project.
        
        Args:
            filter: Optional filter to apply to the models.
            
        Returns:
            List of Model objects.
        """
        try:
            # Get models from the model service
            model_objects = self.model_service.get_models_applied(int(self.environment_id))
            
            # Convert to Model objects
            models = []
            for model_obj in model_objects:
                # Extract runtime info from model's execution_info
                last_run_runtime = None
                last_run_status = None
                last_run_start_time = None
                last_run_end_time = None
                
                if hasattr(model_obj, 'execution_info') and model_obj.execution_info:
                    exec_info = model_obj.execution_info
                    
                    # Get runtime info
                    if hasattr(exec_info, 'execution_time'):
                        last_run_runtime = exec_info.execution_time
                    
                    # Get status
                    if hasattr(exec_info, 'last_run_status'):
                        last_run_status = exec_info.last_run_status
                        
                    # Get timing
                    if hasattr(exec_info, 'execute_started_at'):
                        last_run_start_time = exec_info.execute_started_at
                    if hasattr(exec_info, 'execute_completed_at'):
                        last_run_end_time = exec_info.execute_completed_at
                
                # Extract model materialization
                materialization = None
                if hasattr(model_obj, 'materialized_type'):
                    materialization = model_obj.materialized_type
                
                # Create the model object
                model = Model(
                    model_id=f"{self.name}.{model_obj.name}",
                    last_run_runtime=last_run_runtime,
                    last_run_status=last_run_status,
                    last_run_start_time=last_run_start_time,
                    last_run_end_time=last_run_end_time,
                    tags=model_obj.tags,
                    materialization=materialization,
                    description=model_obj.description,
                )
                
                # Set project reference
                model._project = self
                model._unique_id = model_obj.unique_id
                
                models.append(model)
            
            # Apply filter if provided
            if filter:
                filtered_models = []
                for model in models:
                    # Filter by tags
                    if filter.tags and not any(tag in model.tags for tag in filter.tags):
                        continue
                    
                    # Filter by materialization
                    if filter.materialization and model.materialization != filter.materialization:
                        continue
                    
                    # Filter by runtime
                    if filter.min_runtime is not None and (model.last_run_runtime is None or 
                                                          model.last_run_runtime < filter.min_runtime):
                        continue
                    
                    if filter.max_runtime is not None and (model.last_run_runtime is None or 
                                                          model.last_run_runtime > filter.max_runtime):
                        continue
                    
                    filtered_models.append(model)
                
                return filtered_models
            
            return models
            
        except Exception as e:
            logger.error(f"Failed to fetch models for project {self.name}: {str(e)}")
            return []
    
    @lru_cache(maxsize=32)
    def get_jobs(self, filter: Optional[SearchFilter] = None) -> List[Job]:
        """
        Get all jobs in the project.
        
        Args:
            filter: Optional filter to apply to the jobs.
            
        Returns:
            List of Job objects.
        """
        # TODO: Replace with actual implementation to fetch jobs for the project
        # src/service_api/DbtCloudService.py can retrieve this
        # 
        return []
    
    def slowest_models(self, slowest_n: int = 5, last_n_runs: int = 1, filter: Optional[SearchFilter] = None) -> List[Model]:
        """
        Find the slowest models in the project.
        
        Args:
            slowest_n: Number of slowest models to return.
            last_n_runs: Number of runs to consider when calculating average runtime.
            filter: Optional filter to apply to the models.
            
        Returns:
            List of Model objects, sorted by runtime (slowest first).
        """
        # Get all models with the filter
        all_models = self.get_models(filter=filter)
        
        # For models with runtime info, sort by runtime
        models_with_runtime = [m for m in all_models if m.last_run_runtime is not None]
        
        # If we need to consider multiple runs, we need to fetch historical data
        if last_n_runs > 1:
            # For each model, get historical runs and calculate average runtime
            for model in models_with_runtime:
                # Fetch historical runs
                historical_runs = model.get_runs(last_n=last_n_runs)
                
                # Calculate average runtime if we have runs
                if historical_runs:
                    avg_runtime = sum(run.runtime for run in historical_runs if run.runtime) / len(historical_runs)
                    model.last_run_runtime = avg_runtime
            
        # Sort by last_run_runtime (descending) and take the slowest N
        return sorted(models_with_runtime, key=lambda m: m.last_run_runtime or 0, reverse=True)[:slowest_n]
    
    def longest_running_jobs(self, longest_n: int = 5, last_n_runs: int = 1, 
                           filter: Optional[SearchFilter] = None, 
                           model_filter: Optional[ModelFilter] = None) -> List[Job]:
        """
        Find the longest running jobs in the project.
        
        Args:
            longest_n: Number of longest running jobs to return.
            last_n_runs: Number of runs to consider when calculating average runtime.
            filter: Optional filter to apply to the jobs.
            model_filter: Optional filter to apply to the models in the jobs.
            
        Returns:
            List of Job objects, sorted by runtime (longest first).
        """
        # Get all jobs with the filter
        all_jobs = self.get_jobs(filter=filter)
        
        # For jobs with runtime info, sort by runtime
        jobs_with_runtime = [j for j in all_jobs if j.last_run_runtime is not None]
        
        # If model filter is provided, further filter jobs by their models
        if model_filter:
            filtered_jobs = []
            for job in jobs_with_runtime:
                job_models = job.get_models(filter=model_filter)
                if job_models:  # Only include job if it has models matching the filter
                    filtered_jobs.append(job)
            jobs_with_runtime = filtered_jobs
            
        # If we need to consider multiple runs, calculate average runtime
        if last_n_runs > 1:
            for job in jobs_with_runtime:
                avg_runtime = job.get_average_job_runtime(last_n=last_n_runs)
                if avg_runtime is not None:
                    job.last_run_runtime = avg_runtime
            
        # Sort by last_run_runtime (descending) and take the longest N
        return sorted(jobs_with_runtime, key=lambda j: j.last_run_runtime or 0, reverse=True)[:longest_n]#