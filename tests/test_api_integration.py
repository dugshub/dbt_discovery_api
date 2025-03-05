"""
Integration tests for the API layer.

These tests require a valid DBT Cloud API token and will make actual API calls.
Run with: pytest -xvs tests/test_api_integration.py --run-integration
"""

import os
import pytest

from src.api import DiscoveryAPI


# Mark all tests in this file as integration tests
pytestmark = pytest.mark.integration


@pytest.fixture
def api():
    """Create a real DiscoveryAPI instance for testing."""
    token = os.environ.get("DBT_SERVICE_TOKEN")
    if not token:
        pytest.skip("DBT_SERVICE_TOKEN environment variable not set")
    
    return DiscoveryAPI(token=token)


@pytest.fixture
def environment_id():
    """Get a test environment ID from environment variables."""
    env_id = os.environ.get("ENV_ID_SANDBOX_PRODUCTION")
    if not env_id:
        pytest.skip("ENV_ID_SANDBOX_PRODUCTION environment variable not set")
    
    return int(env_id)


def test_api_project_connection(api, environment_id):
    """Test connecting to a project."""
    project = api.project(environment_id)
    assert project is not None
    assert project.environment_id == environment_id


def test_project_metadata(api, environment_id):
    """Test getting project metadata."""
    project = api.project(environment_id)
    metadata = project.get_metadata()
    
    assert metadata.dbt_project_name is not None
    assert metadata.adapter_type is not None
    assert metadata.environment_id == environment_id


def test_project_get_models(api, environment_id):
    """Test getting all models in a project."""
    project = api.project(environment_id)
    models = project.get_models()
    
    assert len(models) > 0
    
    # Check a few model properties
    first_model = models[0]
    assert first_model.metadata.name is not None
    assert first_model.metadata.unique_id is not None


def test_project_get_model(api, environment_id):
    """Test getting a specific model.
    
    This test depends on having a model with a specific name in your environment.
    Adjust the model_name to match a model in your environment.
    """
    project = api.project(environment_id)
    models = project.get_models()
    
    # Use the name of the first model for testing
    if not models:
        pytest.skip("No models available in the environment")
    
    model_name = models[0].metadata.name
    model = project.get_model(model_name)
    
    assert model is not None
    assert model.metadata.name == model_name


def test_model_properties(api, environment_id):
    """Test model properties."""
    project = api.project(environment_id)
    models = project.get_models()
    
    if not models:
        pytest.skip("No models available in the environment")
    
    # Get the first model
    model = models[0]
    
    # Test metadata
    assert model.metadata is not None
    assert model.metadata.name is not None
    assert model.metadata.unique_id is not None
    
    # Test last_run (may be None if model has never been run)
    # Just checking that the property accessor works, not the actual value
    _ = model.last_run
    
    # Test to_dict
    model_dict = model.to_dict()
    assert model_dict is not None
    assert model_dict["name"] == model.metadata.name


def test_model_historical_runs(api, environment_id):
    """Test getting historical runs for a model."""
    project = api.project(environment_id)
    models = project.get_models()
    
    if not models:
        pytest.skip("No models available in the environment")
    
    # Try to find a model with at least one run
    model_with_runs = None
    for model in models:
        if model.last_run is not None:
            model_with_runs = model
            break
    
    if not model_with_runs:
        pytest.skip("No models with historical runs available")
    
    # Get historical runs
    model_name = model_with_runs.metadata.name
    runs = project.get_model_historical_runs(model_name, limit=5)
    
    assert len(runs) > 0
    
    # Check run properties
    first_run = runs[0]
    # Check status instead of run_id as it appears run_id might not always be present
    assert first_run.status is not None
    # Check that either run_time or execution_time is available to confirm it's a valid run
    assert first_run.run_time is not None or first_run.execution_time is not None
    
    
