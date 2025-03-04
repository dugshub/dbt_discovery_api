from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from pydantic import BaseModel, Field, computed_field


class ModelBase(BaseModel):
    """Base model for all dbt-tools models."""
    
    model_config = {
        "from_attributes": True  # Enable conversion from objects (was orm_mode in v1)
    }


class Model(ModelBase):
    """Represents a model in dbt - Applied State."""
    name: str
    alias: Optional[str] = None
    unique_id: str
    database: Optional[str] = None
    db_schema: Optional[str] = Field(default=None, alias="schema")
    materialized_type: Optional[str] = None
    execution_info: Dict[str, Any] = {}
    tags: List[str] = []
    meta: Dict[str, Any] = {}
    file_path: Optional[str] = None
    description: Optional[str] = None
    contract_enforced: Optional[bool] = None
    language: Optional[str] = None
    fqn: Optional[List[str]] = None
    package_name: Optional[str] = None


class ModelDefinition(ModelBase):
    """Represents a model definition in dbt - Definition State."""
    name: str
    description: Optional[str] = None
    unique_id: str
    resource_type: str
    run_generated_at: Optional[datetime] = None
    project_id: int
    environment_id: int
    account_id: int
    tags: List[str] = []
    meta: Dict[str, Any] = {}
    file_path: str
    database: Optional[str] = None
    db_schema: Optional[str] = Field(default=None, alias="schema")
    alias: Optional[str] = None
    materialized_type: Optional[str] = None
    contract_enforced: Optional[bool] = None
    language: Optional[str] = None
    fqn: Optional[List[str]] = None
    package_name: Optional[str] = None
    group: Optional[str] = None
    raw_code: Optional[str] = None


class ModelHistoricalRun(ModelBase):
    """Represents a historical run of a model."""
    name: str
    alias: Optional[str] = None
    description: Optional[str] = None
    resource_type: str
    tags: List[str] = []
    meta: Dict[str, Any] = {}
    run_id: Optional[str] = None
    invocation_id: Optional[str] = None
    job_id: Optional[int] = None
    thread_id: Optional[str] = None
    run_generated_at: Optional[datetime] = None
    compile_started_at: Optional[datetime] = None
    compile_completed_at: Optional[datetime] = None
    execute_started_at: Optional[datetime] = None
    execute_completed_at: Optional[datetime] = None
    execution_time: Optional[float] = None
    run_elapsed_time: Optional[float] = None
    status: Optional[str] = None
    error: Optional[str] = None
    skip: Optional[bool] = None
    database: Optional[str] = None
    db_schema: Optional[str] = Field(default=None, alias="schema")
    raw_sql: Optional[str] = None
    compiled_sql: Optional[str] = None
    raw_code: Optional[str] = None
    compiled_code: Optional[str] = None
    language: Optional[str] = None
    environment_id: Optional[int] = None
    project_id: Optional[int] = None
    account_id: Optional[int] = None
    owner: Optional[str] = None
    depends_on: Optional[List[str]] = None
    parents_models: Optional[List[Dict[str, Any]]] = None
    parents_sources: Optional[List[Dict[str, Any]]] = None


# Models for runtime metrics
class ModelRuntimeMetrics(BaseModel):
    """Runtime metrics for a model."""
    most_recent_run: Optional[Union['ModelHistoricalRun', Dict[str, Any]]] = None
    execution_info: Dict[str, Any] = Field(default_factory=dict)
    
    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True
    }


class ModelWithRuntime(BaseModel):
    """Model with its runtime metrics."""
    name: str
    unique_id: str
    metadata: Dict[str, Any]
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
        if isinstance(self.runtime_metrics.most_recent_run, BaseModel):
            return self.runtime_metrics.most_recent_run.model_dump()
        return self.runtime_metrics.most_recent_run
        
    @computed_field
    def last_run_status(self) -> Optional[str]:
        """Direct access to last run status from execution_info."""
        if self.runtime_metrics.execution_info:
            return self.runtime_metrics.execution_info.get('last_run_status')
        return None