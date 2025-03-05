"""
Tests for API layer core classes.
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from src.discovery_api.models import ModelHistoricalRun
from src.discovery_api.api.api import DiscoveryAPI


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
    
    # Create test models using dictionary-like objects instead of MagicMock
    # to avoid MagicMock returning more MagicMocks when attributes are accessed
    from types import SimpleNamespace
    
    test_models = [
        SimpleNamespace(
            name="model1",
            unique_id="model.test.model1",
            materialized_type="table",
            database="analytics",
            db_schema="public",  # Use 'db_schema' to match the Pydantic model's alias
            description="Test model 1",
            tags=[]
        ),
        SimpleNamespace(
            name="model2",
            unique_id="model.test.model2",
            materialized_type="view",
            database="analytics",
            db_schema="public",  # Use 'db_schema' to match the Pydantic model's alias
            description="Test model 2",
            tags=[]
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
    mock.get_model_by_name.side_effect = lambda env_id, name, state, **kwargs: next(
        (m for m in test_models if m.name == name), None
    )
    mock.get_model_historical_runs.return_value = test_runs
    
    return mock


@pytest.fixture
def api_with_mocks(mock_environment_service, mock_model_service):
    """Create a DiscoveryAPI instance with mocked services."""
    with patch('src.discovery_api.api.api.BaseQuery'), \
         patch('src.discovery_api.api.api.EnvironmentService') as mock_env_service_cls, \
         patch('src.discovery_api.api.api.ModelService') as mock_model_service_cls:
        
        # Configure mocks to return our pre-configured service mocks
        mock_env_service_cls.return_value = mock_environment_service
        mock_model_service_cls.return_value = mock_model_service
        
        # Create API instance
        api = DiscoveryAPI(token="test_token")
        
        yield api
        
@pytest.fixture
def api_with_return_query(mock_environment_service, mock_model_service):
    """Create a DiscoveryAPI instance with return_query=True."""
    with patch('src.discovery_api.api.api.BaseQuery'), \
         patch('src.discovery_api.api.api.EnvironmentService') as mock_env_service_cls, \
         patch('src.discovery_api.api.api.ModelService') as mock_model_service_cls:
        
        # Configure mocks to return our pre-configured service mocks
        mock_env_service_cls.return_value = mock_environment_service
        mock_model_service_cls.return_value = mock_model_service
        
        # Create API instance with return_query=True
        api = DiscoveryAPI(token="test_token", return_query=True)
        
        yield api


@pytest.fixture
def project(api_with_mocks):
    """Create a Project instance using the mocked API."""
    return api_with_mocks.project(environment_id=12345)

@pytest.fixture
def project_with_return_query(api_with_return_query):
    """Create a Project instance with return_query=True."""
    return api_with_return_query.project(environment_id=12345)


def test_api_initialization():
    """Test API initialization with and without token."""
    # Test with explicit token - we only care that the BaseQuery is initialized correctly
    with patch('src.discovery_api.api.api.BaseQuery') as mock_base_query, \
         patch('src.discovery_api.api.api.EnvironmentService'), \
         patch('src.discovery_api.api.api.ModelService'):
        api = DiscoveryAPI(token="test_token")
        mock_base_query.assert_called_once_with("test_token", "https://metadata.cloud.getdbt.com/graphql")
        assert not api.return_query  # Default value
    
    # Test with custom endpoint - we only care that the BaseQuery is initialized correctly
    with patch('src.discovery_api.api.api.BaseQuery') as mock_base_query, \
         patch('src.discovery_api.api.api.EnvironmentService'), \
         patch('src.discovery_api.api.api.ModelService'):
        api = DiscoveryAPI(token="test_token", endpoint="https://custom-endpoint.com/graphql")
        mock_base_query.assert_called_once_with("test_token", "https://custom-endpoint.com/graphql")
        assert not api.return_query  # Default value
        
    # Test with return_query=True
    with patch('src.discovery_api.api.api.BaseQuery') as mock_base_query, \
         patch('src.discovery_api.api.api.EnvironmentService'), \
         patch('src.discovery_api.api.api.ModelService'):
        api = DiscoveryAPI(token="test_token", return_query=True)
        assert api.return_query


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


def test_project_get_metadata(project, project_with_return_query, mock_environment_service):
    """Test getting project metadata."""
    # Test regular project (return_query=False)
    metadata = project.get_metadata()
    mock_environment_service.get_environment_metadata.assert_called_with(12345, return_query=False)
    assert metadata.dbt_project_name == "test_project"
    assert metadata.adapter_type == "snowflake"
    assert metadata.environment_id == 12345
    
    # Reset mock for next test
    mock_environment_service.reset_mock()
    
    # Test project with return_query=True
    metadata = project_with_return_query.get_metadata()
    mock_environment_service.get_environment_metadata.assert_called_with(12345, return_query=True)
    
    # Test explicit override of return_query
    mock_environment_service.reset_mock()
    metadata = project.get_metadata(return_query=True)
    mock_environment_service.get_environment_metadata.assert_called_with(12345, return_query=True)


def test_project_get_models(project, mock_model_service):
    """Test getting all models in a project."""
    # Test initial call fetches models
    models = project.get_models()
    mock_model_service.get_models_applied.assert_called_once_with(12345, return_query=False)
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
    mock_model_service.get_models_applied.assert_called_once_with(12345, return_query=False)
    assert len(models) == 2


def test_project_get_model(project, mock_model_service):
    """Test getting a specific model."""
    # Test getting an existing model
    model = project.get_model("model1")
    assert model.metadata.name == "model1"
    assert model.metadata.unique_id == "model.test.model1"
    
    # Check that the method was called with the correct parameters
    mock_model_service.get_model_by_name.assert_called_with(12345, "model1", state="applied", return_query=False)
    
    # Test error when model doesn't exist
    mock_model_service.get_model_by_name.return_value = None
    with pytest.raises(ValueError):
        project.get_model("nonexistent_model")


def test_project_get_model_historical_runs(project, mock_model_service):
    """Test getting historical runs for a model."""
    runs = project.get_model_historical_runs("model1")
    mock_model_service.get_model_historical_runs.assert_called_once_with(12345, "model1", last_run_count=5, return_query=False)
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
    
    mock_model_service.get_model_historical_runs.assert_called_once_with(12345, "model1", last_run_count=1, return_query=False)
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
    
    mock_model_service.get_model_historical_runs.assert_called_with(12345, "model1", last_run_count=10, return_query=False)
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


def test_get_models_with_runtime(project, mock_model_service):
    """Test getting models with runtime metrics."""
    # Add execution_info to the models
    for model in mock_model_service.get_models_applied.return_value:
        model.execution_info = {
            'last_run_id': 'run1',
            'last_run_status': 'success',
            'execution_time': 10.5,
            'run_generated_at': datetime.now()
        }
    
    # Call the method
    models_with_runtime = project.get_models_with_runtime()
    
    # Verify model service was called correctly
    mock_model_service.get_models_applied.assert_called_with(12345, return_query=False)
    # Should not call get_model_historical_runs anymore
    mock_model_service.get_model_historical_runs.assert_not_called()
    
    # Verify the result structure
    assert len(models_with_runtime) == 2
    assert all(hasattr(m, 'name') for m in models_with_runtime)
    assert all(hasattr(m, 'unique_id') for m in models_with_runtime)
    assert all(hasattr(m, 'metadata') for m in models_with_runtime)
    assert all(hasattr(m, 'runtime_metrics') for m in models_with_runtime)
    
    # Check the computed fields
    for model in models_with_runtime:
        # Check execution_time property
        assert hasattr(model, 'execution_time')
        assert model.execution_time == 10.5
        
        # Check last_run_status property
        assert hasattr(model, 'last_run_status')
        assert model.last_run_status == 'success'
        
        # Check most_recent_run via computed property
        assert model.most_recent_run is not None
        assert isinstance(model.most_recent_run, dict)
        assert "status" in model.most_recent_run
            
        # Check runtime metrics structure
        assert hasattr(model.runtime_metrics, 'execution_info')
        assert model.runtime_metrics.execution_info.get('execution_time') == 10.5


def test_get_models_with_runtime_sorting_and_limit(project, mock_model_service):
    """Test getting models with runtime metrics with sorting and limit."""
    # Set up models with different execution times
    models = mock_model_service.get_models_applied.return_value
    models[0].execution_info = {
        'last_run_id': 'run1',
        'last_run_status': 'success',
        'execution_time': 5.5,  # Lower runtime
        'run_generated_at': datetime.now()
    }
    models[1].execution_info = {
        'last_run_id': 'run2',
        'last_run_status': 'success',
        'execution_time': 15.5,  # Higher runtime
        'run_generated_at': datetime.now()
    }
    
    # Test descending order (default)
    models_with_runtime = project.get_models_with_runtime()
    assert len(models_with_runtime) == 2
    assert models_with_runtime[0].execution_time == 15.5  # Higher runtime first
    assert models_with_runtime[1].execution_time == 5.5   # Lower runtime second
    
    # Test ascending order
    models_with_runtime = project.get_models_with_runtime(descending=False)
    assert len(models_with_runtime) == 2
    assert models_with_runtime[0].execution_time == 5.5   # Lower runtime first
    assert models_with_runtime[1].execution_time == 15.5  # Higher runtime second
    
    # Test limit
    models_with_runtime = project.get_models_with_runtime(limit=1)
    assert len(models_with_runtime) == 1
    assert models_with_runtime[0].execution_time == 15.5  # Only includes the highest runtime
    
    # Test limit with ascending order
    models_with_runtime = project.get_models_with_runtime(descending=False, limit=1)
    assert len(models_with_runtime) == 1
    assert models_with_runtime[0].execution_time == 5.5   # Only includes the lowest runtime


def test_get_historical_models_runtimes_with_model_list(project, mock_model_service):
    """Test getting historical models runtimes with specific model list."""
    # Set up historical runs for test
    mock_model_service.get_model_historical_runs.return_value = [
        ModelHistoricalRun(
            name="model1",
            resource_type="model",
            run_id="run1",
            status="success",
            execution_time=10.5
        )
    ]
    
    # Set up batch historical runs result
    mock_model_service.get_multiple_models_historical_runs.return_value = {
        "model1": [
            ModelHistoricalRun(
                name="model1",
                resource_type="model",
                run_id="run1",
                status="success",
                execution_time=10.5
            )
        ],
        "model2": [
            ModelHistoricalRun(
                name="model2",
                resource_type="model",
                run_id="run2",
                status="success",
                execution_time=12.5
            )
        ]
    }
    
    # Set up execution_info for test models
    for model in mock_model_service.get_models_applied.return_value:
        model.execution_info = {
            'last_run_id': f'run-{model.name}',
            'last_run_status': 'success',
            'execution_time': 5.5 if model.name == "model1" else 15.5,
            'run_generated_at': datetime.now()
        }
    
    # Call the method with specific model list
    model_names = ["model1", "model2"]
    runtime_metrics = project.get_historical_models_runtimes(models=model_names, limit=2)
    
    # Verify model service was called correctly with batched method
    mock_model_service.get_multiple_models_historical_runs.assert_called_with(
        12345, ["model1", "model2"], last_run_count=5, return_query=False
    )
    
    # Verify the result structure
    assert len(runtime_metrics) == 2
    assert all(hasattr(m, 'most_recent_run') for m in runtime_metrics)
    assert all(hasattr(m, 'execution_info') for m in runtime_metrics)
    
    # Verify API enforces hard limit at 10
    many_models = ["model1"] * 15  # Try to get more than the hard limit
    runtime_metrics = project.get_historical_models_runtimes(models=many_models)
    assert len(runtime_metrics) <= 10  # Should be limited to 10


def test_get_historical_models_runtimes_fastest_slowest(project, mock_model_service):
    """Test getting historical models runtimes for fastest/slowest models."""
    # Set up models with different execution times
    models = mock_model_service.get_models_applied.return_value
    models[0].execution_info = {
        'last_run_id': 'run1',
        'last_run_status': 'success',
        'execution_time': 5.5,  # Lower runtime for model1
        'run_generated_at': datetime.now()
    }
    models[1].execution_info = {
        'last_run_id': 'run2',
        'last_run_status': 'success',
        'execution_time': 15.5,  # Higher runtime for model2
        'run_generated_at': datetime.now()
    }
    
    # Set up batch historical runs results
    model1_runs = [
        ModelHistoricalRun(
            name="model1",
            resource_type="model",
            run_id="run1",
            status="success",
            execution_time=5.5
        )
    ]
    
    model2_runs = [
        ModelHistoricalRun(
            name="model2",
            resource_type="model",
            run_id="run2",
            status="success",
            execution_time=15.5
        )
    ]
    
    # For slowest test
    mock_model_service.get_multiple_models_historical_runs.return_value = {
        "model2": model2_runs
    }
    
    # Test slowest models (default behavior)
    runtime_metrics = project.get_historical_models_runtimes(limit=1)
    mock_model_service.get_multiple_models_historical_runs.assert_called_with(
        12345, ["model2"], last_run_count=5, return_query=False
    )
    assert len(runtime_metrics) == 1
    
    # For fastest test
    mock_model_service.get_multiple_models_historical_runs.reset_mock()
    mock_model_service.get_multiple_models_historical_runs.return_value = {
        "model1": model1_runs
    }
    
    # Test fastest models
    runtime_metrics = project.get_historical_models_runtimes(fastest=True, limit=1)
    mock_model_service.get_multiple_models_historical_runs.assert_called_with(
        12345, ["model1"], last_run_count=5, return_query=False
    )
    assert len(runtime_metrics) == 1
    
    # For explicit slowest flag
    mock_model_service.get_multiple_models_historical_runs.reset_mock()
    mock_model_service.get_multiple_models_historical_runs.return_value = {
        "model2": model2_runs
    }
    
    # Test explicit slowest flag
    runtime_metrics = project.get_historical_models_runtimes(slowest=True, limit=1)
    mock_model_service.get_multiple_models_historical_runs.assert_called_with(
        12345, ["model2"], last_run_count=5, return_query=False
    )
    assert len(runtime_metrics) == 1