def test_get_models_with_runtime(api, environment_id):
    """Test getting models with runtime metrics."""
    project = api.project(environment_id)
    models_with_runtime = project.get_models_with_runtime()
    
    assert len(models_with_runtime) > 0
    
    # Verify we have models with runtime info
    for model in models_with_runtime:
        # Verify structure
        assert model.name is not None
        assert model.unique_id is not None
        assert model.metadata is not None
        assert model.runtime_metrics is not None
        
        # Verify we can access execution data via computed fields
        assert hasattr(model, 'execution_time')
        # execution_time may be None for models that haven't been run
        
        assert hasattr(model, 'last_run_status')
        # last_run_status may be None for models that haven't been run
        
        # Check if we have runtime metrics available
        if model.runtime_metrics.execution_info:
            assert isinstance(model.runtime_metrics.execution_info, dict)
            
            # Check if we have a most recent run
            if model.runtime_metrics.most_recent_run:
                assert hasattr(model.runtime_metrics.most_recent_run, 'status')
                
    # Find a model with execution data if available (for more detailed testing)
    model_with_execution = next((m for m in models_with_runtime if m.execution_time is not None), None)
    
    if model_with_execution:
        assert model_with_execution.execution_time > 0
        assert model_with_execution.last_run_status is not None
        assert model_with_execution.most_recent_run is not None


def test_get_models_with_runtime_sorting_and_limit(api, environment_id):
    """Test sorting and limit functionality for models with runtime metrics."""
    project = api.project(environment_id)
    
    # Skip the test if we don't have enough models with execution_time
    all_models = project.get_models_with_runtime()
    models_with_execution_time = [m for m in all_models if m.execution_time is not None]
    
    if len(models_with_execution_time) < 2:
        pytest.skip("Need at least 2 models with execution_time for sorting test")
    
    # Test descending order (default)
    models_desc = project.get_models_with_runtime(descending=True)
    models_with_times_desc = [m for m in models_desc if m.execution_time is not None]
    
    if len(models_with_times_desc) >= 2:
        # Check if models are sorted by execution_time in descending order
        for i in range(len(models_with_times_desc) - 1):
            assert models_with_times_desc[i].execution_time >= models_with_times_desc[i+1].execution_time
    
    # Test ascending order
    models_asc = project.get_models_with_runtime(descending=False)
    models_with_times_asc = [m for m in models_asc if m.execution_time is not None]
    
    if len(models_with_times_asc) >= 2:
        # Check if models are sorted by execution_time in ascending order
        for i in range(len(models_with_times_asc) - 1):
            assert models_with_times_asc[i].execution_time <= models_with_times_asc[i+1].execution_time
    
    # Test limit
    limit = 2  # Use a small limit for testing
    models_limited = project.get_models_with_runtime(limit=limit)
    assert len(models_limited) == limit
    
    # Verify the limited results are the same as the first 'limit' items from the full results
    for i in range(limit):
        assert models_limited[i].name == models_desc[i].name


def test_get_historical_models_runtimes(api, environment_id):
    """Test getting historical models runtimes."""
    project = api.project(environment_id)
    
    # Skip the test if we don't have enough models with execution_time
    all_models = project.get_models_with_runtime()
    models_with_execution_time = [m for m in all_models if m.execution_time is not None]
    
    if len(models_with_execution_time) < 1:
        pytest.skip("Need at least 1 model with execution_time for this test")
    
    # Get model names for testing
    model_names = [m.name for m in models_with_execution_time[:2]]
    
    # Test with explicit model list
    if model_names:
        runtime_metrics = project.get_historical_models_runtimes(models=model_names[:1], limit=1)
        assert len(runtime_metrics) == 1
        assert runtime_metrics[0].most_recent_run is not None
        assert runtime_metrics[0].execution_info is not None
    
    # Test with slowest flag (default behavior)
    runtime_metrics = project.get_historical_models_runtimes(slowest=True, limit=1)
    assert len(runtime_metrics) == 1
    assert runtime_metrics[0].most_recent_run is not None
    assert runtime_metrics[0].execution_info is not None
    
    # Test with fastest flag
    runtime_metrics = project.get_historical_models_runtimes(fastest=True, limit=1)
    assert len(runtime_metrics) == 1
    # Don't assert most_recent_run is not None as fastest models might not have run history
    assert runtime_metrics[0].execution_info is not None
    
    # Verify the hard limit of 10 is enforced
    runtime_metrics = project.get_historical_models_runtimes(limit=15)
    assert len(runtime_metrics) <= 10