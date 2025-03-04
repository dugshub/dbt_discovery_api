from typing import Dict, Any, Union
import re
from sgqlc.operation import Operation
from src.services.BaseQuery import BaseQuery


class EnvironmentService:
    """Service for querying environment data."""
    
    def __init__(self, base_query: BaseQuery):
        """Initialize with a BaseQuery instance."""
        self.base_query = base_query
        
    def _convert_keys_to_snake_case(self, data: Union[Dict, list, Any]) -> Union[Dict, list, Any]:
        """Convert camelCase keys in dict or list of dicts to snake_case."""
        if isinstance(data, dict):
            new_dict = {}
            for key, value in data.items():
                # Convert camelCase to snake_case
                snake_key = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', key).lower()
                # Recursively convert nested structures
                new_dict[snake_key] = self._convert_keys_to_snake_case(value)
            return new_dict
        elif isinstance(data, list):
            return [self._convert_keys_to_snake_case(item) for item in data]
        else:
            return data
        
    def _add_environment_fields(self, environment: Operation):
        """Add common environment fields to the query."""
        environment.dbt_project_name()
        environment.adapter_type()
        
    def _add_applied_fields(self, applied: Operation):
        """Add Applied state fields to the query."""
        applied.last_updated_at()
        applied.resource_counts()
        applied.latest_git_sha()
        
    def _add_definition_fields(self, definition: Operation):
        """Add Definition state fields to the query."""
        definition.last_updated_at()
        definition.resource_counts()
        
    def get_environment_metadata(self, environment_id: int) -> Dict[str, Any]:
        """Get environment metadata."""
        op, env = self.base_query.create_environment_query(environment_id)
        self._add_environment_fields(env)
        
        response = self.base_query.execute(op)
        result = response["data"]["environment"]
        return self._convert_keys_to_snake_case(result)
    
    def get_applied_state(self, environment_id: int) -> Dict[str, Any]:
        """Get the applied state of the environment."""
        op, applied = self.base_query.create_applied_state_query(environment_id)
        self._add_applied_fields(applied)
        
        response = self.base_query.execute(op)
        result = response["data"]["environment"]["applied"]
        return self._convert_keys_to_snake_case(result)
    
    def get_definition_state(self, environment_id: int) -> Dict[str, Any]:
        """Get the definition state of the environment."""
        op, definition = self.base_query.create_definition_state_query(environment_id)
        self._add_definition_fields(definition)
        
        response = self.base_query.execute(op)
        result = response["data"]["environment"]["definition"]
        return self._convert_keys_to_snake_case(result)