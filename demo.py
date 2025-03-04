"""
DBT Discovery API Demo

This demonstrates using the high-level API layer instead of raw GraphQL queries.
"""

import os
from src.api import DiscoveryAPI

# Get environment and job IDs from environment variables
sandbox_environment_id = int(os.environ.get('ENV_ID_SANDBOX_PRODUCTION'))
mart_environment_id = int(os.environ.get('ENV_ID_MART_PRODUCTION'))

# Initialize the API with your DBT Cloud token
api = DiscoveryAPI(token=os.getenv("DBT_SERVICE_TOKEN"))

def demo_project_metadata():
    """Demonstrate getting project metadata."""
    print("\n=== Project Metadata ===\n")
    
    # Get project by environment ID
    project = api.project(environment_id=sandbox_environment_id)
    
    # Get project metadata
    metadata = project.get_metadata()
    
    # Print project information
    print(f"Project Name: {metadata.dbt_project_name}")
    print(f"Adapter Type: {metadata.adapter_type}")
    print(f"Environment ID: {metadata.environment_id}")

def demo_model_list():
    """Demonstrate getting all models in a project."""
    print("\n=== Models List ===\n")
    
    # Get project by environment ID
    project = api.project(environment_id=sandbox_environment_id)
    
    # Get all models
    models = project.get_models()
    
    # Print models count
    print(f"Found {len(models)} models")
    
    # Print first 5 models
    print("\nFirst 5 models:")
    for i, model in enumerate(models[:5]):
        print(f"{i+1}. {model.metadata.name} ({model.metadata.materialized or 'unknown type'})")

def demo_model_detail():
    """Demonstrate getting a specific model's details."""
    print("\n=== Model Detail ===\n")
    
    model_name = 'bd_deal_actuals'  # Use a model name from your project
    
    # Get project by environment ID
    project = api.project(environment_id=sandbox_environment_id)
    
    try:
        # Get specific model by name
        model = project.get_model(model_name)
        
        # Print model metadata
        print(f"Model Name: {model.metadata.name}")
        print(f"Unique ID: {model.metadata.unique_id}")
        print(f"Database: {model.metadata.database or 'Not specified'}")
        print(f"Schema: {model.metadata.schema or 'Not specified'}")
        print(f"Description: {model.metadata.description or 'No description'}")
        print(f"Materialized Type: {model.metadata.materialized or 'Unknown'}")
        print(f"Tags: {', '.join(model.metadata.tags) if model.metadata.tags else 'No tags'}")
        
        # Get and print last run status
        if model.last_run:
            print(f"\nLast Run Status: {model.last_run.status or 'Unknown'}")
            print(f"Run ID: {model.last_run.run_id or 'Unknown'}")
            print(f"Run Time: {model.last_run.run_time}")
            print(f"Execution Time: {model.last_run.execution_time or 'Unknown'} seconds")
            if model.last_run.error_message:
                print(f"Error: {model.last_run.error_message}")
        else:
            print("\nNo run history available")
    
    except ValueError as e:
        print(f"Error: {str(e)}")

def demo_model_runs():
    """Demonstrate getting historical runs for a model."""
    print("\n=== Model Historical Runs ===\n")
    
    model_name = 'bd_deal_actuals'  # Use a model name from your project
    
    # Get project by environment ID
    project = api.project(environment_id=sandbox_environment_id)
    
    try:
        # Get historical runs directly from project
        runs = project.get_model_historical_runs(model_name, limit=5)
        
        # Print runs information
        print(f"Found {len(runs)} historical runs for model '{model_name}'")
        
        # Print details for each run
        for i, run in enumerate(runs):
            print(f"\nRun {i+1}:")
            print(f"  Status: {run.status or 'Unknown'}")
            print(f"  Run ID: {run.run_id or 'Unknown'}")
            print(f"  Run Time: {run.run_time}")
            print(f"  Execution Time: {run.execution_time or 'Unknown'} seconds")
            if run.error_message:
                print(f"  Error: {run.error_message}")
    
    except ValueError as e:
        print(f"Error: {str(e)}")

def demo_model_to_dict():
    """Demonstrate converting a model to a dictionary."""
    print("\n=== Model to Dictionary ===\n")
    
    model_name = 'bd_deal_actuals'  # Use a model name from your project
    
    # Get project by environment ID
    project = api.project(environment_id=sandbox_environment_id)
    
    try:
        # Get specific model by name
        model = project.get_model(model_name)
        
        # Convert model to dictionary
        model_dict = model.to_dict()
        
        # Print dictionary representation
        import json
        print(json.dumps(model_dict, indent=2, default=str))
    
    except ValueError as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Run all demos
    demo_project_metadata()
    demo_model_list()
    demo_model_detail()
    demo_model_runs()
    demo_model_to_dict()
