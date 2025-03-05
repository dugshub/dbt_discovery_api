"""
DBT Discovery API Demo

This demonstrates using the high-level API layer instead of raw GraphQL queries.
"""

import os
import json
from src.discovery_api.api import DiscoveryAPI

# Utility function for formatted printing
def print_section(title):
    """Print a section header with formatting."""
    print(f"\n=== {title} ===\n")

def print_code_example(code_snippet):
    """Print a code example with formatting."""
    print(f"# Python code:\n{code_snippet}")

def print_item(label, value, indent=0):
    """Print a labeled item with proper formatting."""
    indent_str = "  " * indent
    if value is None or value == '':
        value = 'Not specified'
    print(f"{indent_str}{label}: {value}")

def print_json(data):
    """Pretty print a JSON object."""
    print(json.dumps(data, indent=2, default=str))

# Get environment and job IDs from environment variables
sandbox_environment_id = int(os.environ.get('ENV_ID_SANDBOX_PRODUCTION'))
mart_environment_id = int(os.environ.get('ENV_ID_MART_PRODUCTION'))

# Initialize the API with your DBT Cloud token
api = DiscoveryAPI(token=os.getenv("DBT_SERVICE_TOKEN"))

def demo_project_metadata():
    """Demonstrate getting project metadata."""
    print_section("Project Metadata")
    
    # Get project by environment ID
    print_code_example("project = api.project(environment_id=sandbox_environment_id)")
    project = api.project(environment_id=sandbox_environment_id)
    
    # Get project metadata
    print_code_example("metadata = project.get_metadata()")
    metadata = project.get_metadata()
    
    # Print project information
    print()
    print_item("Project Name", metadata.dbt_project_name)
    print_item("Adapter Type", metadata.adapter_type)
    print_item("Environment ID", metadata.environment_id)

def demo_model_list():
    """Demonstrate getting all models in a project."""
    print_section("Models List")
    
    # Get project by environment ID
    print_code_example("project = api.project(environment_id=sandbox_environment_id)")
    project = api.project(environment_id=sandbox_environment_id)
    
    # Get all models
    print_code_example("models = project.get_models()")
    models = project.get_models()
    
    # Print models count
    print()
    print_item("Found", f"{len(models)} models")
    
    # Print first 5 models
    print("\nFirst 5 models:")
    for i, model in enumerate(models[:5]):
        print_item(f"{i+1}. {model.metadata.name}", f"({model.metadata.materialized or 'unknown type'})")

def demo_model_detail():
    """Demonstrate getting a specific model's details."""
    print_section("Model Detail")
    
    model_name = 'bd_deal_actuals'  # Use a model name from your project
    
    # Get project by environment ID
    print_code_example("project = api.project(environment_id=sandbox_environment_id)")
    project = api.project(environment_id=sandbox_environment_id)
    
    try:
        # Get specific model by name
        print_code_example(f"model = project.get_model('{model_name}')")
        model = project.get_model(model_name)
        
        # Print model metadata
        print()
        print_item("Model Name", model.metadata.name)
        print_item("Unique ID", model.metadata.unique_id)
        print_item("Database", model.metadata.database)
        print_item("Schema", model.metadata.schema)
        print_item("Description", model.metadata.description)
        print_item("Materialized Type", model.metadata.materialized)
        print_item("Tags", ', '.join(model.metadata.tags) if model.metadata.tags else 'No tags')
        
        # Get and print last run status
        if model.last_run:
            print()
            print_item("Last Run Status", model.last_run.status)
            print_item("Run ID", model.last_run.run_id)
            print_item("Run Time", model.last_run.run_time)
            print_item("Execution Time", f"{model.last_run.execution_time or 'Unknown'} seconds")
            if model.last_run.error_message:
                print_item("Error", model.last_run.error_message)
        else:
            print("\nNo run history available")
    
    except ValueError as e:
        print(f"Error: {str(e)}")

def demo_model_runs():
    """Demonstrate getting historical runs for a model."""
    print_section("Model Historical Runs")
    
    model_name = 'bd_deal_actuals'  # Use a model name from your project
    
    # Get project by environment ID
    print_code_example("project = api.project(environment_id=sandbox_environment_id)")
    project = api.project(environment_id=sandbox_environment_id)
    
    try:
        # Get historical runs directly from project
        print_code_example(f"runs = project.get_model_historical_runs('{model_name}', limit=5)")
        runs = project.get_model_historical_runs(model_name, limit=5)
        
        # Print runs information
        print()
        print_item("Found", f"{len(runs)} historical runs for model '{model_name}'")
        
        # Print details for each run
        for i, run in enumerate(runs):
            print(f"\nRun {i+1}:")
            print_item("Status", run.status, indent=1)
            print_item("Run ID", run.run_id, indent=1)
            print_item("Run Time", run.run_time, indent=1)
            print_item("Execution Time", f"{run.execution_time or 'Unknown'} seconds", indent=1)
            if run.error_message:
                print_item("Error", run.error_message, indent=1)
    
    except ValueError as e:
        print(f"Error: {str(e)}")

def demo_model_to_dict():
    """Demonstrate converting a model to a dictionary."""
    print_section("Model to Dictionary")
    
    model_name = 'bd_deal_actuals'  # Use a model name from your project
    
    # Get project by environment ID
    print_code_example("project = api.project(environment_id=sandbox_environment_id)")
    project = api.project(environment_id=sandbox_environment_id)
    
    try:
        # Get specific model by name
        print_code_example(f"model = project.get_model('{model_name}')")
        model = project.get_model(model_name)
        
        # Convert model to dictionary
        print_code_example("model_dict = model.to_dict()")
        model_dict = model.to_dict()
        
        # Print dictionary representation
        print_code_example("print(json.dumps(model_dict, indent=2, default=str))")
        print()
        print_json(model_dict)
    
    except ValueError as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Run all demos
    demo_project_metadata()
    demo_model_list()
    demo_model_detail()
    demo_model_runs()
    demo_model_to_dict()
