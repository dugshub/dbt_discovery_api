from typing import Dict, Any, Optional
import os
import requests


class DbtCloudService:
    """Service for interacting with the dbt Cloud API v2."""

    def __init__(self, token: Optional[str] = None, base_url: str = "https://cloud.getdbt.com/api/v2"):
        """Initialize with auth token and base URL.
        
        Args:
            token: The dbt Cloud API token. If None, will try to get from DBT_CLOUD_TOKEN env var
            base_url: The base URL for the dbt Cloud API
        """
        if token is None:
            token = os.environ.get("DBT_CLOUD_TOKEN")
            if token is None:
                raise ValueError("DBT_CLOUD_TOKEN environment variable not set and no token provided")

        self.base_url = base_url
        self.headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }
    
    def _make_request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None, 
                     data: Optional[Dict[str, Any]] = None, convert_keys: bool = True) -> Dict[str, Any]:
        """Make a request to the dbt Cloud API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (without base URL)
            params: Query parameters
            data: Request body for POST/PUT requests
            convert_keys: Whether to convert response keys to snake_case
            
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
        
        if convert_keys:
            converted_result = self._convert_keys_to_snake_case(result)
            if not isinstance(converted_result, dict):
                raise TypeError(f"Expected dict, got {type(converted_result).__name__}")
            return converted_result
        
        if not isinstance(result, dict):
            raise TypeError(f"Expected dict, got {type(result).__name__}")
        return result
        
    def _convert_keys_to_snake_case(self, obj: Any) -> Any:
        """Convert camelCase keys in the response to snake_case.
        
        Args:
            obj: The object to convert keys in (dict, list, or primitive)
            
        Returns:
            Object with converted keys
        """
        if isinstance(obj, dict):
            return {self._camel_to_snake(k): self._convert_keys_to_snake_case(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_keys_to_snake_case(item) for item in obj]
        else:
            return obj
            
    def _camel_to_snake(self, name: str) -> str:
        """Convert a camelCase string to snake_case.
        
        Args:
            name: The camelCase string
            
        Returns:
            The snake_case version
        """
        import re
        # Insert underscore before uppercase letters and convert to lowercase
        result = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
        return result
    
    def get_jobs(self, account_id: int) -> Dict[str, Any]:
        """Get jobs for a specific account.
        
        Args:
            account_id: The dbt Cloud account ID
            
        Returns:
            Dictionary containing jobs data
        """
        endpoint = f"accounts/{account_id}/jobs/"
        params = {"account_id": account_id}
        
        return self._make_request("GET", endpoint, params=params)
