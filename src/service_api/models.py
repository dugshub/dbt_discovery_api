"""
Models for the dbt Cloud API Service.

These models represent the data structures returned by the dbt Cloud API.
"""

import json
from typing import Dict, List, Optional, Any, ClassVar
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder that can handle datetime objects.
    
    Used for serializing models with datetime fields to JSON.
    """
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


class JsonMixin:
    """Mixin that provides JSON serialization functionality."""
    
    def to_json(self, indent: int = 2) -> str:
        """Convert the model to a JSON string, handling datetime objects.
        
        Args:
            indent: Number of spaces for indentation (default: 2)
            
        Returns:
            JSON string representation of the model
        """
        if hasattr(self, "model_dump"):
            return json.dumps(self.model_dump(), indent=indent, cls=DateTimeEncoder)
        return json.dumps(self, indent=indent, cls=DateTimeEncoder)


class DbtJobSchedule(BaseModel, JsonMixin):
    """Schedule information for a dbt Cloud job."""
    date: Dict[str, Any] = Field(default_factory=dict)
    time: Dict[str, Any] = Field(default_factory=dict)
    cron: Optional[str] = None
    
    model_config: ClassVar = ConfigDict(from_attributes=True)  # type: ignore


class DbtJobTriggers(BaseModel, JsonMixin):
    """Trigger configuration for a dbt Cloud job."""
    github_webhook: bool = False
    schedule: bool = False
    git_provider_webhook: bool = False
    on_merge: bool = False
    
    model_config: ClassVar = ConfigDict(from_attributes=True)  # type: ignore


class DbtJobSettings(BaseModel, JsonMixin):
    """Settings for a dbt Cloud job."""
    threads: int = 1
    target_name: str = "default"
    
    model_config: ClassVar = ConfigDict(from_attributes=True)  # type: ignore


class DbtJob(BaseModel, JsonMixin):
    """A dbt Cloud job."""
    id: int
    account_id: int
    project_id: int
    environment_id: int
    name: str
    description: Optional[str] = None
    execute_steps: List[str] = Field(default_factory=list)
    job_type: str
    compare_changes_flags: Optional[str] = None
    settings: DbtJobSettings
    state: int
    triggers_on_draft_pr: bool = False
    triggers: DbtJobTriggers
    job_completion_trigger_condition: Optional[Any] = None
    created_at: datetime
    updated_at: datetime
    account: Optional[Any] = None
    project: Optional[Any] = None
    environment: Optional[Any] = None
    most_recent_run: Optional[Any] = None
    most_recent_completed_run: Optional[Any] = None
    schedule: Optional[DbtJobSchedule] = None
    generate_sources: bool = False
    cron_humanized: Optional[str] = None
    next_run_humanized: Optional[str] = None
    next_run: Optional[datetime] = None
    
    model_config: ClassVar = ConfigDict(from_attributes=True)  # type: ignore


class DbtAccountInfo(BaseModel, JsonMixin):
    """Information about a dbt Cloud account."""
    id: int
    name: str
    state: int
    
    model_config: ClassVar = ConfigDict(from_attributes=True)  # type: ignore


class DbtJobsResponse(BaseModel, JsonMixin):
    """Response from the dbt Cloud jobs API."""
    data: List[DbtJob]
    status: Optional[Dict[str, Any]] = None
    
    model_config: ClassVar = ConfigDict(from_attributes=True)  # type: ignore


class DbtAccountResponse(BaseModel, JsonMixin):
    """Response from the dbt Cloud account API."""
    data: DbtAccountInfo
    status: Optional[Dict[str, Any]] = None
    
    model_config: ClassVar = ConfigDict(from_attributes=True)  # type: ignore