from typing import List, Dict, Optional, Union, Any
from sgqlc.operation import Operation
from src.discovery_api.services.BaseQuery import BaseQuery
from src.discovery_api.models import Model, ModelDefinition, ModelHistoricalRun
from src.discovery_api.schema.schema import DefinitionResourcesFilter


class ModelService:
    """Service for querying model data from dbt Cloud API."""
    
    def __init__(self, base_query: BaseQuery):
        """Initialize with a BaseQuery instance."""
        self.base_query = base_query
        
    def _transform_field_names(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform GraphQL camelCase field names to Python snake_case for Pydantic models.
        
        This is a temporary solution. Future improvement:
        - Use the schema types directly as inputs/outputs 
        - Or create response objects using the schema types before converting to Pydantic models
        """
        result = {}
        
        # Map of common GraphQL camelCase to Python snake_case field names
        field_map = {
            'uniqueId': 'unique_id',
            'filePath': 'file_path',
            'resourceType': 'resource_type',
            'runGeneratedAt': 'run_generated_at', 
            'projectId': 'project_id',
            'environmentId': 'environment_id',
            'accountId': 'account_id',
            'materializedType': 'materialized_type',
            'packageName': 'package_name',
            'rawCode': 'raw_code',
            'contractEnforced': 'contract_enforced',
            'executionInfo': 'execution_info',
            'lastRunId': 'last_run_id',
            'lastRunStatus': 'last_run_status',
            'lastSuccessJobDefinitionId': 'last_success_job_definition_id',
            'lastSuccessRunId': 'last_success_run_id',
            'runElapsedTime': 'run_elapsed_time',
            'executeCompletedAt': 'execute_completed_at',
            'executeStartedAt': 'execute_started_at',
            'compileStartedAt': 'compile_started_at',
            'compileCompletedAt': 'compile_completed_at',
            'executionTime': 'execution_time',
            'lastRunError': 'last_run_error'
        }
        
        # Transform keys using the mapping
        for key, value in data.items():
            new_key = field_map.get(key, key)
            
            # Handle nested dictionaries
            if isinstance(value, dict):
                result[new_key] = self._transform_field_names(value)
            else:
                result[new_key] = value
                
        return result
        
    def _add_model_common_fields(self, model: Operation) -> None:
        """Add fields common to both applied and definition model states."""
        # Basic information
        model.name()
        model.unique_id()
        model.description()
        model.tags()
        model.meta()
        model.file_path()
        
    def _add_model_applied_fields(self, model: Operation) -> None:
        """Add fields specific to applied state models."""
        # Add common fields
        self._add_model_common_fields(model)
        
        # Add database information for applied state
        try:
            model.database()
            model.schema()
            model.alias()
            model.materialized_type()
            model.fqn()
            model.package_name()
        except Exception:
            # These fields might not be available in all GraphQL schemas
            pass
        
        # Add applied-specific fields
        try:
            model.contract_enforced()
            model.language()
        except Exception:
            # These fields might not be available in all GraphQL schemas
            pass
        
        # Add execution info fields
        try:
            execution_info = model.execution_info()
            
            # Run information
            execution_info.last_run_id()
            execution_info.last_run_status()
            execution_info.last_success_job_definition_id()
            execution_info.last_success_run_id()
            
            # Run timing
            execution_info.run_generated_at()
            execution_info.run_elapsed_time()
            
            # Execution timing
            execution_info.execute_completed_at()
            execution_info.execute_started_at()
            execution_info.compile_started_at()
            execution_info.compile_completed_at()
            execution_info.execution_time()
            
            # Error information
            execution_info.last_run_error()
        except Exception:
            # execution_info might not be available in all GraphQL schemas
            pass
        
    def _add_model_definition_fields(self, model: Operation) -> None:
        """Add fields specific to definition state models."""
        # Add common fields
        self._add_model_common_fields(model)
        
        # Add definition-specific fields
        try:
            model.resource_type()
            model.run_generated_at()
            model.project_id()
            model.environment_id()
            model.account_id()
        except Exception:
            # These fields might not be available in all GraphQL schemas
            pass
            
        # Try to add database fields that might be available in definition state
        try:
            model.database()
            model.schema()
            model.alias()
            model.materialized_type()
            model.fqn()
            model.package_name()
        except Exception:
            # These fields might not be available in all GraphQL schemas
            pass
            
        # Other optional fields
        try:
            model.contract_enforced()
            model.language()
            model.group()
            model.raw_code()
        except Exception:
            # These fields might not be available in all GraphQL schemas
            pass
        
    def _add_historical_run_fields(self, model_run: Operation, options: Optional[Dict[str, bool]] = None) -> None:
        """Add fields to a historical run query based on options."""
        options = options or {
            'include_metadata': True,
            'include_execution': True,
            'include_dbt_metadata': False,
            'include_code': False,
            'include_dependencies': False,
            'include_status': True
        }
        
        # Always included general information
        model_run.name()
        model_run.alias()
        model_run.description()
        model_run.resource_type()
        
        # Conditional fields based on options
        
        # Metadata fields
        if options.get('include_metadata'):
            model_run.tags()
            model_run.meta()
        
        # Execution fields
        if options.get('include_execution'):
            model_run.run_id()
            model_run.invocation_id()
            model_run.job_id()
            model_run.thread_id()
            model_run.run_generated_at()
            model_run.compile_started_at()
            model_run.compile_completed_at()
            model_run.execute_started_at()
            model_run.execute_completed_at()
            model_run.execution_time()
            model_run.run_elapsed_time()
        
        # DBT metadata fields
        if options.get('include_dbt_metadata'):
            model_run.environment_id()
            model_run.project_id()
            model_run.account_id()
            model_run.owner()
        
        # Code fields
        if options.get('include_code'):
            model_run.raw_sql()
            model_run.compiled_sql()
            model_run.raw_code()
            model_run.compiled_code()
            model_run.language()
            model_run.database()
            model_run.schema()
        
        # Dependency fields
        if options.get('include_dependencies'):
            model_run.depends_on()
            model_run.parents_models()
            model_run.parents_sources()
        
        # Status fields
        if options.get('include_status'):
            model_run.status()
            model_run.error()
            model_run.skip()
    
    def get_models_applied(self, environment_id: int, limit: int = 300, **kwargs) -> List[Model]:
        """
        Get models from the applied state.
        
        Args:
            environment_id: The ID of the environment to query
            limit: Maximum number of models to return
            **kwargs: Additional arguments to pass to execute, such as return_query=True
            
        Returns:
            List of Model objects
        """
        op, applied = self.base_query.create_applied_state_query(environment_id)
        
        # Query models with pagination
        models = applied.models(first=limit)
        
        # Add page info
        page_info = models.page_info()
        page_info.has_next_page()
        page_info.has_previous_page()
        
        # Add model fields via edges->node pattern
        model_node = models.edges.node()
        self._add_model_applied_fields(model_node)
        
        # Execute and process response
        response = self.base_query.execute(op, **kwargs)
        
        # Convert to model objects
        result = []
        for node in response['data']['environment']['applied']['models']['edges']:
            # Transform GraphQL camelCase to Python snake_case
            node_data = self._transform_field_names(node['node'])
            result.append(Model(**node_data))
        return result
    
    def get_models_definition(self, environment_id: int, limit: int = 300, **kwargs) -> List[ModelDefinition]:
        """
        Get models from the definition state.
        
        Args:
            environment_id: The ID of the environment to query
            limit: Maximum number of models to return
            **kwargs: Additional arguments to pass to execute, such as return_query=True
            
        Returns:
            List of ModelDefinition objects
        """
        # Create filter for model resources
        resource_filter = DefinitionResourcesFilter(types=["Model"])
        
        op, definition = self.base_query.create_definition_state_query(environment_id)
        
        # Query resources with filter and pagination
        resources = definition.resources(filter=resource_filter, first=limit)
        
        # Add page info
        page_info = resources.page_info()
        page_info.has_next_page()
        page_info.has_previous_page()
        
        # Add model definition fields
        model_node = resources.edges.node()
        self._add_model_definition_fields(model_node)
        
        # Execute and process response
        response = self.base_query.execute(op, **kwargs)
        
        # Convert to model definition objects
        result = []
        for node in response['data']['environment']['definition']['resources']['edges']:
            # Transform GraphQL camelCase to Python snake_case
            node_data = self._transform_field_names(node['node'])
            result.append(ModelDefinition(**node_data))
        return result
    
    def get_model_historical_runs(self, environment_id: int, model_name: str, 
                                  last_run_count: int = 10, 
                                  options: Optional[Dict[str, bool]] = None,
                                  **kwargs) -> List[ModelHistoricalRun]:
        """
        Get historical runs for a specific model.
        
        Args:
            environment_id: The ID of the environment to query
            model_name: The name of the model to query
            last_run_count: Number of historical runs to fetch
            options: Query options for field selection
            **kwargs: Additional arguments to pass to execute, such as return_query=True
            
        Returns:
            List of ModelHistoricalRun objects
        """
        op, applied = self.base_query.create_applied_state_query(environment_id)
        
        # Direct query for historical runs (no edges/node pattern)
        # GraphQL field name may be modelHistoricalRuns (camelCase)
        try:
            runs = applied.model_historical_runs(identifier=model_name, last_run_count=last_run_count)
        except AttributeError:
            # Try camelCase version if snake_case doesn't work
            runs = applied.modelHistoricalRuns(identifier=model_name, lastRunCount=last_run_count)
        
        # Add fields based on options
        self._add_historical_run_fields(runs, options)
        
        # Execute and process response
        response = self.base_query.execute(op, **kwargs)
        
        # Figure out which key the API is using
        api_key = None
        if 'data' in response and 'environment' in response['data'] and 'applied' in response['data']['environment']:
            applied_data = response['data']['environment']['applied']
            if 'model_historical_runs' in applied_data:
                api_key = 'model_historical_runs'
            elif 'modelHistoricalRuns' in applied_data:
                api_key = 'modelHistoricalRuns'
        
        # Return empty list if we can't find the data
        if not api_key or not response['data']['environment']['applied'].get(api_key):
            return []
            
        # Convert to model historical run objects
        result = []
        for run in response['data']['environment']['applied'][api_key]:
            # Transform GraphQL camelCase to Python snake_case
            run_data = self._transform_field_names(run)
            result.append(ModelHistoricalRun(**run_data))
        return result
        
    def get_multiple_models_historical_runs(self, environment_id: int, model_names: List[str],
                                          last_run_count: int = 5,
                                          options: Optional[Dict[str, bool]] = None,
                                          **kwargs) -> Dict[str, List[ModelHistoricalRun]]:
        """
        Get historical runs for multiple models in a single query using aliasing.
        
        This method creates a batched query with aliases for each model to reduce API calls.
        
        Args:
            environment_id: The dbt Cloud environment ID
            model_names: List of model names to fetch
            last_run_count: Number of historical runs to fetch for each model
            options: Query options for field selection
            **kwargs: Additional arguments to pass to execute, such as return_query=True
            
        Returns:
            Dictionary mapping model names to their historical runs
        """
        if not model_names:
            return {}
            
        # Create a new operation
        op = self.base_query.create_operation()
        
        # Get the environment node but don't add it to the operation yet
        env = op.environment(id=environment_id)
        applied = env.applied
        
        # Add aliased queries for each model
        for i, model_name in enumerate(model_names):
            # Create a unique alias for each model
            alias = f"model_{i}"
            
            # Add the aliased query to fetch historical runs
            try:
                runs = applied.model_historical_runs(__alias__=alias, identifier=model_name, last_run_count=last_run_count)
            except AttributeError:
                # Try camelCase version if snake_case doesn't work
                runs = applied.modelHistoricalRuns(__alias__=alias, identifier=model_name, lastRunCount=last_run_count)
            
            # Add fields based on options
            self._add_historical_run_fields(runs, options)
        
        # Execute the consolidated query
        response = self.base_query.execute(op, **kwargs)
        
        # Process the response
        result = {}
        if 'data' in response and 'environment' in response['data'] and 'applied' in response['data']['environment']:
            applied_data = response['data']['environment']['applied']
            
            # Process each aliased model result
            for i, model_name in enumerate(model_names):
                alias = f"model_{i}"
                
                # Look for results under the alias in both possible formats
                model_data = None
                if alias in applied_data:
                    model_data = applied_data[alias]
                
                if model_data:
                    # Convert to model historical run objects
                    model_results = []
                    for run in model_data:
                        # Transform GraphQL camelCase to Python snake_case
                        run_data = self._transform_field_names(run)
                        model_results.append(ModelHistoricalRun(**run_data))
                    
                    result[model_name] = model_results
                else:
                    # No data found for this model
                    result[model_name] = []
        
        return result
    
    def get_model_by_name(self, environment_id: int, model_name: str, 
                          state: str = "applied", **kwargs) -> Optional[Union[Model, ModelDefinition]]:
        """
        Get a specific model by name from either applied or definition state.
        
        Args:
            environment_id: The ID of the environment to query
            model_name: The name of the model to query
            state: The state to query (applied or definition)
            **kwargs: Additional arguments to pass to execute, such as return_query=True
            
        Returns:
            Model or ModelDefinition object, or None if not found
        """
        
        if state.lower() == "applied":
            applied_models = self.get_models_applied(environment_id, **kwargs)
            return next((model for model in applied_models if model.name == model_name), None)
        
        elif state.lower() == "definition":
            definition_models = self.get_models_definition(environment_id, **kwargs)
            return next((model for model in definition_models if model.name == model_name), None)
        
        else:
            raise ValueError(f"Invalid state: {state}. Must be 'applied' or 'definition'.")


# Field Assignment Approach Conversion Summary
# --------------------------------------------
# This file has been updated to use direct method calling for field assignments instead of
# the list-based approach. This change offers several benefits:
#
# 1. BEFORE (List-Based Approach):
#    ```python
#    fields = ["name", "unique_id", "description"]
#    for field in fields:
#        getattr(model, field)()
#    ```
#
# 2. AFTER (Direct Method Calling):
#    ```python
#    model.name()
#    model.unique_id()
#    model.description()
#    ```
#
# Benefits of Direct Method Calling:
# - Improved readability with explicit field assignments
# - Better IDE support for code completion and refactoring
# - Type safety as errors are caught at compile time rather than runtime
# - More maintainable as fields are logically grouped with comments
#
# This approach also makes the code more consistent across the ModelService class
# and follows modern Python programming practices.