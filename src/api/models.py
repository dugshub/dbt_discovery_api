"""
Models for the API layer of the DBT Discovery API.

These models represent the user-facing data structures that are returned by API methods.
They are separate from the service-layer models (src/models.py) that interact with the GraphQL API.
"""

from typing import List, Dict, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field, computed_field


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
    
    model_config = {
        "from_attributes": True  # Enable conversion from objects (was orm_mode in v1)
    }


class RunStatus(BaseModel):
    """Run status information"""
    status: Optional[str] = None  # success, error, running
    run_id: Optional[str] = None
    run_time: Optional[datetime] = Field(default=None, alias="run_generated_at")
    execution_time: Optional[float] = None
    error_message: Optional[str] = Field(default=None, alias="error")
    
    model_config = {
        "from_attributes": True  # Enable conversion from objects (was orm_mode in v1)
    }


class ProjectMetadata(BaseModel):
    """Project metadata information"""
    dbt_project_name: str
    adapter_type: str
    environment_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = {
        "from_attributes": True  # Enable conversion from objects (was orm_mode in v1)
    }


# Runtime metrics models
class ModelRuntimeMetrics(BaseModel):
    """Runtime metrics for a model."""
    most_recent_run: Optional[RunStatus] = None
    execution_info: Dict[str, Any] = Field(default_factory=dict)
    
    model_config = {
        "from_attributes": True
    }


class ModelWithRuntime(BaseModel):
    """Model with its runtime metrics."""
    name: str
    unique_id: str
    metadata: ModelMetadata
    runtime_metrics: ModelRuntimeMetrics
    
    model_config = {
        "from_attributes": True
    }
    
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