"""Test configuration and fixtures for the discovery API tests."""

import pytest
from datetime import datetime
from unittest.mock import Mock

@pytest.fixture
def sample_model_data():
    """Sample model data for testing."""
    return {
        'name': 'test_model',
        'unique_id': 'model.project1.test_model',
        'tags': ['daily', 'marketing'],
        'materialized_type': 'table',
        'description': 'Test model description',
        'execution_info': {
            'execution_time': 10.5,
            'last_run_status': 'success',
            'execute_started_at': datetime(2025, 3, 12, 10, 0, 0),
            'execute_completed_at': datetime(2025, 3, 12, 10, 1, 0)
        }
    }

@pytest.fixture
def sample_job_data():
    """Sample job data for testing."""
    return {
        'id': '123',
        'name': 'Test Job',
        'status': 'success',
        'runtime': 65.5,
        'started_at': datetime(2025, 3, 12, 10, 0, 0),
        'finished_at': datetime(2025, 3, 12, 10, 1, 5),
        'environment_id': '456',
        'models': [
            {
                'name': 'test_model',
                'execution_time': 10.5,
                'status': 'success'
            }
        ]
    }

@pytest.fixture
def mock_services():
    """Mock services for testing."""
    class Services:
        def __init__(self):
            self.base_query = Mock()
            self.job_service = Mock()
            self.model_service = Mock()
            self.environment_service = Mock()
    
    return Services()

@pytest.fixture
def mock_environment():
    """Mock environment for testing."""
    env = {
        'id': '123',
        'dbt_project_name': 'test_project',
        'account_id': '789',
        'project_id': '456'
    }
    return env

@pytest.fixture
def sample_config():
    """Sample config for testing."""
    return {
        'projects': {
            'test_project': {
                'prod_env_id': '123',
                'label': 'Test Project'
            }
        }
    }