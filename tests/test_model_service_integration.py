import os
import pytest
from typing import Optional

from src.services.BaseQuery import BaseQuery
from src.services.ModelService import ModelService
from src.models import Model, ModelDefinition, ModelHistoricalRun


@pytest.fixture
def dbt_token() -> Optional[str]:
    """Retrieve the DBT service token from environment variables."""
    return os.environ.get("DBT_SERVICE_TOKEN")


@pytest.fixture
def environment_id() -> int:
    """Get the environment ID for integration tests."""
    # Using ENV_ID_MART_PRODUCTION as specified
    return int(os.environ.get("ENV_ID_MART_PRODUCTION", "0"))


@pytest.fixture
def base_query(dbt_token) -> Optional[BaseQuery]:
    """Create a real BaseQuery instance with the DBT token."""
    if not dbt_token:
        pytest.skip("DBT_SERVICE_TOKEN environment variable not set")
    return BaseQuery(token=dbt_token)


@pytest.fixture
def model_service(base_query) -> ModelService:
    """Create a ModelService with a real BaseQuery."""
    return ModelService(base_query)


@pytest.mark.integration
class TestModelServiceIntegration:
    """Integration tests for the ModelService class using real dbt Cloud API."""
    
    def test_get_models_applied(self, model_service, environment_id):
        """Test getting applied models from the real API."""
        if environment_id == 0:
            pytest.skip("ENV_ID_MART_PRODUCTION environment variable not set")
            
        result = model_service.get_models_applied(environment_id, limit=5)
        
        # Verify the result is a list of Model objects
        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(model, Model) for model in result)
        
        # Verify model properties
        for model in result:
            assert model.name
            assert model.unique_id
            # Print a few details for debugging
            print(f"Model: {model.name}, Type: {model.materialized_type}")
    
    def test_get_models_definition(self, model_service, environment_id):
        """Test getting model definitions from the real API."""
        if environment_id == 0:
            pytest.skip("ENV_ID_MART_PRODUCTION environment variable not set")
            
        result = model_service.get_models_definition(environment_id, limit=5)
        
        # Verify the result is a list of ModelDefinition objects
        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(model, ModelDefinition) for model in result)
        
        # Verify model properties
        for model in result:
            assert model.name
            assert model.unique_id
            assert model.resource_type
            # Print a few details for debugging
            print(f"Model: {model.name}, File: {model.file_path}")
    
    def test_get_model_by_name(self, model_service, environment_id):
        """Test getting a specific model by name."""
        if environment_id == 0:
            pytest.skip("ENV_ID_MART_PRODUCTION environment variable not set")
            
        # First get a list of models to find a real model name
        models = model_service.get_models_applied(environment_id, limit=1)
        if not models:
            pytest.skip("No models found in the environment")
            
        test_model_name = models[0].name
        print(f"Testing with model: {test_model_name}")
        
        # Test getting the model by name in applied state
        result_applied = model_service.get_model_by_name(
            environment_id, 
            test_model_name, 
            state='applied'
        )
        
        # Verify result
        assert result_applied is not None
        assert isinstance(result_applied, Model)
        assert result_applied.name == test_model_name
        
        # Test getting the model by name in definition state
        result_definition = model_service.get_model_by_name(
            environment_id, 
            test_model_name, 
            state='definition'
        )
        
        # Verify result (this might be None if the model doesn't exist in definition state)
        if result_definition:
            assert isinstance(result_definition, ModelDefinition)
            assert result_definition.name == test_model_name
    
    def test_get_model_historical_runs(self, model_service, environment_id):
        """Test getting historical runs for a model."""
        if environment_id == 0:
            pytest.skip("ENV_ID_MART_PRODUCTION environment variable not set")
            
        # First get a list of models to find a real model name
        models = model_service.get_models_applied(environment_id, limit=1)
        if not models:
            pytest.skip("No models found in the environment")
            
        test_model_name = models[0].name
        print(f"Testing historical runs for model: {test_model_name}")
        
        # Test getting historical runs
        result = model_service.get_model_historical_runs(
            environment_id, 
            test_model_name, 
            last_run_count=3
        )
        
        # Verify result structure
        assert isinstance(result, list)
        # Note: it's possible there are no historical runs, so we don't assert length > 0
        
        if result:
            assert all(isinstance(run, ModelHistoricalRun) for run in result)
            for run in result:
                assert run.name == test_model_name
                print(f"Run status: {run.status}, Run ID: {run.run_id}")
    
    def test_model_fields_consistency(self, model_service, environment_id):
        """Test that model fields are consistent between applied and definition states."""
        if environment_id == 0:
            pytest.skip("ENV_ID_MART_PRODUCTION environment variable not set")
            
        # Get models from both states
        applied_models = model_service.get_models_applied(environment_id, limit=5)
        definition_models = model_service.get_models_definition(environment_id, limit=5)
        
        if not applied_models or not definition_models:
            pytest.skip("Not enough models found in both states")
        
        # Find a model that exists in both states
        common_names = set(m.name for m in applied_models) & set(m.name for m in definition_models)
        if not common_names:
            pytest.skip("No common models found between states")
            
        test_model_name = next(iter(common_names))
        print(f"Testing field consistency for model: {test_model_name}")
        
        # Get the same model from both states
        applied_model = next(m for m in applied_models if m.name == test_model_name)
        definition_model = next(m for m in definition_models if m.name == test_model_name)
        
        # Verify common fields match
        assert applied_model.name == definition_model.name
        assert applied_model.unique_id == definition_model.unique_id
        
        # Check other fields that should be the same
        fields_to_check = [
            'database', 'schema', 'alias', 'materialized_type',
            'contract_enforced', 'language', 'fqn', 'package_name'
        ]
        
        for field in fields_to_check:
            applied_value = getattr(applied_model, field, None)
            definition_value = getattr(definition_model, field, None)
            # Only assert if both values are not None
            if applied_value is not None and definition_value is not None:
                print(f"Field: {field}, Applied: {applied_value}, Definition: {definition_value}")
                assert applied_value == definition_value