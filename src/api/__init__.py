"""
DBT Discovery API Layer - User-friendly interface to the dbt Cloud API.

Provides intuitive access to dbt Cloud resources without the complexity of GraphQL.
"""

from src.api.models import (
    # Common models
    ModelMetadata,
    RunStatus,
    ProjectMetadata,
    
    # Runtime models
    ModelRuntimeMetrics,
    ModelWithRuntime,
)

from src.api.api import (
    # API Classes
    Model,
    Project,
    DiscoveryAPI,
)

__all__ = [
    # Common models
    'ModelMetadata',
    'RunStatus',
    'ProjectMetadata',
    
    # Runtime models
    'ModelRuntimeMetrics',
    'ModelWithRuntime',
    
    # API Classes
    'Model',
    'Project',
    'DiscoveryAPI',
]