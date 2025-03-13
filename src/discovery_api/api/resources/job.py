"""Job implementation for the discovery API."""

from typing import List, Optional
from datetime import datetime
from functools import lru_cache

from src.discovery_api.services.JobService import JobService
from src.discovery_api.services.ModelService import ModelService
from src.discovery_api.models.base import RunStatus, RuntimeReport
from src.discovery_api.models.filters import SearchFilter, ModelFilter
from src.discovery_api.api.resources.model import Model
from src.discovery_api.api.resources.run import Run


class Job:
    """
    Represents a dbt job in dbt Cloud.
    
    A job is a scheduled or manually triggered execution of dbt commands.
    It provides methods to query model and run information for the job.
    """
    
    def __init__(self, job_id: str, environment_id: Optional[str] = None,
                 name: Optional[str] = None):
        """
        Initialize a Job.
        
        Args:
            job_id: The job ID in dbt Cloud.
            environment_id: Optional environment ID the job belongs to.
            name: Optional job name.
        """
        self.job_id = job_id
        self.environment_id = environment_id
        self.name = name
        
        # Initialize services
        self.job_service = JobService()
        self.model_service = ModelService()
        
        # Lazy-loaded properties
        self._last_run: Optional[Run] = None
    
    @property
    def last_run_status(self) -> Optional[RunStatus]:
        """Get the status of the last run."""
        if self._last_run is None:
            self._last_run = self.get_last_run()
        return self._last_run.status if self._last_run else None
    
    @property
    def last_run_runtime(self) -> Optional[float]:
        """Get the runtime of the last run."""
        if self._last_run is None:
            self._last_run = self.get_last_run()
        return self._last_run.runtime if self._last_run else None
    
    @property
    def last_run_start_time(self) -> Optional[datetime]:
        """Get the start time of the last run."""
        if self._last_run is None:
            self._last_run = self.get_last_run()
        return self._last_run.start_time if self._last_run else None
    
    @property
    def last_run_end_time(self) -> Optional[datetime]:
        """Get the end time of the last run."""
        if self._last_run is None:
            self._last_run = self.get_last_run()
        return self._last_run.end_time if self._last_run else None
    
    @lru_cache(maxsize=32)
    def get_models(self, filter: Optional[SearchFilter] = None) -> List[Model]:
        """
        Get all models in the job.
        
        Args:
            filter: Optional filter to apply to the models.
            
        Returns:
            List of Model objects.
        """
        try:
            # Get models from the job service
            models_data = self.job_service.get_job_models(job_id=int(self.job_id))
            
            if not models_data:
                return []
            
            # Convert to Model objects
            models = []
            for model_data in models_data.get('models', []):
                # Create model object
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
    
    def get_last_run(self) -> Optional[Run]:
        """Get the most recent run of the job."""
        try:
            runs = self.get_runs(last_n=1)
            return runs[0] if runs else None
        except Exception:
            return None
    
    @lru_cache(maxsize=32)
    def get_runs(self, last_n: int = 5) -> List[Run]:
        """
        Get recent runs of the job.
        
        Args:
            last_n: Number of recent runs to return.
            
        Returns:
            List of Run objects, sorted by start time (most recent first).
        """
        try:
            # Get runs from the job service
            runs_data = self.job_service.get_job_runs(job_id=int(self.job_id), limit=last_n)
            
            if not runs_data:
                return []
            
            # Convert to Run objects
            runs = []
            for run_data in runs_data:
                run = Run(
                    run_id=str(run_data.get('id')),
                    status=run_data.get('status'),
                    runtime=run_data.get('runtime'),
                    model_count=run_data.get('total_models', 0),
                    start_time=run_data.get('started_at'),
                    end_time=run_data.get('finished_at'),
                    job_id=self.job_id
                )
                runs.append(run)
            
            # Sort by start_time (descending)
            return sorted(runs, key=lambda r: r.start_time, reverse=True)
            
        except Exception as e:
            return []
    
    def get_slowest_models(self, slowest_n: int = 5, filter: Optional[SearchFilter] = None) -> List[Model]:
        """
        Get the slowest models in the job.
        
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
    
    def get_runtimes(self, last_n: int = 5, by_model: bool = False) -> List[RuntimeReport]:
        """
        Get runtime reports for the job.
        
        Args:
            last_n: Number of recent runs to analyze.
            by_model: If True, returns runtimes for each model in the job.
            
        Returns:
            List of RuntimeReport objects.
        """
        reports = []
        
        # Get recent runs
        runs = self.get_runs(last_n=last_n)
        
        for run in runs:
            if by_model:
                # Get models from this run
                run_models = run.get_models()
                
                # Create runtime report for each model
                for model in run_models:
                    report = RuntimeReport(
                        job_id=self.job_id,
                        run_id=run.run_id,
                        model_id=model.model_id,
                        runtime=model.last_run_runtime or 0,
                        start_time=model.last_run_start_time or run.start_time,
                        end_time=model.last_run_end_time or run.end_time
                    )
                    reports.append(report)
            else:
                # Create runtime report for the whole run
                report = RuntimeReport(
                    job_id=self.job_id,
                    run_id=run.run_id,
                    runtime=run.runtime or 0,
                    start_time=run.start_time,
                    end_time=run.end_time
                )
                reports.append(report)
        
        return reports
    
    def get_average_job_runtime(self, last_n: int = 5, filter: Optional[SearchFilter] = None,
                              model_filter: Optional[ModelFilter] = None) -> Optional[float]:
        """
        Calculate the average runtime for the job.
        
        Args:
            last_n: Number of recent runs to analyze.
            filter: Optional filter to apply to the job.
            model_filter: Optional filter to apply to models in the job.
            
        Returns:
            Average runtime in seconds, or None if no valid runs found.
        """
        # Get recent runs
        runs = self.get_runs(last_n=last_n)
        
        if not runs:
            return None
        
        # If we have model filters, we need to check models in each run
        if model_filter:
            filtered_runtimes = []
            
            for run in runs:
                # Get models for this run that match the filter
                filtered_models = run.get_models(filter=model_filter)
                
                if filtered_models:
                    filtered_runtimes.append(run.runtime or 0)
            
            # Calculate average of filtered runs
            if filtered_runtimes:
                return sum(filtered_runtimes) / len(filtered_runtimes)
            return None
        
        # Without model filters, just average run times
        valid_runs = [r for r in runs if r.runtime is not None]
        if valid_runs:
            return sum(r.runtime for r in valid_runs) / len(valid_runs)
        return None
    
    def average_historical_model_runtime(self, slowest_n: int = 5, last_n_runs: int = 5,
                                       filter: Optional[SearchFilter] = None,
                                       model_filter: Optional[ModelFilter] = None) -> float:
        """
        Calculate the average runtime for models over their historical runs.
        
        Args:
            slowest_n: Number of slowest models to consider.
            last_n_runs: Number of historical runs to analyze per model.
            filter: Optional filter to apply to models.
            model_filter: Optional additional model filter.
            
        Returns:
            Average runtime in seconds for the slowest N models.
        """
        # Get all models
        all_models = self.get_models(filter=filter)
        
        # Apply model filter if provided
        if model_filter:
            all_models = [m for m in all_models if (
                (not model_filter.models or m in model_filter.models) and
                (not model_filter.model_ids or m.model_id in model_filter.model_ids)
            )]
        
        # Calculate average runtime for each model
        model_averages = []
        for model in all_models:
            # Get historical runs for this model
            model_runs = model.get_runs(last_n=last_n_runs)
            
            if model_runs:
                # Calculate average runtime
                avg_runtime = sum(r.runtime or 0 for r in model_runs) / len(model_runs)
                model_averages.append((model, avg_runtime))
        
        # Sort by average runtime and get slowest N
        model_averages.sort(key=lambda x: x[1], reverse=True)
        slowest_averages = model_averages[:slowest_n]
        
        # Calculate overall average of the slowest N models
        if slowest_averages:
            return sum(avg for _, avg in slowest_averages) / len(slowest_averages)
        return 0.0