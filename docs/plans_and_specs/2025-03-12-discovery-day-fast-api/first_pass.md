#This was done 100% by 'hand' (autocomplete obviously helps). This is the level I get to on my own before getting
#the ai to help me . he odd question here and there - but AI involvement didn't come until caching in the next design
#from there, AI 100% to fill out the spec. Minor adjustments made by me

Type:
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
