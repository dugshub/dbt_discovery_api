from datetime import datetime
from pydantic import BaseModel

class BaseResource(BaseModel):
    """Base fields for all API resources"""
    id: str
    created_at: datetime
    updated_at: datetime
