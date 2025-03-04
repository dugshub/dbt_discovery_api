"""
Tests for API layer core classes.
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from src.models import Model, ModelHistoricalRun
from src.api import DiscoveryAPI
from src.services.BaseQuery import BaseQuery
from src.services.EnvironmentService import EnvironmentService
from src.services.ModelService import ModelService


@pytest.fixture
def mock_environment_service():
    """Create a mock EnvironmentService."""
    mock = Mock()
    
    # Mock environment metadata
    mock.get_environment_metadata.return_value = {
        "dbt_project_name": "test_project",
        "adapter_type": "snowflake"
    }
    
    return mock


@pytest.fixture
def mock_model_service():
    """Create a mock ModelService."""
    mock = Mock()
    
    # Create test models
    test_models = [
        Model(
            name="model1",
            unique_id="model.test.model1",
            materialized_type="table",
            database="analytics",
            schema="public",  # Use 'schema' field, not 'db_schema'
            description="Test model 1"
        ),
        Model(
            name="model2",
            unique_id="model.test.model2",
            materialized_type="view",
            database="analytics",
            schema="public",  # Use 'schema' field, not 'db_schema'
            description="Test model 2"
        )
    ]
    
    # Create test runs
    now = datetime.now()
    test_runs = [
        ModelHistoricalRun(
            name="model1",
            resource_type="model",  # Required field
            run_id="run1",
            status="success",
            run_generated_at=now,
            execution_time=10.5
        ),
        ModelHistoricalRun(
            name="model1",
            resource_type="model",  # Required field
            run_id="run2",
            status="error",
            run_generated_at=now,
            execution_time=5.2,
            error="Test error"
        )
    ]
    
    # Mock service methods
    mock.get_models_applied.return_value = test_models
    mock.get_model_by_name.side_effect = lambda env_id, name, state: next(
        (m for m in test_models if m.name == name), None
    )
    mock.get_model_historical_runs.return_value = test_runs
    
    return mock


@pytest.fixture
def api_with_mocks(mock_environment_service, mock_model_service):
    """Create a DiscoveryAPI instance with mocked services."""
    with patch('src.api.api.BaseQuery'), \
         patch('src.api.api.EnvironmentService') as mock_env_service_cls, \
         patch('src.api.api.ModelService') as mock_model_service_cls:
        
        # Configure mocks to return our pre-configured service mocks
        mock_env_service_cls.return_value = mock_environment_service
        mock_model_service_cls.return_value = mock_model_service
        
        # Create API instance
        api = DiscoveryAPI(token="test_token")
        
        yield api


@pytest.fixture
def project(api_with_mocks):
    """Create a Project instance using the mocked API."""
    return api_with_mocks.project(environment_id=12345)


def test_api_initialization():
    """Test API initialization with and without token."""
    # Test with explicit token - we only care that the BaseQuery is initialized correctly
    with patch('src.api.api.BaseQuery') as mock_base_query, \
         patch('src.api.api.EnvironmentService'), \
         patch('src.api.api.ModelService'):
        DiscoveryAPI(token="test_token")  # We don't need to store the instance
        mock_base_query.assert_called_once_with("test_token", "https://metadata.cloud.getdbt.com/graphql")
    
    # Test with custom endpoint - we only care that the BaseQuery is initialized correctly
    with patch('src.api.api.BaseQuery') as mock_base_query, \
         patch('src.api.api.EnvironmentService'), \
         patch('src.api.api.ModelService'):
        DiscoveryAPI(token="test_token", endpoint="https://custom-endpoint.com/graphql")  # We don't need to store the instance
        mock_base_query.assert_called_once_with("test_token", "https://custom-endpoint.com/graphql")


def test_api_project_method(api_with_mocks, mock_environment_service):
    """Test the project method of DiscoveryAPI."""
    # Test successful project creation
    project = api_with_mocks.project(environment_id=12345)
    mock_environment_service.get_environment_metadata.assert_called_once_with(12345)
    assert project.environment_id == 12345
    
    # Test project creation with invalid environment ID
    mock_environment_service.get_environment_metadata.side_effect = Exception("Environment not found")
    with pytest.raises(ValueError):
        api_with_mocks.project(environment_id=99999)


def test_project_get_metadata(project, mock_environment_service):
    """Test getting project metadata."""
    metadata = project.get_metadata()
    mock_environment_service.get_environment_metadata.assert_called_with(12345)
    assert metadata.dbt_project_name == "test_project"
    assert metadata.adapter_type == "snowflake"
    assert metadata.environment_id == 12345


def test_project_get_models(project, mock_model_service):
    """Test getting all models in a project."""
    # Test initial call fetches models
    models = project.get_models()
    mock_model_service.get_models_applied.assert_called_once_with(12345)
    assert len(models) == 2
    assert models[0].metadata.name == "model1"
    assert models[1].metadata.name == "model2"
    
    # Test second call uses cache
    mock_model_service.get_models_applied.reset_mock()
    models = project.get_models()
    mock_model_service.get_models_applied.assert_not_called()
    assert len(models) == 2
    
    # Test refresh bypasses cache
    models = project.get_models(refresh=True)
    mock_model_service.get_models_applied.assert_called_once_with(12345)
    assert len(models) == 2


def test_project_get_model(project, mock_model_service):
    """Test getting a specific model."""
    # Test getting an existing model
    model = project.get_model("model1")
    assert model.metadata.name == "model1"
    assert model.metadata.unique_id == "model.test.model1"
    
    # Test error when model doesn't exist
    mock_model_service.get_model_by_name.return_value = None
    with pytest.raises(ValueError):
        project.get_model("nonexistent_model")


def test_project_get_model_historical_runs(project, mock_model_service):
    """Test getting historical runs for a model."""
    runs = project.get_model_historical_runs("model1")
    mock_model_service.get_model_historical_runs.assert_called_once_with(12345, "model1", last_run_count=5)
    assert len(runs) == 2
    assert runs[0].status == "success"
    assert runs[1].status == "error"
    assert runs[1].error_message == "Test error"


def test_model_metadata_property(project):
    """Test the metadata property of Model."""
    model = project.get_model("model1")
    metadata = model.metadata
    
    assert metadata.name == "model1"
    assert metadata.unique_id == "model.test.model1"
    assert metadata.materialized == "table"
    assert metadata.database == "analytics"
    assert metadata.schema == "public"
    assert metadata.description == "Test model 1"


def test_model_last_run_property(project, mock_model_service):
    """Test the last_run property of Model."""
    model = project.get_model("model1")
    last_run = model.last_run
    
    mock_model_service.get_model_historical_runs.assert_called_once_with(12345, "model1", last_run_count=1)
    assert last_run.status == "success"
    assert last_run.run_id == "run1"
    
    # Test caching behavior
    mock_model_service.get_model_historical_runs.reset_mock()
    last_run = model.last_run
    mock_model_service.get_model_historical_runs.assert_not_called()


def test_model_get_historical_runs(project, mock_model_service):
    """Test the get_historical_runs method of Model."""
    model = project.get_model("model1")
    runs = model.get_historical_runs(limit=10)
    
    mock_model_service.get_model_historical_runs.assert_called_with(12345, "model1", last_run_count=10)
    assert len(runs) == 2


def test_model_to_dict(project):
    """Test the to_dict method of Model."""
    model = project.get_model("model1")
    model_dict = model.to_dict()
    
    assert model_dict["name"] == "model1"
    assert model_dict["unique_id"] == "model.test.model1"
    assert model_dict["database"] == "analytics"
    assert model_dict["schema"] == "public"
    assert model_dict["description"] == "Test model 1"
    assert "last_run" in model_dict and isinstance(model_dict["last_run"], dict)