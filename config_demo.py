"""
DBT Discovery API Config Demo

This demonstrates using the config.yml file to automatically load projects.
"""

import os
import json
from src.discovery_api.api.api import DiscoveryAPI

# Utility function for formatted printing
def print_section(title):
    """Print a section header with formatting."""
    print(f"\n=== {title} ===\n")

def print_item(label, value, indent=0):
    """Print a labeled item with proper formatting."""
    indent_str = "  " * indent
    if value is None or value == '':
        value = 'Not specified'
    print(f"{indent_str}{label}: {value}")

def print_json(data):
    """Pretty print a JSON object."""
    print(json.dumps(data, indent=2, default=str))

# Initialize the API with your DBT Cloud token
# The API will automatically load projects from config.yml
api = DiscoveryAPI(token=os.getenv("DBT_SERVICE_TOKEN"))

def demo_config_projects():
    """Demonstrate projects loaded from config.yml."""
    print_section("Projects from config.yml")
    
    # Access projects loaded from config
    print_item("Found", f"{len(api.projects)} projects in config.yml")
    
    # Print information about each project
    for project_name, project in api.projects.items():
        metadata = project.get_metadata()
        print(f"\nProject: {project_name}")
        print_item("Environment ID", metadata.environment_id, indent=1)
        print_item("Project Name", metadata.dbt_project_name, indent=1)
        print_item("Adapter Type", metadata.adapter_type, indent=1)

def demo_project_models():
    """Demonstrate accessing models from a config-loaded project."""
    print_section("Models in Config-Loaded Project")
    
    # Skip if no projects loaded
    if not api.projects:
        print("No projects found in config.yml. Please add projects to the config file.")
        return
    
    # Get the first project for demonstration
    first_project_name = next(iter(api.projects))
    project = api.projects[first_project_name]
    
    print_item("Project", first_project_name)
    
    # Get models
    models = project.get_models()
    print_item("Found", f"{len(models)} models")
    
    # Print first 5 models
    print("\nFirst 5 models:")
    for i, model in enumerate(models[:5]):
        print_item(f"{i+1}. {model.metadata.name}", f"({model.metadata.materialized or 'unknown type'})")

if __name__ == "__main__":
    # Run demos
    demo_config_projects()
    demo_project_models()