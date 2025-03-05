"""
DBT Discovery API Demo

This demonstrates using the high-level API layer instead of raw GraphQL queries.
"""

import os
import json
import argparse
from src.discovery_api.api import DiscoveryAPI

# Get environment and job IDs from environment variables
sandbox_environment_id = int(os.environ.get('ENV_ID_SANDBOX_PRODUCTION'))
mart_environment_id = int(os.environ.get('ENV_ID_MART_PRODUCTION'))

# Initialize the API with your DBT Cloud token
api = DiscoveryAPI(token=os.getenv("DBT_SERVICE_TOKEN"))

# Output formatting helper functions
def format_code(code, use_markdown=False):
    """Format code with optional markdown code block syntax."""
    if use_markdown:
        return f"```python\n{code}\n```"
    return code

def format_heading(text, use_markdown=False):
    """Format heading with optional markdown syntax."""
    if use_markdown:
        return f"### {text}\n"
    return f"\n=== {text} ===\n"

def format_subheading(text, use_markdown=False):
    """Format subheading with optional markdown syntax."""
    if use_markdown:
        return f"#### {text}\n"
    return f"\n{text}\n"

def format_output(text, use_markdown=False):
    """Format output with optional markdown syntax."""
    if use_markdown:
        return f"```\n{text}\n```"
    return text

def demo_project_metadata(use_markdown=False, output_file=None):
    """Demonstrate getting project metadata."""
    output = []

    output.append(format_heading("Project Metadata", use_markdown))
    output.append("This example shows how to retrieve basic metadata about a dbt project.\n")

    # Get project by environment ID
    output.append(format_subheading("Input", use_markdown))
    code = "project = api.project(environment_id=sandbox_environment_id)"
    output.append(format_code(code, use_markdown))

    project = api.project(environment_id=sandbox_environment_id)

    # Get project metadata
    output.append("\n")
    code = "metadata = project.get_metadata()"
    output.append(format_code(code, use_markdown))

    metadata = project.get_metadata()

    # Print project information
    output.append(format_subheading("Output", use_markdown))
    result_text = f"Project Name: {metadata.dbt_project_name}\n"
    result_text += f"Adapter Type: {metadata.adapter_type}\n"
    result_text += f"Environment ID: {metadata.environment_id}"
    
    output.append(format_output(result_text, use_markdown))

    result = "\n".join(output)

    if output_file:
        with open(output_file, 'a') as f:
            f.write(result + "\n\n")

    print(result)

    return result

def demo_model_list(use_markdown=False, output_file=None):
    """Demonstrate getting all models in a project."""
    output = []

    output.append(format_heading("Models List", use_markdown))
    output.append("This example shows how to retrieve a list of all models in a dbt project.\n")

    # Get project by environment ID
    output.append(format_subheading("Input", use_markdown))
    code = "project = api.project(environment_id=sandbox_environment_id)"
    output.append(format_code(code, use_markdown))

    project = api.project(environment_id=sandbox_environment_id)

    # Get all models
    output.append("\n")
    code = "models = project.get_models()"
    output.append(format_code(code, use_markdown))

    models = project.get_models()

    # Print models count
    output.append(format_subheading("Output", use_markdown))
    result_text = f"Found {len(models)} models\n\n"
    result_text += "First 5 models:\n"
    
    for i, model in enumerate(models[:5]):
        result_text += f"{i+1}. {model.metadata.name} ({model.metadata.materialized or 'unknown type'})\n"

    output.append(format_output(result_text, use_markdown))

    result = "\n".join(output)

    if output_file:
        with open(output_file, 'a') as f:
            f.write(result + "\n\n")

    print(result)

    return result

def demo_model_detail(use_markdown=False, output_file=None):
    """Demonstrate getting a specific model's details."""
    output = []

    output.append(format_heading("Model Detail", use_markdown))
    output.append("This example shows how to retrieve detailed information about a specific model.\n")

    model_name = 'bd_deal_actuals'  # Use a model name from your project

    # Get project by environment ID
    output.append(format_subheading("Input", use_markdown))
    code = "project = api.project(environment_id=sandbox_environment_id)"
    output.append(format_code(code, use_markdown))

    project = api.project(environment_id=sandbox_environment_id)

    try:
        # Get specific model by name
        output.append("\n")
        code = f"model = project.get_model('{model_name}')"
        output.append(format_code(code, use_markdown))

        model = project.get_model(model_name)

        # Print model metadata
        output.append(format_subheading("Output", use_markdown))
        result_text = f"Model Name: {model.metadata.name}\n"
        result_text += f"Unique ID: {model.metadata.unique_id}\n"
        result_text += f"Database: {model.metadata.database or 'Not specified'}\n"
        result_text += f"Schema: {model.metadata.schema or 'Not specified'}\n"
        result_text += f"Description: {model.metadata.description or 'No description'}\n"
        result_text += f"Materialized Type: {model.metadata.materialized or 'Unknown'}\n"
        result_text += f"Tags: {', '.join(model.metadata.tags) if model.metadata.tags else 'No tags'}"

        # Get and print last run status
        if model.last_run:
            result_text += f"\n\nLast Run Status: {model.last_run.status or 'Unknown'}\n"
            result_text += f"Run ID: {model.last_run.run_id or 'Unknown'}\n"
            result_text += f"Run Time: {model.last_run.run_time}\n"
            result_text += f"Execution Time: {model.last_run.execution_time or 'Unknown'} seconds"
            if model.last_run.error_message:
                result_text += f"\nError: {model.last_run.error_message}"
        else:
            result_text += "\n\nNo run history available"

        output.append(format_output(result_text, use_markdown))

    except ValueError as e:
        output.append(format_output(f"Error: {str(e)}", use_markdown))

    result = "\n".join(output)

    if output_file:
        with open(output_file, 'a') as f:
            f.write(result + "\n\n")

    print(result)

    return result

