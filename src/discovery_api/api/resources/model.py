"""Model implementation for the discovery API."""

from typing import List, Optional, Dict, Any, TYPE_CHECKING
import logging
from datetime import datetime
from functools import lru_cache

from src.discovery_api.models.base import RunStatus
from src.discovery_api.models.filters import SearchFilter
from src.discovery_api.api.resources.run import Run
from src.discovery_api.api.resources.base import BaseResource

if TYPE_CHECKING:
    from src.discovery_api.api.resources.project import Project
    from src.discovery_api.api.resources.job import Job

logger = logging.getLogger("dbt_discovery_api")


class Model(BaseResource):
    """
    Represents a dbt model.
    
    Provides methods to fetch model information, historical runs,
    and access SQL definition.
    """
    
    name: str
    description: str | None = None
    
    def __init__(self, model_id: str, 
                last_run_status: Optional[RunStatus] = None,
                last_run_runtime: Optional[float] = None,
                last_run_start_time: Optional[datetime] = None,
                last_run_end_time: Optional[datetime] = None,
                tags: Optional[List[str]] = None,
                materialization: Optional[str] = None):
        """
        Initialize a Model.
        
        Args:
            model_id: The model ID in the format project_name.model_name.
            last_run_status: Optional status of the last run.
            last_run_runtime: Optional runtime of the last run.
            last_run_start_time: Optional start time of the last run.
            last_run_end_time: Optional end time of the last run.
            tags: Optional list of tags.
            materialization: Optional materialization type.
        """
        self.model_id = model_id
        self.last_run_status = last_run_status
        self.last_run_runtime = last_run_runtime
        self.last_run_start_time = last_run_start_time
        self.last_run_end_time = last_run_end_time
        self.tags = tags or []
        self.materialization = materialization
        
        # Split model_id into project_name and model_name
        parts = model_id.split('.')
        self.project_name = parts[0]
        self.model_name = parts[1]
        
        # Internal properties
        self._project: Optional['Project'] = None
        self._unique_id: Optional[str] = None
    
    def get_last_run(self) -> Optional[Run]:
        """
        Get the last run for this model.
        
        Returns:
            Run object or None if no run found.
        """
        # Get the most recent run from historical runs
        runs = self.get_runs(last_n=1)
        
        if runs:
            return runs[0]
        
        return None
    
    @lru_cache(maxsize=32)
    def get_runs(self, last_n: int = 5, filter: Optional[SearchFilter] = None) -> List[Run]:
        """
        Get historical runs for this model.
        
        Args:
            last_n: Number of recent runs to return.
            filter: Optional filter to apply to the runs.
            
        Returns:
            List of Run objects.
        """
        if not self._project:
            logger.warning(f"Project reference not set for model {self.model_id}. Cannot get runs.")
            return []
            
        try:
            # Get model service from project
            model_service = self._project.model_service
            
            # Fetch historical runs
            historical_runs = model_service.get_model_historical_runs(
                environment_id=int(self._project.environment_id),
                model_name=self.model_name,
                last_run_count=last_n
            )
            
            # Convert to Run objects
            runs = []
            for run_data in historical_runs:
                # Extract run information
                run_id = str(run_data.get('run_id'))
                job_id = str(run_data.get('job_id'))
                status = RunStatus(run_data.get('status', 'failure').lower())
                runtime = float(run_data.get('execution_time', 0))
                
                # Extract timing information
                start_time = None
                end_time = None
                if 'execute_started_at' in run_data:
                    start_time = run_data.get('execute_started_at')
                if 'execute_completed_at' in run_data:
                    end_time = run_data.get('execute_completed_at')
                
                # Create Run object
                run = Run(
                    run_id=run_id,
                    job_id=job_id,
                    status=status,
                    runtime=runtime,
                    start_time=start_time,
                    end_time=end_time,
                    model_count=1  # Single model run
                )
                
                runs.append(run)
            
            # Apply filter if provided
            if filter:
                filtered_runs = []
                for run in runs:
                    # Filter by runtime
                    if filter.min_runtime is not None and run.runtime < filter.min_runtime:
                        continue
                    
                    if filter.max_runtime is not None and run.runtime > filter.max_runtime:
                        continue
                    
                    filtered_runs.append(run)
                
                return filtered_runs
            
            return runs
            
        except Exception as e:
            logger.error(f"Failed to fetch runs for model {self.model_id}: {str(e)}")
            return []
    
    def get_sql(self) -> str:
        """
        Get the SQL definition for this model.
        
        Returns:
            SQL definition as a string.
        """
        if not self._project or not self._unique_id:
            logger.warning(f"Project reference or unique_id not set for model {self.model_id}. Cannot get SQL.")
            return ""
            
        try:
            # Get model service from project
            model_service = self._project.model_service
            
            # Fetch model by unique ID to get SQL
            model_data = model_service.get_model_by_unique_id(
                environment_id=int(self._project.environment_id),
                unique_id=self._unique_id
            )
            
            # Extract SQL from model data
            sql = model_data.get('raw_sql', '')
            
            return sql
            
        except Exception as e:
            logger.error(f"Failed to fetch SQL for model {self.model_id}: {str(e)}")
            return ""
    
    def freshness(self) -> Optional[RunStatus]:
        """
        Get the freshness status of this model.
        
        Returns:
            RunStatus enum value or None if not available.
        """
        # Freshness is just the last run status
        return self.last_run_status
    
    @lru_cache(maxsize=32)
    def get_jobs(self) -> List['Job']:
        """
        Get all jobs that include this model.
        
        Returns:
            List of Job objects.
        """
        if not self._project:
            logger.warning(f"Project reference not set for model {self.model_id}. Cannot get jobs.")
            return []
            
        try:
            # Get all jobs in the project
            all_jobs = self._project.get_jobs()
            
            # Filter to jobs that include this model
            jobs_with_model = []
            for job in all_jobs:
                job_models = job.get_models()
                model_ids = [m.model_id for m in job_models]
                
                if self.model_id in model_ids:
                    jobs_with_model.append(job)
            
            return jobs_with_model
            
        except Exception as e:
            logger.error(f"Failed to fetch jobs for model {self.model_id}: {str(e)}")
            return []