
## **Overview**

Create a new API layer that replaces the previous implementation while maintaining compatibility with the existing service layer (ModelService, JobService). The solution enhances the architecture with
- A comprehensive object hierarchy (dbtAccount -> Project -> Model/Job -> Run)
- User-friendly filtering mechanisms

The API is designed to efficiently handle common dbt reporting needs such as:
- Finding slowest models across projects
- Identifying longest-running jobs
- Filtering models by tags, materialization, or runtime
- Retrieving historical performance metrics
- Optimizing query performance through intelligent caching

## **Project Structure and Architecture**

### **Directory Structure**

```
src/discovery_api/
├── models/                             # Pydantic models (new)
│   ├── __init__.py
│   ├── base.py                         # Base/common models (RuntimeReport, RunStatus) (new)
│   ├── filters.py                      # Filter models (SearchFilter, ModelFilter, ProjectFilter) (new)
│   └── resources.py                    # Resource models (Model, Job, Project, Run) (new)
├── services/                           # Existing service layer implementations
│   ├── __init__.py
│   ├── BaseQuery.py                    # Base GraphQL query functionality (existing)
│   ├── EnvironmentService.py           # Environment-related services (existing)
│   ├── JobService.py                   # Job-related services (existing)
│   └── ModelService.py                 # Model-related services (existing)
│   └── models.py                       # Models for the services (existing)
├── api/                             # New API layer
│   ├── __init__.py                     # Public exports (new)
│   ├── dbt_account.py                  # dbtAccount implementation (new)
│   ├── resources/                      # Resource classes (new)
│   │   ├── __init__.py
│   │   ├── project.py                  # Project implementation (new)
│   │   ├── model.py                    # Model implementation (new)
│   │   ├── job.py                      # Job implementation (new)
│   │   └── run.py                      # Run implementation (new)
└── exceptions.py                       # Custom exception types (new)
```

### **Models**
```python
class RuntimeReport(BaseModel):
    job_id: str
    run_id: str
    model_id: Optional[str]
    runtime: float
    start_time: datetime
    end_time: datetime

class RunStatus(str, enum.Enum):
    success = "success"
    failure = "failure"
    cancelled = "cancelled" 
    run_completed_at: datetime

class SearchFilter:
    #when used to fetch models, this filters the models by these properties
    #when used to fetch jobs/runs it filters the run for the models that match these properties. Jobs/runs don't have tags so this lets us get "all jobs/runs that contain models tagged with marketing, for example"
    tags: Optional[List[str]]
    materialization: Optional[str]
    min_runtime: Optional[float]
    max_runtime: Optional[float]

class ModelFilter(SearchFilter):
    models: Optional[List[Model]] #this is model_object
    model_ids: Optional[List[str]] #this is project_name.model_name


class ProjectFilter(SearchFilter):
    projects: Optional[List[Project]]
    project_ids: Optional[List[str]]
    include_or_exclude: Optional[str] = "include"
```

