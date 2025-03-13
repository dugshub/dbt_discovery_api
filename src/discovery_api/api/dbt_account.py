"""dbtAccount implementation for the discovery API."""

import os
import yaml
import logging
from typing import List, Optional, Dict, Any
from functools import lru_cache

from src.discovery_api.services.BaseQuery import BaseQuery
from src.discovery_api.models.filters import SearchFilter, ProjectFilter
from src.discovery_api.api.resources.project import Project
from src.discovery_api.api.resources.model import Model
from src.discovery_api.api.resources.job import Job
from src.discovery_api.api.resources.run import Run
from src.discovery_api.exceptions import AuthenticationError, ResourceNotFoundError


logger = logging.getLogger("dbt_discovery_api")


class dbtAccount:
    """
    Main entry point for the dbt Discovery API.
    
    Provides methods to access projects, jobs, models, and runs across all environments.
    Uses config.yml to map project names to environment IDs.
    """
    
    def __init__(self, token: Optional[str] = None, config_path: Optional[str] = None):
        """
        Initialize a dbtAccount.
        
        Args:
            token: The dbt Cloud API token. If not provided, will look for DBT_SERVICE_TOKEN environment variable.
            config_path: Path to the config.yml file. If not provided, will look in the current directory.
        
        Raises:
            AuthenticationError: If token is not provided and DBT_SERVICE_TOKEN is not set.
            ResourceNotFoundError: If config.yml file is not found.
        """
        # Use provided token or get from environment
        self.token = token or os.environ.get("DBT_SERVICE_TOKEN")
        if not self.token:
            raise AuthenticationError("No API token provided. Set DBT_SERVICE_TOKEN environment variable or pass token to constructor.")
        
        # Load configuration from config.yml
        self.config_path = config_path or os.path.join(os.getcwd(), "config.yml")
        if not os.path.exists(self.config_path):
            raise ResourceNotFoundError(f"Config file not found: {self.config_path}")
        
        try:
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load config file: {str(e)}")
            raise ResourceNotFoundError(f"Failed to load config file: {str(e)}")
        
        # Initialize services
        self.base_query = BaseQuery(token=self.token)
        
        # Lazy-loaded properties
        self._projects: Optional[List[Project]] = None
        self._project_filter: Optional[ProjectFilter] = None
    
    @property
    def projects(self) -> List[Project]:
        """Get all projects in the account."""
        if self._projects is None:
            self._projects = self.get_projects()
        return self._projects
    
    @property
    def filter(self) -> Optional[ProjectFilter]:
        """Get the current project filter."""
        return self._project_filter
    
    @filter.setter
    def filter(self, value: Optional[ProjectFilter]):
        """Set the project filter."""
        self._project_filter = value
        # Clear cached properties when filter changes
        self._projects = None
    
    @lru_cache(maxsize=32)
    def get_projects(self, filter: Optional[ProjectFilter] = None) -> List[Project]:
        """
        Get all projects based on config.yml mappings.
        
        Args:
            filter: Optional filter to apply to the projects.
            
        Returns:
            List of Project objects.
        """
        try:
            # Create Project objects from config
            projects = []
            project_configs = self.config.get('projects', {})
            
            for project_name, project_config in project_configs.items():
                env_id = str(project_config.get('prod_env_id'))
                project_label = project_config.get('label', project_name)
                
                # Create project
                project = Project(environment_id=env_id, 
                                 name=project_name,
                                 base_query=self.base_query)
                projects.append(project)
            
            # Apply filter if provided
            if filter:
                filtered_projects = []
                
                # Check environment_ids filter
                if filter.environment_ids:
                    for project in projects:
                        is_included = (
                            (filter.include_or_exclude == "include" and 
                             project.environment_id in filter.environment_ids) or 
                            (filter.include_or_exclude == "exclude" and 
                             project.environment_id not in filter.environment_ids)
                        )
                        if is_included:
                            filtered_projects.append(project)
                else:
                    filtered_projects = projects
                
                # Apply search filters (tags, materialization, runtime) 
                # These need to check models in each project
                if any([filter.tags, filter.materialization, filter.min_runtime, filter.max_runtime]):
                    projects_with_matching_models = []
                    for project in filtered_projects:
                        models = project.get_models(filter=filter)
                        if models:
                            projects_with_matching_models.append(project)
                    filtered_projects = projects_with_matching_models
                
                return filtered_projects
            
            return projects
            
        except Exception as e:
            logger.error(f"Failed to fetch projects: {str(e)}")
            return []
    
    @lru_cache(maxsize=32)
    def get_jobs(self, filter: Optional[SearchFilter] = None) -> List[Job]:
        """
        Get jobs across all projects.
        
        Args:
            filter: Optional filter to apply to the jobs.
            
        Returns:
            List of Job objects.
        """
        # Get projects (using filter to narrow down if needed)
        projects = self.get_projects(filter=self._project_filter)
        
        # Collect jobs from all projects
        all_jobs = []
        for project in projects:
            jobs = project.get_jobs(filter=filter)
            all_jobs.extend(jobs)
            
        return all_jobs
    
    @lru_cache(maxsize=32)
    def get_models(self, filter: Optional[SearchFilter] = None) -> List[Model]:
        """
        Get models across all projects.
        
        Args:
            filter: Optional filter to apply to the models.
            
        Returns:
            List of Model objects.
        """
        # Get projects (using filter to narrow down if needed)
        projects = self.get_projects(filter=self._project_filter)
        
        # Collect models from all projects
        all_models = []
        for project in projects:
            models = project.get_models(filter=filter)
            all_models.extend(models)
            
        return all_models
    
    @lru_cache(maxsize=32)
    def get_runs(self, limit: int = 10, filter: Optional[SearchFilter] = None) -> List[Run]:
        """
        Get recent runs across all projects.
        
        Args:
            limit: Maximum number of runs to return per project.
            filter: Optional filter to apply to the runs.
            
        Returns:
            List of Run objects, sorted by start time (most recent first).
        """
        # Get jobs (using filter to narrow down if needed)
        jobs = self.get_jobs(filter=filter)
        
        # Collect runs from all jobs
        all_runs = []
        for job in jobs:
            runs = job.get_runs(last_n=limit)
            all_runs.extend(runs)
            
        # Sort by start_time (descending) and limit total
        return sorted(all_runs, key=lambda r: r.start_time, reverse=True)[:limit]
    
    def slowest_models(self, slowest_n: int = 5, last_n_runs: int = 1, 
                      filter: Optional[SearchFilter] = None) -> List[Model]:
        """
        Find the slowest models across all projects.
        
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
        
        # If we need to consider multiple runs, calculate average runtime
        if last_n_runs > 1:
            for model in models_with_runtime:
                # Fetch historical runs
                historical_runs = model.get_runs(last_n=last_n_runs)
                
                # Calculate average runtime if we have runs
                if historical_runs:
                    avg_runtime = sum(run.runtime for run in historical_runs) / len(historical_runs)
                    model.last_run_runtime = avg_runtime
            
        # Sort by last_run_runtime (descending) and take the slowest N
        return sorted(models_with_runtime, key=lambda m: m.last_run_runtime or 0, reverse=True)[:slowest_n]
    
    def longest_running_jobs(self, longest_n: int = 5, last_n_runs: int = 1, 
                           filter: Optional[SearchFilter] = None,
                           model_filter: Optional[SearchFilter] = None) -> List[Job]:
        """
        Find the longest running jobs across all projects.
        
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
        return sorted(jobs_with_runtime, key=lambda j: j.last_run_runtime or 0, reverse=True)[:longest_n]