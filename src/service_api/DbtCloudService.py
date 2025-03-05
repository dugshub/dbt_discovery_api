from typing import Dict, Any, Optional
import os
import requests
from .models import DbtJobsResponse, DbtAccountResponse


class DbtCloudService:
    """Service for interacting with the dbt Cloud API v2."""

    def __init__(self, token: Optional[str] = None, base_url: str = "https://cloud.getdbt.com/api/v2"):
        """Initialize with auth token and base URL.
        
        Args:
            token: The dbt Cloud API token. If None, will try to get from DBT_SERVICE_TOKEN env var
            base_url: The base URL for the dbt Cloud API
        """
        if token is None:
            token = os.environ.get("DBT_SERVICE_TOKEN")
            if token is None:
                raise ValueError("DBT_SERVICE_TOKEN environment variable not set and no token provided")

        self.base_url = base_url
        self.headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }
    
    def _make_request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None, 
                     data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a request to the dbt Cloud API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (without base URL)
            params: Query parameters
            data: Request body for POST/PUT requests
            
        Returns:
            API response as a dictionary
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        response = requests.request(
            method=method,
            url=url,
            headers=self.headers,
            params=params,
            json=data
        )
        
        response.raise_for_status()
        result = response.json()
        
        if not isinstance(result, dict):
            raise TypeError(f"Expected dict, got {type(result).__name__}")
        return result
    
    def get_jobs(self, account_id: int) -> DbtJobsResponse:
        """Get jobs for a specific account.
        
        Args:
            account_id: The dbt Cloud account ID
            
        Returns:
            DbtJobsResponse containing a list of DbtJob objects
        """
        endpoint = f"accounts/{account_id}/jobs/"
        params = {"account_id": account_id}
        
        response_data = self._make_request("GET", endpoint, params=params)
        return DbtJobsResponse.model_validate(response_data)

    def get_account(self, account_id: int) -> DbtAccountResponse:
        """Get account information.
        
        Args:
            account_id: The dbt Cloud account ID
            
        Returns:
            DbtAccountResponse containing account information
        """
        endpoint = f"accounts/{account_id}/"
        
        response_data = self._make_request("GET", endpoint)
        return DbtAccountResponse.model_validate(response_data)
