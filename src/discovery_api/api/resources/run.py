"""Run implementation for the discovery API."""

from typing import List, Optional
from datetime import datetime
from functools import lru_cache

from src.discovery_api.services.JobService import JobService
from src.discovery_api.services.ModelService import ModelService
from src.discovery_api.models.base import RunStatus
from src.discovery_api.models.filters import SearchFilter, ModelFilter
from src.discovery_api.api.resources.model import Model


class Run:
    """
    Represents a dbt run.
    
    A run is a single execution of a dbt job. It contains information about
    the execution status, timing, and associated models.
    """
    
    def __init__(self, run_id: str, status: Optional[str] = None,
                 runtime: Optional[float] = None, model_count: Optional[int] = None,
                 start_time: Optional[datetime] = None, end_time: Optional[datetime] = None,
                 job_id: Optional[str] = None):
        """
        Initialize a Run.
        
        Args:
            run_id: The run ID in dbt Cloud.
            status: Optional run status.
            runtime: Optional total runtime in seconds.
            model_count: Optional number of models in the run.
            start_time: Optional run start time.
            end_time: Optional run end time.
            job_id: Optional ID of the job this run belongs to.
        """
        self.run_id = run_id
        self.status = RunStatus(status.lower()) if status else None
        self.runtime = runtime
        self.model_count = model_count
        self.start_time = start_time
        self.end_time = end_time
        self.job_id = job_id
        
        # Initialize services
        self.job_service = JobService()
        self.model_service = ModelService()
        
        # Lazy-loaded properties
        self._models: Optional[List[Model]] = None
    
    @property
    def job(self) -> 'Job':
        """Get the job this run belongs to."""
        from src.discovery_api.api.resources.job import Job
        return Job(job_id=self.job_id)
    
    @lru_cache(maxsize=32)
    def get_models(self, filter: Optional[SearchFilter] = None) -> List[Model]:
        """
        Get all models in this run.
        
        Args:
            filter: Optional filter to apply to the models.
            
        Returns:
            List of Model objects.
        """
        try:
            # Get models from the run (using job service since run is part of a job)
            models_data = self.job_service.get_run_models(run_id=int(self.run_id))
            
            if not models_data:
                return []
            
            # Convert to Model objects
            models = []
            for model_data in models_data.get('models', []):
                # Create model object with run-specific data
                model = Model(
                    model_id=model_data.get('unique_id', '').split('.')[-1],
                    last_run_runtime=model_data.get('execution_time'),
                    last_run_status=model_data.get('status'),
                    last_run_start_time=model_data.get('execute_started_at'),
                    last_run_end_time=model_data.get('execute_completed_at'),
                    tags=model_data.get('tags', []),
                    materialization=model_data.get('materialized'),
                    description=model_data.get('description'),
                )
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
            return []
    
    def get_slowest_models(self, slowest_n: int = 5, filter: Optional[SearchFilter] = None) -> List[Model]:
        """
        Get the slowest models in this run.
        
        Args:
            slowest_n: Number of slowest models to return.
            filter: Optional filter to apply to the models.
            
        Returns:
            List of Model objects, sorted by runtime (slowest first).
        """
        # Get all models with the filter
        all_models = self.get_models(filter=filter)
        
        # For models with runtime info, sort by runtime
        models_with_runtime = [m for m in all_models if m.last_run_runtime is not None]
        
        # Sort by last_run_runtime (descending) and take the slowest N
        return sorted(models_with_runtime, key=lambda m: m.last_run_runtime or 0, reverse=True)[:slowest_n]
    
    def average_model_runtime(self, slowest_n: int = 5, filter: Optional[SearchFilter] = None,
                            model_filter: Optional[ModelFilter] = None) -> float:
        """
        Calculate the average runtime for models in this run.
        
        Args:
            slowest_n: Number of slowest models to consider.
            filter: Optional filter to apply to models.
            model_filter: Optional additional model filter.
            
        Returns:
            Average runtime in seconds for the slowest N models.
        """
        # Get models with any base filters
        all_models = self.get_models(filter=filter)
        
        # Apply model filter if provided
        if model_filter:
            all_models = [m for m in all_models if (
                (not model_filter.models or m in model_filter.models) and
                (not model_filter.model_ids or m.model_id in model_filter.model_ids)
            )]
        
        # Get models with runtime info
        models_with_runtime = [m for m in all_models if m.last_run_runtime is not None]
        
        # Sort by runtime and get slowest N
        slowest_models = sorted(models_with_runtime, 
                              key=lambda m: m.last_run_runtime or 0, 
                              reverse=True)[:slowest_n]
        
        # Calculate average runtime for the slowest N models
        if slowest_models:
            return sum(m.last_run_runtime or 0 for m in slowest_models) / len(slowest_models)
        return 0.0