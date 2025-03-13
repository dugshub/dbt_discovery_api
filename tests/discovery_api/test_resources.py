"""Tests for resource models (Model, Job, Run, Project)."""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from src.discovery_api.models.base import RunStatus
from src.discovery_api.models.filters import SearchFilter, ModelFilter
from src.discovery_api.api.resources.model import Model
from src.discovery_api.api.resources.job import Job
from src.discovery_api.api.resources.run import Run
from src.discovery_api.api.resources.project import Project

# Test data
@pytest.fixture
def sample_datetime():
    return datetime(2025, 3, 12, 10, 0, 0)

@pytest.fixture
def mock_job_service():
    service = Mock()
    service.get_job_models.return_value = {
        'models': [
            {
                'unique_id': 'model.project1.model1',
                'name': 'model1',
                'execution_time': 10.5,
                'status': 'success',
                'execute_started_at': datetime(2025, 3, 12, 10, 0, 0),
                'execute_completed_at': datetime(2025, 3, 12, 10, 1, 0),
                'tags': ['daily'],
                'materialized': 'table',
                'description': 'Test model'
            }
        ]
    }
    service.get_job_runs.return_value = [
        {
            'id': '123',
            'status': 'success',
            'runtime': 65.5,
            'total_models': 1,
            'started_at': datetime(2025, 3, 12, 10, 0, 0),
            'finished_at': datetime(2025, 3, 12, 10, 1, 5)
        }
    ]
    return service

@pytest.fixture
def mock_model_service():
    service = Mock()
    service.get_models_applied.return_value = [
        {
            'name': 'model1',
            'unique_id': 'model.project1.model1',
            'tags': ['daily'],
            'materialized_type': 'table',
            'description': 'Test model',
            'execution_info': {
                'execution_time': 10.5,
                'last_run_status': 'success',
                'execute_started_at': datetime(2025, 3, 12, 10, 0, 0),
                'execute_completed_at': datetime(2025, 3, 12, 10, 1, 0)
            }
        }
    ]
    return service

class TestModel:
    """Test Model resource."""
    
    def test_model_init(self):
        """Test Model initialization."""
        model = Model(
            model_id="project1.model1",
            last_run_status=RunStatus.SUCCESS,
            last_run_runtime=10.5,
            last_run_start_time=datetime(2025, 3, 12, 10, 0, 0),
            last_run_end_time=datetime(2025, 3, 12, 10, 1, 0),
            tags=["daily"],
            materialization="table",
            description="Test model"
        )
        
        assert model.model_id == "project1.model1"
        assert model.project_name == "project1"
        assert model.model_name == "model1"
        assert model.last_run_status == RunStatus.SUCCESS
        assert model.last_run_runtime == 10.5
        assert len(model.tags) == 1
        assert model.materialization == "table"
    
    def test_get_runs(self, mock_model_service):
        """Test getting model runs."""
        model = Model(model_id="project1.model1")
        model._project = Mock()
        model._project.environment_id = "123"
        model._project.model_service = mock_model_service
        
        runs = model.get_runs(last_n=1)
        assert len(runs) == 1
        assert isinstance(runs[0], Run)
    
    def test_get_sql(self, mock_model_service):
        """Test getting model SQL."""
        mock_model_service.get_model_by_unique_id.return_value = {
            'raw_sql': 'SELECT * FROM table'
        }
        
        model = Model(model_id="project1.model1")
        model._project = Mock()
        model._project.environment_id = "123"
        model._project.model_service = mock_model_service
        model._unique_id = "model.project1.model1"
        
        sql = model.get_sql()
        assert sql == 'SELECT * FROM table'

class TestJob:
    """Test Job resource."""
    
    def test_job_init(self):
        """Test Job initialization."""
        job = Job(
            job_id="123",
            environment_id="456",
            name="Test Job",
            last_run_status=RunStatus.SUCCESS,
            last_run_runtime=65.5,
            last_run_start_time=datetime(2025, 3, 12, 10, 0, 0),
            last_run_end_time=datetime(2025, 3, 12, 10, 1, 5)
        )
        
        assert job.job_id == "123"
        assert job.environment_id == "456"
        assert job.name == "Test Job"
        assert job.last_run_status == RunStatus.SUCCESS
        assert job.last_run_runtime == 65.5
    
    def test_get_models(self, mock_job_service):
        """Test getting job models."""
        job = Job(job_id="123")
        job.job_service = mock_job_service
        
        models = job.get_models()
        assert len(models) == 1
        assert isinstance(models[0], Model)
        assert models[0].model_id == "model1"
    
    def test_get_runs(self, mock_job_service):
        """Test getting job runs."""
        job = Job(job_id="123")
        job.job_service = mock_job_service
        
        runs = job.get_runs(last_n=1)
        assert len(runs) == 1
        assert isinstance(runs[0], Run)
        assert runs[0].runtime == 65.5

