from typing import List, Dict, Optional, Union
from sgqlc.operation import Operation
from services.BaseQuery import BaseQuery
from models import Model, ModelDefinition, ModelHistoricalRun
from schema.schema import DefinitionResourcesFilter


class ModelService:
    """Service for querying model data from dbt Cloud API."""
    
    def __init__(self, base_query: BaseQuery):
        """Initialize with a BaseQuery instance."""
        self.base_query = base_query
        
    def _add_model_common_fields(self, model: Operation) -> None:
        """Add fields common to both applied and definition model states."""
        fields = [
            "name", "unique_id", "description", "tags", "meta", "file_path",
            "database", "schema", "alias", "materialized_type", "fqn", "package_name"
        ]
        for field in fields:
            getattr(model, field)()
        
    def _add_model_applied_fields(self, model: Operation) -> None:
        """Add fields specific to applied state models."""
        # Add common fields
        self._add_model_common_fields(model)
        
        # Add applied-specific fields
        fields = ["contract_enforced", "language"]
        for field in fields:
            getattr(model, field)()
        
        # Add execution info fields
        execution_info = model.execution_info()
        execution_fields = [
            "last_run_id", "last_run_status", "last_success_job_definition_id",
            "last_success_run_id", "run_generated_at", "run_elapsed_time",
            "execute_completed_at", "execute_started_at", "compile_started_at",
            "compile_completed_at", "execution_time", "last_run_error"
        ]
        for field in execution_fields:
            getattr(execution_info, field)()
        
    def _add_model_definition_fields(self, model: Operation) -> None:
        """Add fields specific to definition state models."""
        # Add common fields
        self._add_model_common_fields(model)
        
        # Add definition-specific fields
        fields = [
            "resource_type", "run_generated_at", "project_id", "environment_id",
            "account_id", "contract_enforced", "language", "group", "raw_code"
        ]
        for field in fields:
            getattr(model, field)()
        
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
        general_fields = ["name", "alias", "description", "resource_type"]
        for field in general_fields:
            getattr(model_run, field)()
        
        # Conditional field groups
        field_groups = {
            'include_metadata': ["tags", "meta"],
            'include_execution': [
                "run_id", "invocation_id", "job_id", "thread_id", "run_generated_at",
                "compile_started_at", "compile_completed_at", "execute_started_at",
                "execute_completed_at", "execution_time", "run_elapsed_time"
            ],
            'include_dbt_metadata': ["environment_id", "project_id", "account_id", "owner"],
            'include_code': [
                "raw_sql", "compiled_sql", "raw_code", "compiled_code",
                "language", "database", "schema"
            ],
            'include_dependencies': ["depends_on", "parents_models", "parents_sources"],
            'include_status': ["status", "error", "skip"]
        }
        
        # Add fields based on options
        for option, fields in field_groups.items():
            if options.get(option):
                for field in fields:
                    getattr(model_run, field)()
    
    def get_models_applied(self, environment_id: int, limit: int = 300) -> List[Model]:
        """Get models from the applied state."""
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
        response = self.base_query.execute(op)
        
        # Convert to model objects
        return [Model(**node['node']) 
                for node in response['data']['environment']['applied']['models']['edges']]
    
    def get_models_definition(self, environment_id: int, limit: int = 300) -> List[ModelDefinition]:
        """Get models from the definition state."""
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
        response = self.base_query.execute(op)
        
        # Convert to model definition objects
        return [ModelDefinition(**node['node']) 
                for node in response['data']['environment']['definition']['resources']['edges']]
    
    def get_model_historical_runs(self, environment_id: int, model_name: str, 
                                 last_run_count: int = 10, 
                                 options: Optional[Dict[str, bool]] = None) -> List[ModelHistoricalRun]:
        """Get historical runs for a specific model."""
        op, applied = self.base_query.create_applied_state_query(environment_id)
        
        # Direct query for historical runs (no edges/node pattern)
        runs = applied.model_historical_runs(identifier=model_name, last_run_count=last_run_count)
        
        # Add fields based on options
        self._add_historical_run_fields(runs, options)
        
        # Execute and process response
        response = self.base_query.execute(op)
        
        # Convert to model historical run objects
        return [ModelHistoricalRun(**run) 
                for run in response['data']['environment']['applied']['model_historical_runs']]
    
    def get_model_by_name(self, environment_id: int, model_name: str, 
                          state: str = "applied") -> Optional[Union[Model, ModelDefinition]]:
        """Get a specific model by name from either applied or definition state."""
        if state.lower() == "applied":
            models = self.get_models_applied(environment_id)
            return next((model for model in models if model.name == model_name), None)
        elif state.lower() == "definition":
            models = self.get_models_definition(environment_id)
            return next((model for model in models if model.name == model_name), None)
        else:
            raise ValueError(f"Invalid state: {state}. Must be 'applied' or 'definition'.")