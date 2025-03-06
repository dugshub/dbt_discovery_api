from typing import Optional, Tuple, Dict, Any
from sgqlc.endpoint.http import HTTPEndpoint
from sgqlc.operation import Operation
from src.discovery_api.schema import schema
import os
import logging
import time


# Configure logging - use a stream handler to ensure output is visible in pytest
logger = logging.getLogger("dbt_discovery_api")

# Get log level from environment variable, default to WARNING if not specified
log_level_name = os.environ.get("DBT_DISCOVERY_LOG_LEVEL", "WARNING").upper()
log_level = getattr(logging, log_level_name, logging.WARNING)
logger.setLevel(log_level)

# Only add handler if it doesn't already have handlers to avoid duplicates
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    # Prevent propagation to avoid duplicate logs
    logger.propagate = False


class BaseQuery:
    """Base class for handling all GraphQL interactions."""

    def __init__(self, token: Optional[str] = None, endpoint: str = "https://metadata.cloud.getdbt.com/graphql"):
        """Initialize with auth token and endpoint."""
        if token is None:
            token = os.environ.get("DBT_SERVICE_TOKEN")
            if token is None:
                raise ValueError("DBT_SERVICE_TOKEN environment variable not set and no token provided")

        self.client = HTTPEndpoint(endpoint, {'Authorization': f'Bearer {token}'})
        logger.info(f"Initialized BaseQuery with endpoint: {endpoint}")
        
    def execute(self, operation: Operation, return_query: bool = False) -> Dict[str, Any]:
        """
        Execute a GraphQL operation and return the response.
        
        Args:
            operation: The GraphQL operation to execute
            return_query: If True, include the GraphQL query in the response
            
        Returns:
            Dictionary containing the response, with the query included if return_query is True
        """
        logger.info(f"Executing GraphQL operation, query length: {len(str(operation))}")
        start_time = time.time()
        
        try:
            # Add timing for the HTTP request itself
            http_start_time = time.time()
            result = self.client(operation)
            http_time = time.time() - http_start_time
            total_execution_time = time.time() - start_time
            
            logger.info(f"GraphQL HTTP request took {http_time:.3f} seconds")
            logger.info(f"GraphQL execution completed `in {total_execution_time:.3f} seconds")
            
            # Set a reasonable threshold for slow query warnings
            # Adjust this value based on your performance expectations
            if total_execution_time > 1.0:
                logger.warning(f"Slow GraphQL query detected: {total_execution_time:.3f} seconds")
                logger.warning(f"HTTP portion of slow query: {http_time:.3f} seconds")
                # Log a truncated version of the query for slow operations
                query_str = str(operation)
                if len(query_str) > 200:
                    logger.warning(f"Slow query beginning: {query_str[:200]}..."
                                    f"(total length: {len(query_str)})")
                else:
                    logger.warning(f"Slow query: {query_str}")
                
            if return_query:
                # Create a copy of the result to avoid modifying the original response
                response_with_query = dict(result)
                # Add the GraphQL query to the response
                response_with_query["query"] = str(operation)
                return response_with_query
                
            return dict(result)  # Ensure we return a Dict[str, Any]
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"GraphQL execution failed after {execution_time:.3f} seconds: {str(e)}")
            raise
    
    def create_operation(self) -> Operation:
        """Create a new GraphQL operation."""
        logger.debug("Creating new GraphQL operation")
        return Operation(schema.schema.Query)
    
    # Precanned, isolated queries for common operations
    def create_environment_query(self, environment_id: int) -> Tuple[Operation, Any]:
        """Create a query for environment data."""
        logger.debug(f"Creating environment query for environment_id: {environment_id}")
        start_time = time.time()
        op = self.create_operation()
        env = op.environment(id=environment_id)
        logger.debug(f"Environment query creation completed in {time.time() - start_time:.3f} seconds")
        return op, env

    def create_applied_state_query(self, environment_id: int) -> Tuple[Operation, Any]:
        """Create a query for applied state data."""
        logger.debug(f"Creating applied state query for environment_id: {environment_id}")
        start_time = time.time()
        op = self.create_operation()
        applied = op.environment(id=environment_id).applied
        logger.debug(f"Applied state query creation completed in {time.time() - start_time:.3f} seconds")
        return op, applied

    def create_definition_state_query(self, environment_id: int) -> Tuple[Operation, Any]:
        """Create a query for definition state data."""
        logger.debug(f"Creating definition state query for environment_id: {environment_id}")
        start_time = time.time()
        op = self.create_operation()
        definition = op.environment(id=environment_id).definition
        logger.debug(f"Definition state query creation completed in {time.time() - start_time:.3f} seconds")
        return op, definition
        
    def create_job_query(self, job_id: int) -> Tuple[Operation, Any]:
        """Create a query for job data."""
        logger.debug(f"Creating job query for job_id: {job_id}")
        start_time = time.time()
        op = self.create_operation()
        job = op.job(id=job_id)
        logger.debug(f"Job query creation completed in {time.time() - start_time:.3f} seconds")
        return op, job

    # Utility functions for creating customized queries with the BaseQuery class
    def _add_environment_query(self, op: Operation, environment_id: int, alias: Optional[str] = None) -> Tuple[Operation, Any]:
        """Add environment fields to the query."""
        logger.debug(f"Adding environment query for environment_id: {environment_id}, alias: {alias}")
        start_time = time.time()
        # The sgqlc library handles the conversion from int to the appropriate type
        kwargs: Dict[str, Any] = {"id": environment_id}
        if alias:
            kwargs["__alias__"] = alias
        environment = op.environment(**kwargs)
        logger.debug(f"Environment query addition completed in {time.time() - start_time:.3f} seconds")
        return op, environment
        
    def _add_job_query(self, op: Operation, job_id: int, alias: Optional[str] = None) -> Tuple[Operation, Any]:
        """Add job fields to the query."""
        logger.debug(f"Adding job query for job_id: {job_id}, alias: {alias}")
        start_time = time.time()
        # The sgqlc library handles the conversion from int to the appropriate type
        kwargs: Dict[str, Any] = {"id": job_id}
        if alias:
            kwargs["__alias__"] = alias
        job = op.job(**kwargs)
        logger.debug(f"Job query addition completed in {time.time() - start_time:.3f} seconds")
        return op, job

    def _add_applied_query(self, op: Operation, environment_id: int, alias: Optional[str] = None) -> Tuple[Operation, Any]:
        """Add applied state fields to the query."""
        logger.debug(f"Adding applied query for environment_id: {environment_id}, alias: {alias}")
        start_time = time.time()
        # The sgqlc library handles the conversion from int to the appropriate type
        kwargs: Dict[str, Any] = {"id": environment_id}
        if alias:
            kwargs["__alias__"] = alias
        applied = op.environment(**kwargs).applied
        logger.debug(f"Applied query addition completed in {time.time() - start_time:.3f} seconds")
        return op, applied

    def _add_definition_query(self, op: Operation, environment_id: int, alias: Optional[str] = None) -> Tuple[Operation, Any]:
        """Add definition state fields to the query."""
        logger.debug(f"Adding definition query for environment_id: {environment_id}, alias: {alias}")
        start_time = time.time()
        # The sgqlc library handles the conversion from int to the appropriate type
        kwargs: Dict[str, Any] = {"id": environment_id}
        if alias:
            kwargs["__alias__"] = alias
        definition = op.environment(**kwargs).definition
        logger.debug(f"Definition query addition completed in {time.time() - start_time:.3f} seconds")
        return op, definition