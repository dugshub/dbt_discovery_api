"""Base models for the discovery API."""

from typing import Optional, List
from datetime import datetime
import enum
from pydantic import BaseModel


class RuntimeReport(BaseModel):
    """Report on the runtime of a model or job."""
    
    job_id: str
    run_id: str
    model_id: Optional[str] = None
    runtime: float
    start_time: datetime
    end_time: datetime


class RunStatus(str, enum.Enum):
    """Status of a run."""
    
    SUCCESS = "success"
    FAILURE = "failure"
    CANCELLED = "cancelled"