def demo_model_runs(use_markdown=False, output_file=None):
    """Demonstrate getting historical runs for a model."""
    output = []

    output.append(format_heading("Model Historical Runs", use_markdown))
    output.append("This example shows how to retrieve the run history for a specific model.\n")

    model_name = 'bd_deal_actuals'  # Use a model name from your project

    # Get project by environment ID
    output.append(format_subheading("Input", use_markdown))
    code = "project = api.project(environment_id=sandbox_environment_id)"
    output.append(format_code(code, use_markdown))

    project = api.project(environment_id=sandbox_environment_id)

    try:
        # Get historical runs directly from project
        output.append("\n")
        code = f"runs = project.get_model_historical_runs('{model_name}', limit=5)"
        output.append(format_code(code, use_markdown))

        runs = project.get_model_historical_runs(model_name, limit=5)

        # Print runs information
        output.append(format_subheading("Output", use_markdown))
        result_text = f"Found {len(runs)} historical runs for model '{model_name}'\n"

        # Print details for each run
        for i, run in enumerate(runs):
            result_text += f"\nRun {i+1}:\n"
            result_text += f"  Status: {run.status or 'Unknown'}\n"
            result_text += f"  Run ID: {run.run_id or 'Unknown'}\n"
            result_text += f"  Run Time: {run.run_time}\n"
            result_text += f"  Execution Time: {run.execution_time or 'Unknown'} seconds"
            if run.error_message:
                result_text += f"\n  Error: {run.error_message}"

        output.append(format_output(result_text, use_markdown))

    except ValueError as e:
        output.append(format_output(f"Error: {str(e)}", use_markdown))

    result = "\n".join(output)

    if output_file:
        with open(output_file, 'a') as f:
            f.write(result + "\n\n")

    print(result)

    return result

def demo_model_to_dict(use_markdown=False, output_file=None):
    """Demonstrate converting a model to a dictionary."""
    output = []

    output.append(format_heading("Model to Dictionary", use_markdown))
    output.append("This example shows how to convert a model object to a dictionary for further processing.\n")

    model_name = 'bd_deal_actuals'  # Use a model name from your project

    # Get project by environment ID
    output.append(format_subheading("Input", use_markdown))
    code = "project = api.project(environment_id=sandbox_environment_id)"
    output.append(format_code(code, use_markdown))

    project = api.project(environment_id=sandbox_environment_id)

    try:
        # Get specific model by name
        output.append("\n")
        code = f"model = project.get_model('{model_name}')"
        output.append(format_code(code, use_markdown))

        model = project.get_model(model_name)

        # Convert model to dictionary
        output.append("\n")
        code = "model_dict = model.to_dict()"
        output.append(format_code(code, use_markdown))

        model_dict = model.to_dict()

        # Print dictionary representation
        output.append(format_subheading("Output", use_markdown))
        code = "print(json.dumps(model_dict, indent=2, default=str))"
        output.append(format_code(code, use_markdown))

        output.append("\nResult (truncated for readability):")
        
        # Format the JSON output in a more readable way for the README
        json_output = json.dumps(model_dict, indent=2, default=str)
        # Truncate if too long
        if len(json_output) > 1000 and use_markdown:
            json_output = json_output[:1000] + "\n... (truncated)"
            
        output.append(format_output(json_output, use_markdown))

    except ValueError as e:
        output.append(format_output(f"Error: {str(e)}", use_markdown))

    result = "\n".join(output)

    if output_file:
        with open(output_file, 'a') as f:
            f.write(result + "\n\n")

    print(result)

    return result

if __name__ == "__main__":

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='DBT Discovery API Demo')

    parser.add_argument('--markdown', action='store_true', help='Format output in markdown')

    parser.add_argument('--output', type=str, help='Save output to specified file')

    args = parser.parse_args()

    # If output file is specified, create/clear the file
    if args.output:
        with open(args.output, 'w') as f:
            if args.markdown:
                f.write("# DBT Discovery API Examples\n\n")
                f.write("This document demonstrates how to use the DBT Discovery API with Python. ")
                f.write("Each example shows the Python code needed and the resulting output.\n\n")
            else:
                f.write("DBT Discovery API Demo Output\n\n")

    # Run all demos with the specified formatting options
    demo_project_metadata(use_markdown=args.markdown, output_file=args.output)

    demo_model_list(use_markdown=args.markdown, output_file=args.output)

    demo_model_detail(use_markdown=args.markdown, output_file=args.output)

    demo_model_runs(use_markdown=args.markdown, output_file=args.output)

    demo_model_to_dict(use_markdown=args.markdown, output_file=args.output)

    if args.output:
        print(f"\nOutput saved to {args.output}")
