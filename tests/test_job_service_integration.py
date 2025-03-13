import os
import pytest
from typing import Optional

from src.discovery_api.services.BaseQuery import BaseQuery
from src.discovery_api.services.JobService import JobService


@pytest.fixture
def dbt_token() -> Optional[str]:
    """Retrieve the DBT service token from environment variables."""
    return os.environ.get("DBT_SERVICE_TOKEN")


@pytest.fixture
def job_id() -> int:
    """Get the job ID for integration tests."""
    # Get job ID from environment variable
    return int(os.environ.get("TEST_JOB_ID", "0"))


@pytest.fixture
def base_query(dbt_token) -> Optional[BaseQuery]:
    """Create a real BaseQuery instance with the DBT token."""
    if not dbt_token:
        pytest.skip("DBT_SERVICE_TOKEN environment variable not set")
    return BaseQuery(token=dbt_token)


@pytest.fixture
def job_service(base_query) -> JobService:
    """Create a JobService with a real BaseQuery."""
    return JobService(base_query)


@pytest.mark.integration
class TestJobServiceIntegration:
    """Integration tests for the JobService class using real dbt Cloud API."""
    
    def test_get_job_metadata(self, job_service, job_id):
        """Test getting job metadata from the real API."""
        if job_id == 0:
            pytest.skip("TEST_JOB_ID environment variable not set")
            
        result = job_service.get_job_metadata(job_id)
        
        # Verify that we got a result
        assert result is not None
        assert "id" in result
        assert result["id"] == job_id
        assert "run_id" in result
        
        # Print details for debugging
        print(f"Job ID: {result['id']}, Run ID: {result['run_id']}")
    
    def test_get_job_models(self, job_service, job_id):
        """Test getting job models from the real API."""
        if job_id == 0:
            pytest.skip("TEST_JOB_ID environment variable not set")
            
        result = job_service.get_job_models(job_id)
        
        # Verify that we got a result
        assert result is not None
        
        # Check if there are any models
        assert "models" in result
        if len(result["models"]) > 0:
            # Verify model properties
            for model in result["models"]:
                assert "name" in model
                assert "unique_id" in model
                # Print a few details for debugging
                print(f"Model: {model['name']}, Unique ID: {model['unique_id']}")
    
    def test_get_job_tests(self, job_service, job_id):
        """Test getting job tests from the real API."""
        if job_id == 0:
            pytest.skip("TEST_JOB_ID environment variable not set")
            
        result = job_service.get_job_tests(job_id)
        
        # Verify that we got a result
        assert result is not None
        
        # Check if there are any tests
        assert "tests" in result
        if len(result["tests"]) > 0:
            # Verify test properties
            for test in result["tests"]:
                assert "name" in test
                assert "unique_id" in test
                # Print a few details for debugging
                print(f"Test: {test['name']}, Unique ID: {test['unique_id']}")
    
    def test_get_job_model_by_unique_id(self, job_service, job_id):
        """Test getting a specific model by unique_id."""
        if job_id == 0:
            pytest.skip("TEST_JOB_ID environment variable not set")
            
        # First get a list of models to find a real unique_id
        job_data = job_service.get_job_models(job_id)
        if not job_data or "models" not in job_data or not job_data["models"]:
            pytest.skip("No models found in the job")
            
        test_model = job_data["models"][0]
        test_unique_id = test_model["unique_id"]
        print(f"Testing with model: {test_model['name']}, unique_id: {test_unique_id}")
        
        # Test getting the model by unique_id
        result = job_service.get_job_model_by_unique_id(job_id, test_unique_id)
        
        # Verify result
        assert result is not None
        assert "name" in result
        assert "unique_id" in result
        assert result["unique_id"] == test_unique_id
    
    def test_get_job_test_by_unique_id(self, job_service, job_id):
        """Test getting a specific test by unique_id."""
        if job_id == 0:
            pytest.skip("TEST_JOB_ID environment variable not set")
            
        # First get a list of tests to find a real unique_id
        job_data = job_service.get_job_tests(job_id)
        if not job_data or "tests" not in job_data or not job_data["tests"]:
            pytest.skip("No tests found in the job")
            
        test_item = job_data["tests"][0]
        test_unique_id = test_item["unique_id"]
        print(f"Testing with test: {test_item['name']}, unique_id: {test_unique_id}")
        
        # Test getting the test by unique_id
        result = job_service.get_job_test_by_unique_id(job_id, test_unique_id)
        
        # Verify result
        assert result is not None
        assert "name" in result
        assert "unique_id" in result
        assert result["unique_id"] == test_unique_id
    
    def test_get_job_with_models_and_tests(self, job_service, job_id):
        """Test getting job data with models and tests."""
        if job_id == 0:
            pytest.skip("TEST_JOB_ID environment variable not set")
            
        result = job_service.get_job_with_models_and_tests(job_id)
        
        # Verify that we got a result
        assert result is not None
        
        # Check that models and tests are included
        assert "models" in result
        assert "tests" in result
        
        # Print some info for debugging
        print(f"Job ID: {result['id']}")
        print(f"Number of models: {len(result['models'])}")
        print(f"Number of tests: {len(result['tests'])}")
    
    def test_field_selection(self, job_service, job_id):
        """Test field selection options for job queries."""
        if job_id == 0:
            pytest.skip("TEST_JOB_ID environment variable not set")
            
        # Test with only database fields
        result_db = job_service.get_job_models(job_id, include_database=True, include_code=False)
        
        # Check database fields are included but code fields are not
        if "models" in result_db and result_db["models"]:
            model = result_db["models"][0]
            assert "database" in model
            assert "schema" in model
            assert "raw_sql" not in model
            assert "compiled_sql" not in model
            
        # Test with only code fields
        result_code = job_service.get_job_models(job_id, include_database=False, include_code=True)
        
        # Check code fields are included but database fields are not
        if "models" in result_code and result_code["models"]:
            model = result_code["models"][0]
            assert "raw_sql" in model
            assert "compiled_sql" in model
            assert "database" not in model
            assert "schema" not in model