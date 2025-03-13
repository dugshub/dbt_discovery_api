"""Resource models for the discovery API."""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, computed_field, Field

from src.discovery_api.models.base import RunStatus


class Run(BaseModel):
    """Represents a dbt run."""
    
    run_id: str
    status: RunStatus
    runtime: float
    model_count: int
    start_time: datetime
    end_time: datetime
    job_id: str
    
    @property
    def job(self) -> 'Job':
        """Get the job that this run belongs to."""
        from src.discovery_api.api.resources.job import Job
        return Job(job_id=self.job_id)


class Model(BaseModel):
    """Represents a dbt model."""
    
    model_id: str  # This is project_name.model_name
    last_run_status: Optional[RunStatus] = None
    last_run_runtime: Optional[float] = None
    last_run_start_time: Optional[datetime] = None
    last_run_end_time: Optional[datetime] = None
    tags: List[str] = Field(default_factory=list)
    materialization: Optional[str] = None
    description: Optional[str] = None

    @computed_field
    def project_name(self) -> str:
        """Get the project name from the model_id."""
        return self.model_id.split('.')[0]
    
    @computed_field
    def model_name(self) -> str:
        """Get the model name from the model_id."""
        return self.model_id.split('.')[1]


class Job(BaseModel):
    """Represents a dbt job."""
    
    job_id: str
    last_run_status: Optional[RunStatus] = None
    last_run_runtime: Optional[float] = None
    last_run_start_time: Optional[datetime] = None
    last_run_end_time: Optional[datetime] = None
    environment_id: Optional[str] = None
    name: Optional[str] = None


class Project(BaseModel):
    """Represents a dbt project."""
    
    environment_id: str
    models: Optional[List[Model]] = None
    jobs: Optional[List[Job]] = None
    model_count: Optional[int] = None
    job_count: Optional[int] = None
    name: Optional[str] = None