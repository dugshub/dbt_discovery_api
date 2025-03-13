"""Tests for filter models."""

import pytest
from src.discovery_api.models.filters import SearchFilter, ModelFilter, ProjectFilter
from src.discovery_api.models.resources import Model, Project

def test_search_filter():
    """Test SearchFilter model."""
    # Test empty filter
    filter = SearchFilter()
    assert filter.tags is None
    assert filter.materialization is None
    assert filter.min_runtime is None
    assert filter.max_runtime is None

    # Test full filter
    filter = SearchFilter(
        tags=["daily", "marketing"],
        materialization="table",
        min_runtime=10.0,
        max_runtime=60.0
    )
    assert filter.tags == ["daily", "marketing"]
    assert filter.materialization == "table"
    assert filter.min_runtime == 10.0
    assert filter.max_runtime == 60.0

    # Test validation
    with pytest.raises(ValueError):
        SearchFilter(min_runtime="not a float")
    
    with pytest.raises(ValueError):
        SearchFilter(tags="not a list")

def test_model_filter():
    """Test ModelFilter model."""
    # Create test models
    model1 = Model(model_id="project1.model1")
    model2 = Model(model_id="project1.model2")

    # Test empty filter
    filter = ModelFilter()
    assert filter.models is None
    assert filter.model_ids is None
    assert filter.tags is None  # Inherited from SearchFilter

    # Test filter with models
    filter = ModelFilter(
        models=[model1, model2],
        model_ids=["project1.model1", "project1.model2"],
        tags=["daily"]
    )
    assert len(filter.models) == 2
    assert filter.model_ids == ["project1.model1", "project1.model2"]
    assert filter.tags == ["daily"]

    # Test validation
    with pytest.raises(ValueError):
        ModelFilter(models="not a list")
    
    with pytest.raises(ValueError):
        ModelFilter(model_ids="not a list")

def test_project_filter():
    """Test ProjectFilter model."""
    # Create test projects
    project1 = Project(environment_id="123")
    project2 = Project(environment_id="456")

    # Test empty filter
    filter = ProjectFilter()
    assert filter.projects is None
    assert filter.environment_ids is None
    assert filter.include_or_exclude == "include"
    assert filter.tags is None  # Inherited from SearchFilter

    # Test filter with projects
    filter = ProjectFilter(
        projects=[project1, project2],
        environment_ids=["123", "456"],
        include_or_exclude="exclude",
        tags=["daily"]
    )
    assert len(filter.projects) == 2
    assert filter.environment_ids == ["123", "456"]
    assert filter.include_or_exclude == "exclude"
    assert filter.tags == ["daily"]

    # Test validation
    with pytest.raises(ValueError):
        ProjectFilter(include_or_exclude="invalid")
    
    with pytest.raises(ValueError):
        ProjectFilter(projects="not a list")
    
    with pytest.raises(ValueError):
        ProjectFilter(environment_ids="not a list")