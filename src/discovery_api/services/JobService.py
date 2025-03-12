from typing import Dict, Any, Union, List, cast
import re
from sgqlc.operation import Operation
from src.discovery_api.services.BaseQuery import BaseQuery


class JobService:
    """Service for querying job data."""
    
    def __init__(self, base_query: BaseQuery):
        """Initialize with a BaseQuery instance."""
        self.base_query = base_query
        
    def _convert_keys_to_snake_case(self, data: Union[Dict[Any, Any], List[Any], Any]) -> Union[Dict[str, Any], List[Any], Any]:
        """Convert camelCase keys in dict or list of dicts to snake_case."""
        if isinstance(data, dict):
            new_dict: Dict[str, Any] = {}
            for key, value in data.items():
                # Convert camelCase to snake_case
                snake_key = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', str(key)).lower()
                # Recursively convert nested structures
                new_dict[snake_key] = self._convert_keys_to_snake_case(value)
            return new_dict
        elif isinstance(data, list):
            return [self._convert_keys_to_snake_case(item) for item in data]
        else:
            return data
    
    def _add_job_fields(self, job: Operation):
        """Add common job fields to the query."""
        job.id()
        job.run_id()
    
    def _add_model_fields(self, models: Operation, **kwargs):
        """
        Add model fields to the query.
        
        Args:
            models: The Operation object to add fields to
            **kwargs: Optional field groups to include:
                include_database (bool): Include database fields
                include_run_metadata (bool): Include run metadata fields
                include_timing (bool): Include execution timing fields
                include_status (bool): Include status information fields
                include_code (bool): Include code fields
                include_all (bool): Include all fields
        """
        # Check if specific field groups are explicitly set
        has_explicit_field_groups = any(
            key in kwargs for key in [
                'include_database', 'include_run_metadata', 
                'include_timing', 'include_status', 'include_code'
            ]
        )
        
        # Default field groups to include
        # If any specific field group is set, don't use include_all as default
        default_include_all = not has_explicit_field_groups
        
        include_all = kwargs.get('include_all', default_include_all)
        include_database = kwargs.get('include_database', include_all)
        include_run_metadata = kwargs.get('include_run_metadata', include_all)
        include_timing = kwargs.get('include_timing', include_all)
        include_status = kwargs.get('include_status', include_all)
        include_code = kwargs.get('include_code', include_all)
        
        # Basic model information (always included)
        models.name()
        models.unique_id()
        models.description()
        models.tags()
        models.resource_type()
        
        # Database information
        if include_database:
            models.database()
            models.schema()
            models.alias()
        
        # Run metadata
        if include_run_metadata:
            models.run_id()
            models.job_id()
            models.invocation_id()
            models.thread_id()
        
        # Execution timing
        if include_timing:
            models.run_generated_at()
            models.compile_started_at()
            models.compile_completed_at()
            models.execute_started_at()
            models.execute_completed_at()
            models.execution_time()
            models.run_elapsed_time()
        
        # Status information
        if include_status:
            models.status()
            models.error()
            models.skip()
        
        # Code fields
        if include_code:
            models.raw_sql()
            models.compiled_sql()
            models.raw_code()
            models.compiled_code()
    
    def _add_test_fields(self, tests: Operation, **kwargs):
        """
        Add test fields to the query.
        
        Args:
            tests: The Operation object to add fields to
            **kwargs: Optional field groups to include:
                include_run_metadata (bool): Include run metadata fields
                include_timing (bool): Include execution timing fields
                include_status (bool): Include status information fields
                include_code (bool): Include code fields
                include_all (bool): Include all fields
        """
        # Check if specific field groups are explicitly set
        has_explicit_field_groups = any(
            key in kwargs for key in [
                'include_run_metadata', 'include_timing', 
                'include_status', 'include_code'
            ]
        )
        
        # Default field groups to include
        # If any specific field group is set, don't use include_all as default
        default_include_all = not has_explicit_field_groups
        
        include_all = kwargs.get('include_all', default_include_all)
        include_run_metadata = kwargs.get('include_run_metadata', include_all)
        include_timing = kwargs.get('include_timing', include_all)
        include_status = kwargs.get('include_status', include_all)
        include_code = kwargs.get('include_code', include_all)
        
        # Basic test information (always included)
        tests.name()
        tests.unique_id()
        tests.description()
        tests.column_name()
        tests.tags()
        tests.resource_type()
        
        # Run metadata
        if include_run_metadata:
            tests.run_id()
            tests.job_id()
            tests.invocation_id()
        
        # Execution timing
        if include_timing:
            tests.run_generated_at()
            tests.compile_started_at()
            tests.compile_completed_at()
            tests.execute_started_at()
            tests.execute_completed_at()
            tests.execution_time()
            tests.run_elapsed_time()
        
        # Status information
        if include_status:
            tests.status()
            tests.error()
            tests.state()
            tests.warn()
            tests.fail()
            tests.skip()
        
        # Code fields
        if include_code:
            tests.raw_sql()
            tests.compiled_sql()
            tests.raw_code()
            tests.compiled_code()
    
    def get_job_metadata(self, job_id: int, **kwargs) -> Dict[str, Any]:
        """
        Get job metadata.
        
        Args:
            job_id: The ID of the job to query
            **kwargs: Additional arguments to pass to execute, such as return_query=True
            
        Returns:
            Dictionary containing job metadata
        """
        # Extract execution kwargs
        exec_kwargs = {k: v for k, v in kwargs.items() if k in ['return_query']}
        
        op, job = self.base_query.create_job_query(job_id)
        self._add_job_fields(job)
        
        response = self.base_query.execute(op, **exec_kwargs)
        result = response["data"]["job"]
            
        return cast(Dict[str, Any], self._convert_keys_to_snake_case(result))
    
    def get_job_models(self, job_id: int, **kwargs) -> Dict[str, Any]:
        """
        Get models for a specific job.
        
        Args:
            job_id: The ID of the job to query
            **kwargs: Additional arguments to pass to execute or field selection:
                include_database (bool): Include database fields
                include_run_metadata (bool): Include run metadata fields
                include_timing (bool): Include execution timing fields
                include_status (bool): Include status information fields
                include_code (bool): Include code fields
                include_all (bool): Include all fields
                return_query (bool): Return the query instead of executing it
            
        Returns:
            Dictionary containing job models data
        """
        # Extract execution kwargs from field selection kwargs
        exec_kwargs = {k: v for k, v in kwargs.items() if k in ['return_query']}
        field_kwargs = {k: v for k, v in kwargs.items() if k not in exec_kwargs}
        
        op, job = self.base_query.create_job_query(job_id)
        models = job.models()
        self._add_model_fields(models, **field_kwargs)
        
        response = self.base_query.execute(op, **exec_kwargs)
        result = response["data"]["job"]
            
        return cast(Dict[str, Any], self._convert_keys_to_snake_case(result))
    
    def get_job_tests(self, job_id: int, **kwargs) -> Dict[str, Any]:
        """
        Get tests for a specific job.
        
        Args:
            job_id: The ID of the job to query
            **kwargs: Additional arguments to pass to execute or field selection:
                include_run_metadata (bool): Include run metadata fields
                include_timing (bool): Include execution timing fields
                include_status (bool): Include status information fields
                include_code (bool): Include code fields
                include_all (bool): Include all fields
                return_query (bool): Return the query instead of executing it
            
        Returns:
            Dictionary containing job tests data
        """
        # Extract execution kwargs from field selection kwargs
        exec_kwargs = {k: v for k, v in kwargs.items() if k in ['return_query']}
        field_kwargs = {k: v for k, v in kwargs.items() if k not in exec_kwargs}
        
        op, job = self.base_query.create_job_query(job_id)
        tests = job.tests()
        self._add_test_fields(tests, **field_kwargs)
        
        response = self.base_query.execute(op, **exec_kwargs)
        result = response["data"]["job"]
            
        return cast(Dict[str, Any], self._convert_keys_to_snake_case(result))
    
    def get_job_model_by_unique_id(self, job_id: int, unique_id: str, **kwargs) -> Dict[str, Any]:
        """
        Get a specific model by unique_id from a job.
        
        Args:
            job_id: The ID of the job to query
            unique_id: The unique ID of the model to retrieve
            **kwargs: Additional arguments to pass to execute or field selection:
                include_database (bool): Include database fields
                include_run_metadata (bool): Include run metadata fields
                include_timing (bool): Include execution timing fields
                include_status (bool): Include status information fields
                include_code (bool): Include code fields
                include_all (bool): Include all fields
                return_query (bool): Return the query instead of executing it
            
        Returns:
            Dictionary containing the model data
        """
        # Extract execution kwargs from field selection kwargs
        exec_kwargs = {k: v for k, v in kwargs.items() if k in ['return_query']}
        field_kwargs = {k: v for k, v in kwargs.items() if k not in exec_kwargs}
        
        op, job = self.base_query.create_job_query(job_id)
        model = job.model(unique_id=unique_id)
        self._add_model_fields(model, **field_kwargs)
        
        response = self.base_query.execute(op, **exec_kwargs)
        result = response["data"]["job"]["model"]
        
        # Return None if model not found
        if not result:
            return None
            
        return cast(Dict[str, Any], self._convert_keys_to_snake_case(result))
    
    def get_job_test_by_unique_id(self, job_id: int, unique_id: str, **kwargs) -> Dict[str, Any]:
        """
        Get a specific test by unique_id from a job.
        
        Args:
            job_id: The ID of the job to query
            unique_id: The unique ID of the test to retrieve
            **kwargs: Additional arguments to pass to execute or field selection:
                include_run_metadata (bool): Include run metadata fields
                include_timing (bool): Include execution timing fields
                include_status (bool): Include status information fields
                include_code (bool): Include code fields
                include_all (bool): Include all fields
                return_query (bool): Return the query instead of executing it
            
        Returns:
            Dictionary containing the test data
        """
        # Extract execution kwargs from field selection kwargs
        exec_kwargs = {k: v for k, v in kwargs.items() if k in ['return_query']}
        field_kwargs = {k: v for k, v in kwargs.items() if k not in exec_kwargs}
        
        op, job = self.base_query.create_job_query(job_id)
        test = job.test(unique_id=unique_id)
        self._add_test_fields(test, **field_kwargs)
        
        response = self.base_query.execute(op, **exec_kwargs)
        result = response["data"]["job"]["test"]
        
        # Return None if test not found
        if not result:
            return None
            
        return cast(Dict[str, Any], self._convert_keys_to_snake_case(result))
    
    def get_job_with_models_and_tests(self, job_id: int, **kwargs) -> Dict[str, Any]:
        """
        Get job data with models and tests.
        
        Args:
            job_id: The ID of the job to query
            **kwargs: Additional arguments to pass to execute or field selection:
                include_database (bool): Include database fields for models
                include_run_metadata (bool): Include run metadata fields
                include_timing (bool): Include execution timing fields
                include_status (bool): Include status information fields
                include_code (bool): Include code fields
                include_all (bool): Include all fields
                return_query (bool): Return the query instead of executing it
            
        Returns:
            Dictionary containing job data with models and tests
        """
        # Extract execution kwargs from field selection kwargs
        exec_kwargs = {k: v for k, v in kwargs.items() if k in ['return_query']}
        field_kwargs = {k: v for k, v in kwargs.items() if k not in exec_kwargs}
        
        op, job = self.base_query.create_job_query(job_id)
        
        # Add job fields
        self._add_job_fields(job)
        
        # Add models data
        models = job.models()
        self._add_model_fields(models, **field_kwargs)
        
        # Add tests data
        tests = job.tests()
        self._add_test_fields(tests, **field_kwargs)
        
        response = self.base_query.execute(op, **exec_kwargs)
        result = response["data"]["job"]
            
        return cast(Dict[str, Any], self._convert_keys_to_snake_case(result))
