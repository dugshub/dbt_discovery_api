import os
import pytest
from typing import Dict, Any, Optional

from query_layer.EnvironmentService import EnvironmentService
from query_layer.BaseQuery import BaseQuery


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
def environment_service(base_query) -> EnvironmentService:
    """Create an EnvironmentService with a real BaseQuery."""
    return EnvironmentService(base_query)


@pytest.mark.integration
class TestEnvironmentServiceIntegration:
    """Integration tests for the EnvironmentService class using real dbt Cloud API."""
    
    def test_get_environment_metadata(self, environment_service, environment_id):
        """Test getting environment metadata from the real API."""
        if environment_id == 0:
            pytest.skip("ENV_ID_MART_PRODUCTION environment variable not set")
            
        result = environment_service.get_environment_metadata(environment_id)
        
        # Verify the structure of the response
        assert isinstance(result, dict)
        assert "dbt_project_name" in result
        assert "adapter_type" in result
        
        # Log for debugging
        print(f"Project name: {result['dbt_project_name']}")
        print(f"Adapter type: {result['adapter_type']}")
    
    def test_get_applied_state(self, environment_service, environment_id):
        """Test getting applied state from the real API."""
        if environment_id == 0:
            pytest.skip("ENV_ID_MART_PRODUCTION environment variable not set")
            
        result = environment_service.get_applied_state(environment_id)
        
        # Verify the structure of the response
        assert isinstance(result, dict)
        assert "last_updated_at" in result
        assert "resource_counts" in result
        assert "latest_git_sha" in result
        
        # Verify resource counts is a dict with expected keys
        assert isinstance(result["resource_counts"], dict)
        
        # Log for debugging
        print(f"Last updated: {result['last_updated_at']}")
        print(f"Latest git SHA: {result['latest_git_sha']}")
        print(f"Resource counts: {result['resource_counts']}")
    
    def test_get_definition_state(self, environment_service, environment_id):
        """Test getting definition state from the real API."""
        if environment_id == 0:
            pytest.skip("ENV_ID_MART_PRODUCTION environment variable not set")
            
        result = environment_service.get_definition_state(environment_id)
        
        # Verify the structure of the response
        assert isinstance(result, dict)
        assert "last_updated_at" in result
        assert "resource_counts" in result
        
        # Verify resource counts is a dict
        assert isinstance(result["resource_counts"], dict)
        
        # Log for debugging
        print(f"Last updated: {result['last_updated_at']}")
        print(f"Resource counts: {result['resource_counts']}")