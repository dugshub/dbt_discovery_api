import pytest
from unittest.mock import MagicMock

from src.discovery_api.services.EnvironmentService import EnvironmentService
from src.discovery_api.services.BaseQuery import BaseQuery


@pytest.fixture
def mock_base_query():
    """Fixture to create a mocked BaseQuery."""
    mock = MagicMock(spec=BaseQuery)
    
    # Mock the execute method to return a predefined response
    mock.execute.return_value = {
        "data": {
            "environment": {
                "dbt_project_name": "test_project",
                "adapter_type": "snowflake",
                "applied": {
                    "last_updated_at": "2023-01-01T00:00:00Z",
                    "resource_counts": {"models": 10, "tests": 5},
                    "latest_git_sha": "abc123"
                },
                "definition": {
                    "last_updated_at": "2023-01-01T00:00:00Z",
                    "resource_counts": {"models": 12, "tests": 7}
                }
            }
        }
    }
    
    # Mock the create_operation methods
    mock_op = MagicMock()
    mock_env = MagicMock()
    mock.create_environment_query.return_value = (mock_op, mock_env)
    
    mock_applied = MagicMock()
    mock.create_applied_state_query.return_value = (mock_op, mock_applied)
    
    mock_definition = MagicMock()
    mock.create_definition_state_query.return_value = (mock_op, mock_definition)
    
    return mock


@pytest.fixture
def environment_service(mock_base_query):
    """Fixture to create an EnvironmentService with a mocked BaseQuery."""
    return EnvironmentService(mock_base_query)


class TestEnvironmentService:
    """Tests for the EnvironmentService class."""
    
    def test_init(self, mock_base_query):
        """Test initialization of EnvironmentService."""
        service = EnvironmentService(mock_base_query)
        assert service.base_query == mock_base_query
    
    def test_add_environment_fields(self, environment_service):
        """Test _add_environment_fields method."""
        mock_env = MagicMock()
        environment_service._add_environment_fields(mock_env)
        
        # Verify the correct fields are added
        mock_env.dbt_project_name.assert_called_once()
        mock_env.adapter_type.assert_called_once()
    
    def test_add_applied_fields(self, environment_service):
        """Test _add_applied_fields method."""
        mock_applied = MagicMock()
        environment_service._add_applied_fields(mock_applied)
        
        # Verify the correct fields are added
        mock_applied.last_updated_at.assert_called_once()
        mock_applied.resource_counts.assert_called_once()
        mock_applied.latest_git_sha.assert_called_once()
    
    def test_add_definition_fields(self, environment_service):
        """Test _add_definition_fields method."""
        mock_definition = MagicMock()
        environment_service._add_definition_fields(mock_definition)
        
        # Verify the correct fields are added
        mock_definition.last_updated_at.assert_called_once()
        mock_definition.resource_counts.assert_called_once()
    
    def test_get_environment_metadata(self, environment_service, mock_base_query):
        """Test get_environment_metadata method."""
        # Define test data
        environment_id = 123
        expected_result = {
            "dbt_project_name": "test_project",
            "adapter_type": "snowflake"
        }
        
        # Configure mock
        mock_base_query.execute.return_value = {
            "data": {"environment": expected_result}
        }
        
        # Call the method
        result = environment_service.get_environment_metadata(environment_id)
        
        # Verify the result
        assert result == expected_result
        
        # Verify method calls
        mock_base_query.create_environment_query.assert_called_once_with(environment_id)
        _, mock_env = mock_base_query.create_environment_query.return_value
        mock_base_query.execute.assert_called_once()
    
    def test_get_applied_state(self, environment_service, mock_base_query):
        """Test get_applied_state method."""
        # Define test data
        environment_id = 123
        expected_result = {
            "last_updated_at": "2023-01-01T00:00:00Z",
            "resource_counts": {"models": 10, "tests": 5},
            "latest_git_sha": "abc123"
        }
        
        # Configure mock
        mock_base_query.execute.return_value = {
            "data": {"environment": {"applied": expected_result}}
        }
        
        # Call the method
        result = environment_service.get_applied_state(environment_id)
        
        # Verify the result
        assert result == expected_result
        
        # Verify method calls
        mock_base_query.create_applied_state_query.assert_called_once_with(environment_id)
        _, mock_applied = mock_base_query.create_applied_state_query.return_value
        mock_base_query.execute.assert_called_once()
    
    def test_get_definition_state(self, environment_service, mock_base_query):
        """Test get_definition_state method."""
        # Define test data
        environment_id = 123
        expected_result = {
            "last_updated_at": "2023-01-01T00:00:00Z",
            "resource_counts": {"models": 12, "tests": 7}
        }
        
        # Configure mock
        mock_base_query.execute.return_value = {
            "data": {"environment": {"definition": expected_result}}
        }
        
        # Call the method
        result = environment_service.get_definition_state(environment_id)
        
        # Verify the result
        assert result == expected_result
        
        # Verify method calls
        mock_base_query.create_definition_state_query.assert_called_once_with(environment_id)
        _, mock_definition = mock_base_query.create_definition_state_query.return_value
        mock_base_query.execute.assert_called_once()