"""
Models for the API layer of the DBT Discovery API.

These models represent the user-facing data structures that are returned by API methods.
They are separate from the service-layer models (src/models.py) that interact with the GraphQL API.
"""

from typing import List, Dict, Optional, Any, ClassVar
from datetime import datetime
from pydantic import BaseModel, Field, computed_field, ConfigDict


# Common API models
class ModelMetadata(BaseModel):
    """Model metadata information"""
    name: str
    unique_id: str
    database: Optional[str] = None
    schema: Optional[str] = Field(default=None, alias="db_schema")  # Use alias to avoid conflict with BaseModel.schema
    description: Optional[str] = None
    materialized: Optional[str] = Field(default=None, alias="materialized_type")
    tags: List[str] = Field(default_factory=list)
    
    # Using the correct syntax for Pydantic v2 model_config
    model_config: ClassVar = ConfigDict(from_attributes=True)  # type: ignore


class RunStatus(BaseModel):
    """Run status information"""
    status: Optional[str] = None  # success, error, running
    run_id: Optional[str] = None
    run_time: Optional[datetime] = Field(default=None, alias="run_generated_at")
    execution_time: Optional[float] = None
    error_message: Optional[str] = Field(default=None, alias="error")
    
    # Using the correct syntax for Pydantic v2 model_config
    model_config: ClassVar = ConfigDict(from_attributes=True)  # type: ignore


class ProjectMetadata(BaseModel):
    """Project metadata information"""
    dbt_project_name: str
    adapter_type: str
    environment_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # Using the correct syntax for Pydantic v2 model_config
    model_config: ClassVar = ConfigDict(from_attributes=True)  # type: ignore


# Runtime metrics models
class ModelRuntimeMetrics(BaseModel):
    """Runtime metrics for a model."""
    most_recent_run: Optional[RunStatus] = None
    execution_info: Dict[str, Any] = Field(default_factory=dict)
    
    # Using the correct syntax for Pydantic v2 model_config
    model_config: ClassVar = ConfigDict(from_attributes=True)  # type: ignore


class ModelWithRuntime(BaseModel):
    """Model with its runtime metrics."""
    name: str
    unique_id: str
    metadata: ModelMetadata
    runtime_metrics: ModelRuntimeMetrics
    
    # Using the correct syntax for Pydantic v2 model_config
    model_config: ClassVar = ConfigDict(from_attributes=True)  # type: ignore
    
    @computed_field
    def execution_time(self) -> Optional[float]:
        """Direct access to execution time from execution_info."""
        if self.runtime_metrics.execution_info:
            return self.runtime_metrics.execution_info.get('execution_time')
        return None
    
    @computed_field
    def most_recent_run(self) -> Optional[Dict[str, Any]]:
        """Direct access to most recent run for convenience."""
        if self.runtime_metrics.most_recent_run:
            return self.runtime_metrics.most_recent_run.model_dump()
        return None
        
    @computed_field
    def last_run_status(self) -> Optional[str]:
        """Direct access to last run status from execution_info."""
        if self.runtime_metrics.execution_info:
            return self.runtime_metrics.execution_info.get('last_run_status')
        return None