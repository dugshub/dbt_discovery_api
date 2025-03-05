#!/usr/bin/env python3

import os
import sys
import time
from src.discovery_api.services.BaseQuery import BaseQuery
from src.discovery_api.services.ModelService import ModelService

# Ensure token is available
token = os.environ.get("DBT_SERVICE_TOKEN")
if not token:
    print("Error: DBT_SERVICE_TOKEN environment variable not set")
    sys.exit(1)

# Use any environment ID from config.yml
environment_id = 95718  # Using spothero_accounting.prod_env_id from config.yml

# Create the services
base_query = BaseQuery(token=token)
model_service = ModelService(base_query)

# Test a few queries
print("Testing model service queries...")

def test_query(description, func, *args, **kwargs):
    print(f"\n{description}:")
    start = time.time()
    result = func(*args, **kwargs)
    duration = time.time() - start
    print(f"Query completed in {duration:.3f} seconds")
    return result

# Test with different query sizes
print("\n=== Testing with small queries (limit=2) ===")
models = test_query("Fetching applied models (small)", 
                    model_service.get_models_applied, environment_id, limit=2)
if models:
    print(f"Found {len(models)} models")
    for model in models:
        print(f"Model: {model.name}")

models = test_query("Fetching definition models (small)", 
                    model_service.get_models_definition, environment_id, limit=2)
if models:
    print(f"Found {len(models)} models")
    for model in models:
        print(f"Model: {model.name}")

# Test with larger queries to see performance impact
print("\n=== Testing with larger queries (limit=20) ===")
models = test_query("Fetching applied models (larger)", 
                    model_service.get_models_applied, environment_id, limit=20)
if models:
    print(f"Found {len(models)} models")

models = test_query("Fetching definition models (larger)", 
                    model_service.get_models_definition, environment_id, limit=20)
if models:
    print(f"Found {len(models)} models")

# Test with a much larger query limit to potentially see performance impact
print("\n=== Testing with very large query (limit=100) ===")
models = test_query("Fetching applied models (very large)", 
                    model_service.get_models_applied, environment_id, limit=100)
if models:
    print(f"Found {len(models)} models")

# Get a single model by name with full detail (might be slower)
if models and len(models) > 0:
    test_model_name = models[0].name
    print(f"\n=== Testing model detail query for '{test_model_name}' ===")
    model = test_query(f"Fetching model detail", 
                      model_service.get_model_by_name, 
                      environment_id, test_model_name, state='applied')
    if model:
        print(f"Successfully retrieved details for model: {model.name}")

print("\nDone!")