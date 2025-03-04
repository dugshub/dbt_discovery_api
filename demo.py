from sgqlc.operation import Operation
from src.schema import DefinitionResourcesFilter
from sgqlc.endpoint.http import HTTPEndpoint

import schema

import os
# Get environment and job IDs from environment variables
sandbox_environment_id = int(os.environ.get('ENV_ID_SANDBOX_PRODUCTION'))
mart_environment_id = int(os.environ.get('ENV_ID_MART_PRODUCTION'))





## Environment Details
### Environments carry either Definition or Applied state. Definition is based on the project code and the latest git commit, 
# while Applied is based on the project's current state based on job runs and builds.

op = Operation(schema.Query)

environment_id = sandbox_environment_id

##  Using alias here is not needed - just a way of showing how we can instantiate and include multiple versions of the same node
environment = op.environment(id=sandbox_environment_id,__alias__='dbt_environment')


## Adding common environment fields
environment.dbt_project_name()
environment.adapter_type()


## Splitting applied and definition for demonstrative purposes - this could be done in fewer lines but this shows the full way its generated
applied = environment.applied(__alias__='applied')
definition = environment.definition(__alias__='definition')

## Last Github State (DefinitionState)
definition.last_updated_at()
definition.resource_counts()


## Latest Job Run (Applied State)
applied.last_updated_at()
applied.resource_counts()
applied.latest_git_sha()

## Optional extended fields
op


## Applied model_definitions Related Queries
## This gets information about the model_definitions across a given project, but not the models themselves

op = Operation(schema.Query)
environment_id = sandbox_environment_id
min_models_to_fetch = 300

models = op.environment(id=environment_id).applied.models(first=min_models_to_fetch)

## instantiating the objects we care to return - this isn't necessary but it keeps it organized
page_info = models.page_info(__alias__='graphql query metadata') 
model_detail = models.edges.node(__alias__='model')
model_execution = model_detail.execution_info(__alias__='model_run_details')

#define page metadata we care about - if we don't do this we get all (not bad, just default)
page_info.has_next_page()
page_info.has_previous_page()

## Add general models fields
model_detail.name()
model_detail.alias()
model_detail.unique_id()

## Model Run Information 
model_execution.last_run_id()
model_execution.last_run_status()
model_execution.last_success_job_definition_id()
model_execution.last_success_run_id()
model_execution.run_generated_at()
model_execution.run_elapsed_time()
model_execution.execute_completed_at()

#model_detail.execution_info.last_success_job_definition_id()

op

## Defined Resource Query (Model Filtered in this example)

op = Operation(schema.Query)

environment_id = sandbox_environment_id

resource_type_filter = ["Model"]
resource_filter = DefinitionResourcesFilter(types=resource_type_filter)

model_name = 'bd_deal_actuals'
min_resource_results = 500


## Navigate to the Model Node specifically (using filter=resource_type)  this is technically reusable across other resource types
model_definition = op.environment(id=sandbox_environment_id).definition.resources(filter=resource_filter, first=min_resource_results).edges.node()

## General Details
model_definition.name()
model_definition.description()
model_definition.unique_id()
model_definition.resource_type()
model_definition.run_generated_at()

## Project and Environment Details 
model_definition.project_id()
model_definition.environment_id()
model_definition.account_id()

#Resource Metadata
model_definition.tags()
model_definition.meta()
model_definition.file_path()

op

# Single Model Historical Run Details

op = Operation(schema.Query)

environment_id = sandbox_environment_id


model_name = 'bd_deal_actuals'
last_run_count = 20

model_historical_run = op.environment(id=environment_id).applied.model_historical_runs(identifier=model_name, last_run_count=last_run_count,__alias__="model_detail")

include_metadata = True
include_execution = True
include_dbt_metadata = False
include_code = False
include_dependenceies = False
include_status = True


# General Information
model_historical_run.name()
model_historical_run.alias()
model_historical_run.description()
model_historical_run.resource_type()

# Model Metadata
if include_metadata:
    model_historical_run.tags()
    model_historical_run.meta()

# Execution and Timing
if include_execution:
    model_historical_run.run_id()
    model_historical_run.invocation_id()
    model_historical_run.job_id()
    model_historical_run.thread_id()
    model_historical_run.run_generated_at()
    model_historical_run.compile_started_at()
    model_historical_run.compile_completed_at()
    model_historical_run.execute_started_at()
    model_historical_run.execute_completed_at()
    model_historical_run.execution_time()
    model_historical_run.run_elapsed_time()


# dbt Project/Environment Metadata
if include_dbt_metadata:
    model_historical_run.environment_id()
    model_historical_run.project_id()
    model_historical_run.account_id()
    model_historical_run.owner()

# Code and SQL
if include_code:
    model_historical_run.raw_sql()
    model_historical_run.compiled_sql()
    model_historical_run.raw_code()
    model_historical_run.compiled_code()
    model_historical_run.language()
    model_historical_run.database()
    model_historical_run.schema()


# Dependencies and Relationships
if include_dependenceies:
    model_historical_run.depends_on()
    model_historical_run.parents_models()
    model_historical_run.parents_sources()

# Status and Error
if include_status:
    model_historical_run.status()
    model_historical_run.error()
    model_historical_run.skip()

# Other
print(op)


# Initialize the client with Bearer token
client = HTTPEndpoint('https://metadata.cloud.getdbt.com/graphql', {'Authorization': f'Bearer {os.getenv("DBT_SERVICE_TOKEN")}'})

# Execute the operation
response = client(op)

# Process the response
print(response)