Classes:
```python

class dbtAccount:
    environment: ['production','staging']
    projects: List[Project]
    filter: Optional[ProjectFilter] = None

    def get_projects(self, filter: ProjectFilter = None) -> List[Project]:
        pass

    def get_jobs(self, filter: SearchFilter = None) -> List[Job]:
        # Searches across all projects (unless included_)
        pass

    def get_models(self, filter: SearchFilter = None) -> List[Model]:
        # Searches across all projects
        pass

    def get_runs(self, limit: int = 10, filter: SearchFilter = None) -> List[Run]:
        # Searches across all projects
        pass
        
    def slowest_models(self, slowest_n: int = 5, last_n_runs: int = 1, filter: SearchFilter = None) -> List[Model]:
        # Finds slowest models across all projects
        pass
        
    def longest_running_jobs(self, longest_n: int = 5, last_n_runs: int = 1, filter: SearchFilter = None, model_filter: ModelFilter = None) -> List[Job]:
        # Finds longest running jobs across all projects
        pass

class Project:
    project_id: str
    models: List[Model]
    jobs: List[Job]
    model_count: int
    job_count: int

    def get_models(self, filter: SearchFilter = None) -> List[Model]: #Filtering by tags, materialization, runtime, etc. Use kwargs for this unless you have a better solution.
        pass

    def get_jobs(self, filter: SearchFilter = None) -> List[Job]:
        pass

    def slowest_models(self, slowest_n: int = 5, last_n_runs: int = 1, filter: SearchFilter = None) -> List[Model]:
        #Finds slowest models across all projects, by default uses last run if last_n_runs > 1 uses historical runs (requiring multiple queries)
        pass

    def longest_running_jobs(self, longest_n: int = 5, last_n_runs: int = 1, filter: SearchFilter = None, model_filter: ModelFilter = None) -> List[Job]:
        #This should use job.get_average_job_runtime(), passing the filter params.
        #last_n_runs is the number of runs to use for the average, by default looking at the most recent run (likely meaning no additional query is needed as historical runs may require multiple api requests)
        pass

class Model:
    model_id: str #this is project_name.model_name
    last_run_status: RunStatus
    last_run_runtime: float
    last_run_start_time: datetime
    last_run_end_time: datetime
    
    def __init__(self, model_name: str, project_name: str):
        last_run = self.get_last_run()
        self.last_run_status = last_run.status
        ...

        def get_last_run(self) -> Run:
            pass

        def get_runs(self, last_n: int = 5, filter: SearchFilter = None) -> List[Run]:
            pass

        def get_sql(self) -> str:
            pass

        def freshness(self) -> RunStatus:
            pass

        def get_jobs(self) -> List[Job]: #Returns all jobs that this model is triggered in.
            pass
        
class Job:
    job_id: str
    last_run_status: RunStatus
    last_run_runtime: float
    last_run_start_time: datetime
    last_run_end_time: datetime

    def __init__(self, job_id: str):
        last_run = self.get_last_run()
        self.last_run_status = last_run.status
        ...


    def get_models(self, **kwargs) -> List[Model]:
        ## Filter by tags, materialization, runtime, etc. Use kwargs for this unless you have a better solution.
        pass

    def get_last_run(self) -> Run:
        pass

    def get_runs(self, last_n: int = 5) -> List[Run]:
        pass

    def get_slowest_models(self, slowest_n: int = 5, filter: SearchFilter = None) -> List[Model]:
        pass

    def get_runtimes(self, last_n: int = 5, by_model: bool = False) -> List[RuntimeReport]:
        #returns the last N runtimes (not run objects) for the given job
        #if by_model is True, returns the last N runtimes for each model in the job
        pass

    def get_average_job_runtime(self, last_n: int = 5, filter: SearchFilter = None, model_filter: ModelFilter = None) -> float: #filter by tags within models so we can get average_job_time for jobs containing models tagged with marketing
        pass

    def average_historical_model_runtime(self, slowest_n: int = 5, last_n_runs: int = 5, filter: SearchFilter = None, model_filter: ModelFilter = None) -> float: 
        #Calculates the average runtime for a model over the last N runs, allowing it to be filtered to the worst N models (worst defined by the total average, not most recent)
        #This is different from the average_model_runtime method, which returns the average runtime of the last N runs
        #This would need to fetch the last N models, calculate the average runtime for each, and return the average of the worst N models.
        pass

class Run:
    #Future add - threads that the run uses
    run_id: str
    status: RunStatus
    runtime: float
    model_count: int
    start_time: datetime
    end_time: datetime
    job: Job

    def __init__(self, run_id: str):
        pass

    def get_models(self, **kwargs, filter: SearchFilter = None) -> List[Model]:
        pass

    def get_slowest_models(self, slowest_n: int = 5, filter: SearchFilter = None) -> List[Model]:
        pass

    def average_model_runtime(self, slowest_n: int = 5, filter: SearchFilter = None, model_filter: ModelFilter = None) -> float: #calculates the average runtime, allowing it to be filtered to the worst offenders. 
        pass
```


## Example Usage :

- This example shows a simple call to get all models for a job
- The kwargs can be used to add or remove various fields from the response
- Other methods behave similarly across all classes
- This is how the queries within the API layer should be set up using the service classes
- For queries that retrieve results for multiple models, use batching
- Tests show in detail how these methods work

