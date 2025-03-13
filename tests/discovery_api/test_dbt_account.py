"""Tests for dbtAccount implementation."""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime
import os
import yaml

from src.discovery_api.api.dbt_account import dbtAccount
from src.discovery_api.models.base import RunStatus
from src.discovery_api.models.filters import SearchFilter, ProjectFilter
from src.discovery_api.api.resources.project import Project
from src.discovery_api.api.resources.model import Model
from src.discovery_api.api.resources.job import Job
from src.discovery_api.api.resources.run import Run
from src.discovery_api.exceptions import AuthenticationError, ResourceNotFoundError

@pytest.fixture
def mock_config(tmp_path):
    """Create a mock config file."""
    config = {
        'projects': {
            'project1': {
                'prod_env_id': '123',
                'label': 'Project One'
            },
            'project2': {
                'prod_env_id': '456',
                'label': 'Project Two'
            }
        }
    }
    
    config_path = tmp_path / "config.yml"
    with open(config_path, 'w') as f:
        yaml.dump(config, f)
    
    return str(config_path)

@pytest.fixture
def mock_base_query():
    return Mock()

class TestDbtAccount:
    """Test dbtAccount class."""
    
    def test_init_no_token(self):
        """Test initialization without token."""
        with pytest.raises(AuthenticationError):
            dbtAccount()
    
    def test_init_no_config(self):
        """Test initialization without config file."""
        with pytest.raises(ResourceNotFoundError):
            dbtAccount(token="test-token", config_path="/invalid/path")
    
    def test_init_success(self, mock_config):
        """Test successful initialization."""
        account = dbtAccount(token="test-token", config_path=mock_config)
        assert account.token == "test-token"
        assert account.config_path == mock_config
        assert isinstance(account.config, dict)
        assert "projects" in account.config
    
    def test_get_projects(self, mock_config, mock_base_query):
        """Test getting projects."""
        account = dbtAccount(token="test-token", config_path=mock_config)
        account.base_query = mock_base_query
        
        projects = account.get_projects()
        assert len(projects) == 2
        assert all(isinstance(p, Project) for p in projects)
        assert {p.environment_id for p in projects} == {"123", "456"}
    
    def test_get_projects_with_filter(self, mock_config, mock_base_query):
        """Test getting projects with filter."""
        account = dbtAccount(token="test-token", config_path=mock_config)
        account.base_query = mock_base_query
        
        # Filter to include only project1
        filter = ProjectFilter(environment_ids=["123"])
        projects = account.get_projects(filter=filter)
        assert len(projects) == 1
        assert projects[0].environment_id == "123"
    
    def test_get_jobs(self, mock_config, mock_base_query):
        """Test getting jobs across projects."""
        account = dbtAccount(token="test-token", config_path=mock_config)
        account.base_query = mock_base_query
        
        # Mock project.get_jobs to return test data
        test_jobs = [
            Job(job_id="1", environment_id="123"),
            Job(job_id="2", environment_id="456")
        ]
        
        with patch('src.discovery_api.api.resources.project.Project.get_jobs', return_value=test_jobs[:1]):
            jobs = account.get_jobs()
            assert len(jobs) == 2  # One from each project
            assert all(isinstance(j, Job) for j in jobs)
    
    def test_get_models(self, mock_config, mock_base_query):
        """Test getting models across projects."""
        account = dbtAccount(token="test-token", config_path=mock_config)
        account.base_query = mock_base_query
        
        # Mock project.get_models to return test data
        test_models = [
            Model(model_id="project1.model1", tags=["daily"]),
            Model(model_id="project1.model2", tags=["weekly"])
        ]
        
        with patch('src.discovery_api.api.resources.project.Project.get_models', return_value=test_models):
            models = account.get_models()
            assert len(models) == 4  # Two from each project
            assert all(isinstance(m, Model) for m in models)
    
    def test_get_runs(self, mock_config, mock_base_query):
        """Test getting runs across projects."""
        account = dbtAccount(token="test-token", config_path=mock_config)
        account.base_query = mock_base_query
        
        # Mock job.get_runs to return test data
        test_runs = [
            Run(run_id="1", status="success", runtime=10.5, model_count=2,
                start_time=datetime(2025, 3, 12, 10, 0, 0),
                end_time=datetime(2025, 3, 12, 10, 1, 0))
        ]
        
        with patch('src.discovery_api.api.resources.job.Job.get_runs', return_value=test_runs):
            runs = account.get_runs(limit=5)
            assert len(runs) <= 5  # Respects limit
            assert all(isinstance(r, Run) for r in runs)
    
    def test_slowest_models(self, mock_config, mock_base_query):
        """Test getting slowest models across projects."""
        account = dbtAccount(token="test-token", config_path=mock_config)
        account.base_query = mock_base_query
        
        # Mock get_models to return test data with different runtimes
        test_models = [
            Model(model_id="project1.model1", last_run_runtime=30.5),
            Model(model_id="project1.model2", last_run_runtime=10.5),
            Model(model_id="project2.model1", last_run_runtime=20.5)
        ]
        
        with patch('src.discovery_api.api.dbt_account.dbtAccount.get_models', return_value=test_models):
            slowest = account.slowest_models(slowest_n=2)
            assert len(slowest) == 2
            assert slowest[0].last_run_runtime > slowest[1].last_run_runtime
    
    def test_longest_running_jobs(self, mock_config, mock_base_query):
        """Test getting longest running jobs across projects."""
        account = dbtAccount(token="test-token", config_path=mock_config)
        account.base_query = mock_base_query
        
        # Mock get_jobs to return test data with different runtimes
        test_jobs = [
            Job(job_id="1", last_run_runtime=100.5),
            Job(job_id="2", last_run_runtime=50.5),
            Job(job_id="3", last_run_runtime=75.5)
        ]
        
        with patch('src.discovery_api.api.dbt_account.dbtAccount.get_jobs', return_value=test_jobs):
            longest = account.longest_running_jobs(longest_n=2)
            assert len(longest) == 2
            assert longest[0].last_run_runtime > longest[1].last_run_runtime
    
    def test_caching(self, mock_config, mock_base_query):
        """Test that caching works for expensive operations."""
        account = dbtAccount(token="test-token", config_path=mock_config)
        account.base_query = mock_base_query
        
        # Mock expensive operations
        with patch('src.discovery_api.api.resources.project.Project.get_models') as mock_get_models:
            mock_get_models.return_value = [Model(model_id="test.model1")]
            
            # First call should hit the service
            account.get_models()
            assert mock_get_models.call_count == 2  # Once for each project
            
            # Second call should use cache
            account.get_models()
            assert mock_get_models.call_count == 2  # No additional calls