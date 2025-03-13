# In src/discovery_api/models/__init__.py
"""Model exports for the discovery API."""

# Remove service-layer imports
from src.discovery_api.models.filters import SearchFilter, ModelFilter, ProjectFilter
from src.discovery_api.models.resources import Model, Job, Project, Run
from src.discovery_api.models.base import RunStatus, RuntimeReport  # Direct base import

__all__ = [
    # Base models
    'RunStatus',
    'RuntimeReport',
    
    # Filter models
    'SearchFilter',
    'ModelFilter',
    'ProjectFilter',
    
    # Resource models
    'Model',
    'Job',
    'Project',
    'Run'
]