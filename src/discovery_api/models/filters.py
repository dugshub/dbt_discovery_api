"""Filter models for the discovery API."""

from typing import Optional, List, Union
from pydantic import BaseModel, Field


class SearchFilter(BaseModel):
    """
    Base search filter for models and runs.
    
    When used to fetch models, this filters the models by these properties.
    When used to fetch jobs/runs it filters the run for the models that match these properties.
    Jobs/runs don't have tags so this lets us get "all jobs/runs that contain models tagged 
    with marketing, for example"
    """
    
    tags: Optional[List[str]] = None
    materialization: Optional[str] = None
    min_runtime: Optional[float] = None
    max_runtime: Optional[float] = None


class ModelFilter(SearchFilter):
    """Filter for models, extends SearchFilter with model-specific filters."""
    
    models: Optional[List['Model']] = None  # Model objects
    model_ids: Optional[List[str]] = None  # project_name.model_name


class ProjectFilter(SearchFilter):
    """Filter for projects, extends SearchFilter with project-specific filters."""
    
    projects: Optional[List['Project']] = None
    environment_ids: Optional[List[str]] = None
    include_or_exclude: Optional[str] = Field(default="include", pattern="^(include|exclude)$")


# Update forward references
from src.discovery_api.models.resources import Model, Project  # noqa
ModelFilter.model_config["populate_by_name"] = True
ProjectFilter.model_config["populate_by_name"] = True