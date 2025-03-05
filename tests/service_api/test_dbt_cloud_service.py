"""
Tests for the service_api module.
"""

import json
import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock

from src.service_api.DbtCloudService import DbtCloudService
from src.service_api.models import (
    DbtJobsResponse, DbtAccountResponse, DbtJob, DbtAccountInfo,
    DbtJobSchedule, DateTimeEncoder
)


class TestDbtModels:
    """Tests for the models in the service_api module."""
    
    def test_api_response_mixin_to_json(self):
        """Test that the ApiResponseMixin.to_json method properly serializes models."""
        from src.service_api.models import DbtAccountResponse, DbtAccountInfo
        from datetime import datetime
        import json
        
        # Create a test response with a datetime
        test_date = datetime(2023, 1, 1, 12, 0, 0)
        account_info = DbtAccountInfo(
            id=123,
            name="Test Account",
            state=1
        )
        response = DbtAccountResponse(
            data=account_info,
            status={
                "code": 200,
                "timestamp": test_date
            }
        )
        
        # Test JSON serialization
        json_str = response.to_json(indent=2)
        
        # Verify it's valid JSON
        parsed = json.loads(json_str)
        assert parsed["data"]["id"] == 123
        assert parsed["data"]["name"] == "Test Account"
        assert parsed["status"]["code"] == 200
        assert parsed["status"]["timestamp"] == "2023-01-01T12:00:00"
        
    def test_job_schedule_serialization(self):
        """Test that job schedules with list values serialize correctly."""
        # Create a schedule with list in the date field
        schedule = DbtJobSchedule(
            date={
                "type": "days_of_week",
                "days": [0, 1, 2, 3, 4, 5, 6]
            },
            time={
                "type": "every_hour",
                "interval": 1
            },
            cron="0 * * * 0,1,2,3,4,5,6"
        )
        
        # Serialize to JSON using the to_json method
        json_str = schedule.to_json()
        parsed = json.loads(json_str)
        
        # Verify the days list is preserved
        assert parsed["date"]["days"] == [0, 1, 2, 3, 4, 5, 6]
        assert parsed["time"]["type"] == "every_hour"
        assert parsed["cron"] == "0 * * * 0,1,2,3,4,5,6"
        
    def test_job_completion_trigger_condition_dict(self):
        """Test that job_completion_trigger_condition can handle dictionary values."""
        # Create a job with a dictionary for job_completion_trigger_condition
        job = DbtJob(
            id=1,
            account_id=123,
            project_id=456,
            environment_id=789,
            name="Test Job",
            description="Test job description",
            execute_steps=["dbt run"],
            job_type="scheduled",
            settings={"threads": 4, "target_name": "prod"},
            state=1,
            triggers={
                "github_webhook": False,
                "schedule": True,
                "git_provider_webhook": False,
                "on_merge": False
            },
            job_completion_trigger_condition={
                "condition": {
                    "job_id": 54321,
                    "statuses": [20],
                    "project_id": 456
                }
            },
            created_at=datetime(2023, 1, 1),
            updated_at=datetime(2023, 1, 2)
        )
        
        # Create a response with the job
        response = DbtJobsResponse(
            data=[job],
            status={"code": 200}
        )
        
        # Serialize to JSON
        json_str = response.to_json()
        parsed = json.loads(json_str)
        
        # Verify the dictionary is preserved
        trigger_condition = parsed["data"][0]["job_completion_trigger_condition"]
        assert isinstance(trigger_condition, dict)
        assert trigger_condition["condition"]["job_id"] == 54321
        assert trigger_condition["condition"]["project_id"] == 456
        assert trigger_condition["condition"]["statuses"] == [20]


