# DBT Discovery API Examples

This document demonstrates how to use the DBT Discovery API with Python. Each example shows the Python code needed and the resulting output.

### Project Metadata

This example shows how to retrieve basic metadata about a dbt project.

#### Input

```python
project = api.project(environment_id=sandbox_environment_id)
```


```python
metadata = project.get_metadata()
```
#### Output

```
Project Name: analytics_sandbox
Adapter Type: redshift
Environment ID: 304679
```

### Models List

This example shows how to retrieve a list of all models in a dbt project.

#### Input

```python
project = api.project(environment_id=sandbox_environment_id)
```


```python
models = project.get_models()
```
#### Output

```
Found 219 models

First 5 models:
1. b2b_facility_contact_mapping (table)
2. bad_rental_cost (table)
3. bd_deal_actuals (table)
4. bd_deal_facility_base (table)
5. bd_deal_goals (view)

```

### Model Detail

This example shows how to retrieve detailed information about a specific model.

#### Input

```python
project = api.project(environment_id=sandbox_environment_id)
```


```python
model = project.get_model('bd_deal_actuals')
```
#### Output

```
Model Name: bd_deal_actuals
Unique ID: model.analytics_sandbox.bd_deal_actuals
Database: spotheroprod
Schema: analytics_sandbox
Description: No description
Materialized Type: table
Tags: daily

Last Run Status: success
Run ID: Unknown
Run Time: 2025-03-04 10:39:05.068000+00:00
Execution Time: 7.648142576217651 seconds
```

### Model Historical Runs

This example shows how to retrieve the run history for a specific model.

#### Input

```python
project = api.project(environment_id=sandbox_environment_id)
```


```python
runs = project.get_model_historical_runs('bd_deal_actuals', limit=5)
```
#### Output

```
Found 5 historical runs for model 'bd_deal_actuals'

Run 1:
  Status: success
  Run ID: Unknown
  Run Time: 2025-03-04 10:39:05.068000+00:00
  Execution Time: 7.648142576217651 seconds
Run 2:
  Status: success
  Run ID: Unknown
  Run Time: 2025-03-03 23:41:35.296000+00:00
  Execution Time: 16.45683360099792 seconds
Run 3:
  Status: success
  Run ID: Unknown
  Run Time: 2025-03-03 22:19:37.099000+00:00
  Execution Time: 7.76534104347229 seconds
Run 4:
  Status: success
  Run ID: Unknown
  Run Time: 2025-03-03 20:30:02.411000+00:00
  Execution Time: 4.265995264053345 seconds
Run 5:
  Status: success
  Run ID: Unknown
  Run Time: 2025-03-03 10:36:30.306000+00:00
  Execution Time: 10.0227997303009 seconds
```

### Model to Dictionary

This example shows how to convert a model object to a dictionary for further processing.

#### Input

```python
project = api.project(environment_id=sandbox_environment_id)
```


```python
model = project.get_model('bd_deal_actuals')
```


```python
model_dict = model.to_dict()
```
#### Output

```python
print(json.dumps(model_dict, indent=2, default=str))
```

Result (truncated for readability):
```
{
  "name": "bd_deal_actuals",
  "unique_id": "model.analytics_sandbox.bd_deal_actuals",
  "database": "spotheroprod",
  "schema": "analytics_sandbox",
  "description": "",
  "materialized": "table",
  "tags": [
    "daily"
  ],
  "last_run": {
    "status": "success",
    "run_id": null,
    "run_time": "2025-03-04 10:39:05.068000+00:00",
    "execution_time": 7.648142576217651,
    "error_message": null
  }
}
```

