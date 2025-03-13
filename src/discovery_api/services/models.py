"""Models for the discovery API."""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel

from src.discovery_api.models.base import RunStatus

class ModelDefinition(BaseModel):
    """Represents a model in the definition state."""
    
    name: str
    unique_id: str
    description: Optional[str] = None
    tags: List[str] = []
    meta: Dict[str, Any] = {}
    file_path: Optional[str] = None
    resource_type: Optional[str] = None
    run_generated_at: Optional[datetime] = None
    project_id: Optional[str] = None
    environment_id: Optional[str] = None
    account_id: Optional[str] = None
    database: Optional[str] = None
    schema: Optional[str] = None
    alias: Optional[str] = None
    materialized_type: Optional[str] = None
    fqn: Optional[List[str]] = None
    package_name: Optional[str] = None
    contract_enforced: Optional[bool] = None
    language: Optional[str] = None
    group: Optional[str] = None
    raw_code: Optional[str] = None

class ModelHistoricalRun(BaseModel):
    """Represents a historical run of a model."""
    
    name: str
    alias: Optional[str] = None
    description: Optional[str] = None
    resource_type: str
    tags: List[str] = []
    meta: Dict[str, Any] = {}
    run_id: Optional[str] = None
    invocation_id: Optional[str] = None
    job_id: Optional[str] = None
    thread_id: Optional[str] = None
    run_generated_at: Optional[datetime] = None
    compile_started_at: Optional[datetime] = None
    compile_completed_at: Optional[datetime] = None
    execute_started_at: Optional[datetime] = None
    execute_completed_at: Optional[datetime] = None
    execution_time: Optional[float] = None
    run_elapsed_time: Optional[float] = None
    status: Optional[RunStatus] = None
    error: Optional[str] = None
    skip: Optional[bool] = None
    raw_sql: Optional[str] = None
    compiled_sql: Optional[str] = None
    raw_code: Optional[str] = None
    compiled_code: Optional[str] = None
    language: Optional[str] = None
    database: Optional[str] = None
    schema: Optional[str] = None
    depends_on: Optional[List[str]] = None
    parents_models: Optional[List[str]] = None
    parents_sources: Optional[List[str]] = None
    environment_id: Optional[str] = None
    project_id: Optional[str] = None
    account_id: Optional[str] = None
    owner: Optional[str] = None