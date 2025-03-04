"""
DBT Discovery API Layer - User-friendly interface to the dbt Cloud API.

Provides intuitive access to dbt Cloud resources without the complexity of GraphQL.
"""

from src.api.api import (
    # Models
    ModelMetadata,
    RunStatus,
    ProjectMetadata,
    
    # API Classes
    Model,
    Project,
    DiscoveryAPI,
)

__all__ = [
    'ModelMetadata',
    'RunStatus',
    'ProjectMetadata',
    'Model',
    'Project',
    'DiscoveryAPI',
]