class TestRun:
    """Test Run resource."""
    
    def test_run_init(self):
        """Test Run initialization."""
        run = Run(
            run_id="123",
            status="success",
            runtime=65.5,
            model_count=1,
            start_time=datetime(2025, 3, 12, 10, 0, 0),
            end_time=datetime(2025, 3, 12, 10, 1, 5),
            job_id="456"
        )
        
        assert run.run_id == "123"
        assert run.status == RunStatus.SUCCESS
        assert run.runtime == 65.5
        assert run.model_count == 1
        assert run.job_id == "456"
    
    def test_get_models(self, mock_job_service):
        """Test getting run models."""
        run = Run(run_id="123", job_id="456")
        run.job_service = mock_job_service
        
        models = run.get_models()
        assert len(models) == 1
        assert isinstance(models[0], Model)
    
    def test_get_slowest_models(self, mock_job_service):
        """Test getting slowest models in run."""
        run = Run(run_id="123", job_id="456")
        run.job_service = mock_job_service
        
        models = run.get_slowest_models(slowest_n=1)
        assert len(models) == 1
        assert isinstance(models[0], Model)
        assert models[0].last_run_runtime == 10.5

class TestProject:
    """Test Project resource."""
    
    def test_project_init(self):
        """Test Project initialization."""
        project = Project(environment_id="123", name="Test Project")
        assert project.environment_id == "123"
        assert project.name == "Test Project"
    
    def test_get_models(self, mock_model_service):
        """Test getting project models."""
        project = Project(environment_id="123")
        project.model_service = mock_model_service
        
        models = project.get_models()
        assert len(models) == 1
        assert isinstance(models[0], Model)
        assert models[0].model_id == "project1.model1"
    
    def test_model_count(self, mock_model_service):
        """Test getting project model count."""
        project = Project(environment_id="123")
        project.environment_service.get_definition_state.return_value = {
            'resource_counts': {'model': 5}
        }
        
        assert project.model_count == 5
    
    def test_slowest_models(self, mock_model_service):
        """Test getting slowest models in project."""
        project = Project(environment_id="123")
        project.model_service = mock_model_service
        
        models = project.slowest_models(slowest_n=1)
        assert len(models) == 1
        assert isinstance(models[0], Model)
        assert models[0].last_run_runtime == 10.5

# Integration tests
def test_job_model_integration(mock_job_service, mock_model_service):
    """Test integration between Job and Model."""
    job = Job(job_id="123")
    job.job_service = mock_job_service
    
    # Get models from job
    models = job.get_models()
    assert len(models) == 1
    
    # Get runs for a model
    model = models[0]
    model._project = Mock()
    model._project.environment_id = "123"
    model._project.model_service = mock_model_service
    
    runs = model.get_runs(last_n=1)
    assert len(runs) == 1

def test_filtering_integration():
    """Test filter integration across resources."""
    # Create test data
    base_datetime = datetime(2025, 3, 12, 10, 0, 0)
    
    model1 = Model(
        model_id="project1.model1",
        tags=["daily"],
        materialization="table",
        last_run_runtime=10.5
    )
    model2 = Model(
        model_id="project1.model2",
        tags=["weekly"],
        materialization="view",
        last_run_runtime=20.5
    )
    
    # Test SearchFilter
    filter = SearchFilter(
        tags=["daily"],
        materialization="table",
        min_runtime=5.0,
        max_runtime=15.0
    )
    
    # Should match model1 but not model2
    models = [model1, model2]
    filtered_models = [m for m in models if (
        (not filter.tags or any(tag in m.tags for tag in filter.tags)) and
        (not filter.materialization or m.materialization == filter.materialization) and
        (filter.min_runtime is None or m.last_run_runtime >= filter.min_runtime) and
        (filter.max_runtime is None or m.last_run_runtime <= filter.max_runtime)
    )]
    
    assert len(filtered_models) == 1
    assert filtered_models[0].model_id == "project1.model1"