class TestDbtCloudService:
    """Tests for the DbtCloudService class."""

    @pytest.fixture
    def dbt_cloud_service(self):
        """Create a DbtCloudService instance with a mock token."""
        with patch.dict('os.environ', {'DBT_SERVICE_TOKEN': 'test_token'}):
            return DbtCloudService()

    @pytest.fixture
    def mock_response(self):
        """Create a mock HTTP response."""
        mock = MagicMock()
        mock.json.return_value = {}
        mock.raise_for_status.return_value = None
        return mock

    def test_init_with_token(self):
        """Test initialization with an explicit token."""
        service = DbtCloudService(token="explicit_token")
        assert service.headers["Authorization"] == "Bearer explicit_token"
        assert service.base_url == "https://cloud.getdbt.com/api/v2"

    def test_init_with_custom_url(self):
        """Test initialization with a custom base URL."""
        service = DbtCloudService(token="test_token", base_url="https://custom.dbt.com/api/v2")
        assert service.base_url == "https://custom.dbt.com/api/v2"

    def test_init_without_token_raises_error(self):
        """Test that initialization without a token raises an error."""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError) as excinfo:
                DbtCloudService()
            assert "DBT_SERVICE_TOKEN environment variable not set" in str(excinfo.value)

    @patch('requests.request')
    def test_make_request(self, mock_request, dbt_cloud_service, mock_response):
        """Test the _make_request method."""
        mock_response.json.return_value = {"key": "value"}
        mock_request.return_value = mock_response

        result = dbt_cloud_service._make_request("GET", "test/endpoint", params={"param": "value"})

        mock_request.assert_called_once_with(
            method="GET",
            url="https://cloud.getdbt.com/api/v2/test/endpoint",
            headers=dbt_cloud_service.headers,
            params={"param": "value"},
            json=None
        )
        assert result == {"key": "value"}

    @patch('requests.request')
    def test_make_request_invalid_response(self, mock_request, dbt_cloud_service, mock_response):
        """Test that _make_request raises an error for non-dict responses."""
        mock_response.json.return_value = ["not", "a", "dict"]
        mock_request.return_value = mock_response

        with pytest.raises(TypeError) as excinfo:
            dbt_cloud_service._make_request("GET", "test/endpoint")
        assert "Expected dict, got list" in str(excinfo.value)

    @patch('src.service_api.DbtCloudService.DbtCloudService._make_request')
    def test_get_jobs(self, mock_make_request, dbt_cloud_service):
        """Test the get_jobs method."""
        mock_job = {
            "id": 1,
            "account_id": 123,
            "project_id": 456,
            "environment_id": 789,
            "name": "Test Job",
            "description": "Test job description",
            "execute_steps": ["dbt run"],
            "job_type": "scheduled",
            "settings": {"threads": 4, "target_name": "prod"},
            "state": 1,
            "triggers": {
                "github_webhook": False,
                "schedule": True,
                "git_provider_webhook": False,
                "on_merge": False
            },
            "job_completion_trigger_condition": None,
            "schedule": {
                "date": {"days": [0, 1, 2, 3, 4, 5, 6]},
                "time": {"type": "every_hour", "hour": None, "minute": 0}
            },
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-02T00:00:00Z"
        }
        
        mock_make_request.return_value = {
            "data": [mock_job],
            "status": {"code": 200}
        }

        account_id = 123
        result = dbt_cloud_service.get_jobs(account_id)

        mock_make_request.assert_called_once_with(
            "GET", 
            "accounts/123/jobs/", 
            params={"account_id": 123}
        )
        
        assert isinstance(result, DbtJobsResponse)
        assert len(result.data) == 1
        assert isinstance(result.data[0], DbtJob)
        assert result.data[0].name == "Test Job"
        assert result.data[0].account_id == 123

    @patch('src.service_api.DbtCloudService.DbtCloudService._make_request')
    def test_get_account(self, mock_make_request, dbt_cloud_service):
        """Test the get_account method."""
        mock_account = {
            "id": 123,
            "name": "Test Account",
            "state": 1
        }
        
        mock_make_request.return_value = {
            "data": mock_account,
            "status": {"code": 200}
        }

        account_id = 123
        result = dbt_cloud_service.get_account(account_id)

        mock_make_request.assert_called_once_with("GET", "accounts/123/")
        
        assert isinstance(result, DbtAccountResponse)
        assert isinstance(result.data, DbtAccountInfo)
        assert result.data.name == "Test Account"
        assert result.data.id == 123
        assert result.data.state == 1


@pytest.mark.integration
class TestDbtCloudServiceIntegration:
    """Integration tests for the DbtCloudService class that require API access."""
    
    @pytest.fixture
    def dbt_cloud_service(self):
        """Create a DbtCloudService instance using the environment token."""
        return DbtCloudService()
    
    def test_get_jobs_integration(self, dbt_cloud_service):
        """Integration test for getting jobs from a real account."""
        # To run this test, you need a real dbt Cloud account ID and valid token
        # The test will be skipped by default unless --run-integration is specified
        
        # Replace with a real account ID for testing
        account_id = 19751
        
        response = dbt_cloud_service.get_jobs(account_id)
        
        assert isinstance(response, DbtJobsResponse)
        assert hasattr(response, 'data')
        
        # Basic validation that we got some data
        if len(response.data) > 0:
            job = response.data[0]
            assert isinstance(job, DbtJob)
            assert job.account_id == account_id
    
    def test_get_account_integration(self, dbt_cloud_service):
        """Integration test for getting account information."""
        # To run this test, you need a real dbt Cloud account ID and valid token
        # The test will be skipped by default unless --run-integration is specified
        
        # Replace with a real account ID for testing
        account_id = 19751
        
        response = dbt_cloud_service.get_account(account_id)
        
        assert isinstance(response, DbtAccountResponse)
        assert hasattr(response, 'data')
        assert isinstance(response.data, DbtAccountInfo)
        assert response.data.id == account_id