```python
import os
from src.discovery_api.services import BaseQuery, JobService

env = BaseQuery(token=os.environ.get("DBT_SERVICE_TOKEN"))
rental_behaviour_job = JobService(env)
all_models = rental_behaviour_job.get_job_models(job_id=760646)

job_details = rental_behaviour_job.get_job_metadata(job_id=760646)


#all_models (truncated)
{'models': [{'name': 'b2b_facility_contact_mapping',
   'unique_id': 'model.analytics_sandbox.b2b_facility_contact_mapping',
   'description': '',
   'tags': ['adhoc', 'daily'],
   'resource_type': 'model',
   'database': 'spotheroprod',
   'schema': 'analytics_sandbox_adhoc',
   'alias': 'b2b_facility_contact_mapping',
   'run_id': 376739307,
   'job_id': 760646,
   'invocation_id': 'e174c46b-a06b-4622-8395-12e1e67e6da7',
   'thread_id': 'Thread-1 (worker)',
   'run_generated_at': '2025-03-12T10:35:38.459Z',
   'compile_started_at': '2025-03-12T09:00:34.023Z',
   'compile_completed_at': '2025-03-12T09:00:34.047Z',
   'execute_started_at': '2025-03-12T09:00:34.109Z',
   'execute_completed_at': '2025-03-12T09:00:53.171Z',
   'execution_time': 19.31550598144531,
   'run_elapsed_time': 5709.064619541168,
   'status': 'success',
   'error': None,
   'skip': False,
   'raw_sql': "{{ config(materialized='table',\n        sort_type='compound',\n        sort=['sh_user_id'],\n        dist='sh_user_id', tags=['daily']) }}\n\nSELECT DISTINCT\n    TRY_CAST(shu.id AS INT) AS sh_user_id\n  , TRY_CAST(sa.parking_spot_id AS INT) AS sh_parking_spot_id\n  , sfc.email\n  , ocr.rate_inventory_specialist_c AS sfdc_is_rate_inventory_specialist\n  , sa.spot_admin_id AS sh_spot_admin_id\n  , sfc.id AS sfdc_contact_id\nFROM sh_public.spothero_user shu                                                                    --sh_user\nINNER JOIN sfdc.contact sfc ON shu.id = sfc.unique_user_id_c                                        --sfdc_contact to sh_user\nINNER JOIN sh_public.spot_admin sa ON shu.id = sa.user_id                                           --sh_user LJ to sh_spot_admin\nINNER JOIN sh_public.parking_spot shps ON shps.parking_spot_id = sa.parking_spot_id                 --sh_ps LJ to sh_spot_admin\nINNER JOIN sfdc.opportunity_contact_roles_c ocr ON ocr.contact_c = sfc.id                           --sfdc_ocr to sfdc_contact\nINNER JOIN sfdc.opportunity o ON o.id = ocr.opportunity_c AND o.spot_id_c = shps.parking_spot_id    --sfdc_opp to sfdc_ocr AND sfdc_opp to sh_ps\nWHERE sfc.account_id IS NOT NULL\n  AND shps.status NOT IN ('deleted','archived')\n  AND ocr.rate_inventory_specialist_c IS TRUE\n  AND sa.deleted IS FALSE",
   'compiled_sql': "\n\nSELECT DISTINCT\n    TRY_CAST(shu.id AS INT) AS sh_user_id\n  , TRY_CAST(sa.parking_spot_id AS INT) AS sh_parking_spot_id\n  , sfc.email\n  , ocr.rate_inventory_specialist_c AS sfdc_is_rate_inventory_specialist\n  , sa.spot_admin_id AS sh_spot_admin_id\n  , sfc.id AS sfdc_contact_id\nFROM sh_public.spothero_user shu                                                                    --sh_user\nINNER JOIN sfdc.contact sfc ON shu.id = sfc.unique_user_id_c                                        --sfdc_contact to sh_user\nINNER JOIN sh_public.spot_admin sa ON shu.id = sa.user_id                                           --sh_user LJ to sh_spot_admin\nINNER JOIN sh_public.parking_spot shps ON shps.parking_spot_id = sa.parking_spot_id                 --sh_ps LJ to sh_spot_admin\nINNER JOIN sfdc.opportunity_contact_roles_c ocr ON ocr.contact_c = sfc.id                           --sfdc_ocr to sfdc_contact\nINNER JOIN sfdc.opportunity o ON o.id = ocr.opportunity_c AND o.spot_id_c = shps.parking_spot_id    --sfdc_opp to sfdc_ocr AND sfdc_opp to sh_ps\nWHERE sfc.account_id IS NOT NULL\n  AND shps.status NOT IN ('deleted','archived')\n  AND ocr.rate_inventory_specialist_c IS TRUE\n  AND sa.deleted IS FALSE",
   'raw_code': "{{ config(materialized='table',\n        sort_type='compound',\n        sort=['sh_user_id'],\n        dist='sh_user_id', tags=['daily']) }}\n\nSELECT DISTINCT\n    TRY_CAST(shu.id AS INT) AS sh_user_id\n  , TRY_CAST(sa.parking_spot_id AS INT) AS sh_parking_spot_id\n  , sfc.email\n  , ocr.rate_inventory_specialist_c AS sfdc_is_rate_inventory_specialist\n  , sa.spot_admin_id AS sh_spot_admin_id\n  , sfc.id AS sfdc_contact_id\nFROM sh_public.spothero_user shu                                                                    --sh_user\nINNER JOIN sfdc.contact sfc ON shu.id = sfc.unique_user_id_c                                        --sfdc_contact to sh_user\nINNER JOIN sh_public.spot_admin sa ON shu.id = sa.user_id                                           --sh_user LJ to sh_spot_admin\nINNER JOIN sh_public.parking_spot shps ON shps.parking_spot_id = sa.parking_spot_id                 --sh_ps LJ to sh_spot_admin\nINNER JOIN sfdc.opportunity_contact_roles_c ocr ON ocr.contact_c = sfc.id                           --sfdc_ocr to sfdc_contact\nINNER JOIN sfdc.opportunity o ON o.id = ocr.opportunity_c AND o.spot_id_c = shps.parking_spot_id    --sfdc_opp to sfdc_ocr AND sfdc_opp to sh_ps\nWHERE sfc.account_id IS NOT NULL\n  AND shps.status NOT IN ('deleted','archived')\n  AND ocr.rate_inventory_specialist_c IS TRUE\n  AND sa.deleted IS FALSE",
   'compiled_code': "\n\nSELECT DISTINCT\n    TRY_CAST(shu.id AS INT) AS sh_user_id\n  , TRY_CAST(sa.parking_spot_id AS INT) AS sh_parking_spot_id\n  , sfc.email\n  , ocr.rate_inventory_specialist_c AS sfdc_is_rate_inventory_specialist\n  , sa.spot_admin_id AS sh_spot_admin_id\n  , sfc.id AS sfdc_contact_id\nFROM sh_public.spothero_user shu                                                                    --sh_user\nINNER JOIN sfdc.contact sfc ON shu.id = sfc.unique_user_id_c                                        --sfdc_contact to sh_user\nINNER JOIN sh_public.spot_admin sa ON shu.id = sa.user_id                                           --sh_user LJ to sh_spot_admin\nINNER JOIN sh_public.parking_spot shps ON shps.parking_spot_id = sa.parking_spot_id                 --sh_ps LJ to sh_spot_admin\nINNER JOIN sfdc.opportunity_contact_roles_c ocr ON ocr.contact_c = sfc.id                           --sfdc_ocr to sfdc_contact\nINNER JOIN sfdc.opportunity o ON o.id = ocr.opportunity_c AND o.spot_id_c = shps.parking_spot_id    --sfdc_opp to sfdc_ocr AND sfdc_opp to sh_ps\nWHERE sfc.account_id IS NOT NULL\n  AND shps.status NOT IN ('deleted','archived')\n  AND ocr.rate_inventory_specialist_c IS TRUE\n  AND sa.deleted IS FALSE"},
    ...
]}

#job_details 
{'id': 760646, 'run_id': 376739307}
```
