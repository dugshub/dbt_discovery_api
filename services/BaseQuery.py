from typing import Optional, Tuple, Dict, Any
from sgqlc.endpoint.http import HTTPEndpoint
from sgqlc.operation import Operation
from schema import schema
import os


class BaseQuery:
    """Base class for handling all GraphQL interactions."""

    def __init__(self, token: Optional[str] = None, endpoint: str = "https://metadata.cloud.getdbt.com/graphql"):
        """Initialize with auth token and endpoint."""
        if token is None:
            token = os.environ.get("DBT_SERVICE_TOKEN")
            if token is None:
                raise ValueError("DBT_SERVICE_TOKEN environment variable not set and no token provided")

        self.client = HTTPEndpoint(endpoint, {'Authorization': f'Bearer {token}'})
        
    def execute(self, operation: Operation) -> Dict[str, Any]:
        """Execute a GraphQL operation and return the response."""
        return self.client(operation)
    
    def create_operation(self) -> Operation:
        """Create a new GraphQL operation."""
        return Operation(schema.schema.Query)
    
    # Precanned, isolated queries for common operations
    def create_environment_query(self, environment_id: int) -> Tuple[Operation, Any]:
        """Create a query for environment data."""
        op = self.create_operation()
        env = op.environment(id=environment_id)
        return op, env

    def create_applied_state_query(self, environment_id: int) -> Tuple[Operation, Any]:
        """Create a query for applied state data."""
        op = self.create_operation()
        applied = op.environment(id=environment_id).applied
        return op, applied

    def create_definition_state_query(self, environment_id: int) -> Tuple[Operation, Any]:
        """Create a query for definition state data."""
        op = self.create_operation()
        definition = op.environment(id=environment_id).definition
        return op, definition

    # Utility functions for creating customized queries with the BaseQuery class
    def _add_environment_query(self, op: Operation, environment_id: int, alias: Optional[str] = None) -> Tuple[Operation, Any]:
        """Add environment fields to the query."""
        kwargs = {"id": environment_id}
        if alias:
            kwargs["__alias__"] = alias
        environment = op.environment(**kwargs)
        return op, environment

    def _add_applied_query(self, op: Operation, environment_id: int, alias: Optional[str] = None) -> Tuple[Operation, Any]:
        """Add applied state fields to the query."""
        kwargs = {"id": environment_id}
        if alias:
            kwargs["__alias__"] = alias
        applied = op.environment(**kwargs).applied
        return op, applied

    def _add_definition_query(self, op: Operation, environment_id: int, alias: Optional[str] = None) -> Tuple[Operation, Any]:
        """Add definition state fields to the query."""
        kwargs = {"id": environment_id}
        if alias:
            kwargs["__alias__"] = alias
        definition = op.environment(**kwargs).definition
        return op, definition