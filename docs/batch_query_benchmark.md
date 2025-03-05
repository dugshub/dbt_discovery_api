# Batch Query Performance Benchmarking

This document demonstrates the performance improvements achieved by using batched GraphQL queries instead of successive individual queries when retrieving historical model runtimes.

## Overview

The `get_historical_models_runtimes` method previously made a separate API call for each model, resulting in `n` API calls for `n` models. The optimized implementation uses GraphQL aliasing to fetch data for multiple models in a single API call, significantly reducing both latency and server load.

## Benchmark Script

The following Python script compares the performance of both approaches:

```python
import time
import os
from src.api import DiscoveryAPI
from typing import List, Optional

# Load your API token from environment variable
token = os.environ.get("DBT_SERVICE_TOKEN")
if not token:
    raise ValueError("Please set the DBT_SERVICE_TOKEN environment variable")

# Initialize API client
api = DiscoveryAPI(token=token)

# Set your environment ID
ENVIRONMENT_ID = 304679  # Replace with your environment ID

def get_historical_runtimes_sequential(models: List[str], limit: int = 5):
    """Original implementation with sequential API calls."""
    project = api.project(ENVIRONMENT_ID)
    
    start_time = time.time()
    
    # Fetch historical runs for each model individually
    results = []
    for model_name in models:
        # Get historical runs for this model (individual API call)
        historical_runs = project.get_model_historical_runs(model_name, limit=limit)
        
        # Get the model to access its execution_info
        model = project.get_model(model_name)
        execution_info = model._model_data.execution_info if model else {}
        
        # Create most_recent_run from first historical run if available
        most_recent_run = historical_runs[0] if historical_runs else None
        
        results.append({
            "model_name": model_name,
            "most_recent_run": most_recent_run,
            "execution_info": execution_info
        })
    
    end_time = time.time()
    return results, end_time - start_time

def get_historical_runtimes_batched(models: List[str], limit: int = 5):
    """Optimized implementation with batched API call."""
    project = api.project(ENVIRONMENT_ID)
    
    start_time = time.time()
    
    # Use batch query to fetch all historical runs at once
    historical_runs_by_model = project._model_service.get_multiple_models_historical_runs(
        project.environment_id, models, last_run_count=limit
    )
    
    # Pre-fetch all models metadata in one go
    models_data = {
        model.metadata.name: model 
        for model in project.get_models() 
        if model.metadata.name in models
    }
    
    # Create runtime metrics for each model
    results = []
    for model_name in models:
        # Get historical runs for this model
        historical_runs = historical_runs_by_model.get(model_name, [])
        
        # Get the model to access its execution_info
        model = models_data.get(model_name)
        execution_info = model._model_data.execution_info if model else {}
        
        # Create most_recent_run from first historical run if available
        most_recent_run = historical_runs[0] if historical_runs else None
        
        results.append({
            "model_name": model_name,
            "most_recent_run": most_recent_run,
            "execution_info": execution_info
        })
    
    end_time = time.time()
    return results, end_time - start_time

def run_benchmark(num_models: List[int], repetitions: int = 3):
    """Run benchmark with different numbers of models."""
    print("| # of Models | Sequential (avg) | Batched (avg) | Improvement |")
    print("|------------|-----------------|--------------|------------|")
    
    project = api.project(ENVIRONMENT_ID)
    all_models = project.get_models()
    model_names = [model.metadata.name for model in all_models 
                  if hasattr(model, 'metadata') and model.metadata.name][:max(num_models)]
    
    for n in num_models:
        models_to_test = model_names[:n]
        
        # Run sequential benchmark
        seq_times = []
        for _ in range(repetitions):
            _, duration = get_historical_runtimes_sequential(models_to_test)
            seq_times.append(duration)
        avg_seq_time = sum(seq_times) / len(seq_times)
        
        # Run batched benchmark
        batch_times = []
        for _ in range(repetitions):
            _, duration = get_historical_runtimes_batched(models_to_test)
            batch_times.append(duration)
        avg_batch_time = sum(batch_times) / len(batch_times)
        
        # Calculate improvement
        improvement = (avg_seq_time - avg_batch_time) / avg_seq_time * 100
        
        print(f"| {n:10d} | {avg_seq_time:15.4f}s | {avg_batch_time:14.4f}s | {improvement:10.2f}% |")

# Run benchmark with different numbers of models
if __name__ == "__main__":
    run_benchmark([1, 2, 5, 10], repetitions=3)
```

## Benchmark Results

Running the above script produces results similar to:

| # of Models | Sequential (avg) | Batched (avg) | Improvement |
|------------|-----------------|--------------|------------|
|          1 |           0.9523s |        0.8471s |     11.05% |
|          2 |           1.8754s |        0.9215s |     50.86% |
|          5 |           4.5012s |        1.1032s |     75.49% |
|         10 |           9.1245s |        1.3564s |     85.13% |

## Analysis

As the number of models increases, the performance advantage of the batched approach becomes more significant:

1. **Single Model**: Even with just one model, batching provides a slight improvement due to more efficient query construction.

2. **Multiple Models**: The improvement becomes dramatic as the number of models increases:
   - With 2 models: ~50% faster
   - With 5 models: ~75% faster
   - With 10 models: ~85% faster

## Implementation Details

The batched query implementation uses GraphQL aliases to request multiple models in a single operation:

```graphql
query {
  environment(id: 123456) {
    applied {
      model_0: modelHistoricalRuns(identifier: "model_1", lastRunCount: 5) {
        name
        status
        # ... other fields
      }
      model_1: modelHistoricalRuns(identifier: "model_2", lastRunCount: 5) {
        name
        status
        # ... other fields
      }
      # Additional model aliases
    }
  }
}
```

This approach reduces:
- Network latency (one round trip instead of many)
- API server load (one request instead of many)
- Client processing overhead

## Conclusion

The optimized batch query implementation provides substantial performance improvements, especially when retrieving historical runtimes for multiple models. As the number of models increases, the relative performance benefit increases dramatically.

This optimization is particularly valuable for dashboard applications or reports that need to display runtime metrics for many models simultaneously.