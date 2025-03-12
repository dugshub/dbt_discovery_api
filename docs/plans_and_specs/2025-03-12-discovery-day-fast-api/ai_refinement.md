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
    
    def __hash__(self) -> int:
        """Make filter hashable for cache key generation"""
        filter_tuple = (
            tuple(sorted(self.tags)) if self.tags else None,
            self.materialization,
            self.min_runtime,
            self.max_runtime
        )
        return hash(filter_tuple)

class ModelFilter(SearchFilter):
    models: Optional[List[Model]] #this is model_object
    model_ids: Optional[List[str]] #this is project_name.model_name


class ProjectFilter(SearchFilter):
    projects: Optional[List[Project]]
    project_ids: Optional[List[str]]
    include_or_exclude: Optional[str] = "include"

class CachingStrategy:
    """Controls caching behavior across the API"""
    
    cache_ttl: int = 300  # Time to live for cache entries in seconds (default: 5 minutes)
    enable_caching: bool = True  # Whether caching is enabled globally
    
    def should_refresh(self, cache_key: str) -> bool:
        """Check if a cache entry should be refreshed based on TTL"""
        pass
        
    def update_timestamp(self, cache_key: str) -> None:
        """Update the timestamp for a cache entry"""
        pass
        
    def invalidate_cache(self, scope: str = "all") -> None:
        """Invalidate cache entries by scope (all, models, jobs, runs)"""
        pass
```

Classes:
```python

class dbtAccount:
    environment: ['production','staging']
    projects: List[Project]
    filter: Optional[ProjectFilter] = None
    caching_strategy: Optional[CachingStrategy] = None

    def __init__(self, token: str, caching_strategy: Optional[CachingStrategy] = None):
        self.caching_strategy = caching_strategy or CachingStrategy()
        self._projects_cache: Optional[List[Project]] = None

    def get_projects(self, filter: ProjectFilter = None, refresh: bool = False) -> List[Project]:
        # Use caching strategy to determine if refresh is needed
        pass

    def get_jobs(self, filter: SearchFilter = None, refresh: bool = False) -> List[Job]:
        # Searches across all projects (unless included_)
        pass

    def get_models(self, filter: SearchFilter = None, refresh: bool = False) -> List[Model]:
        # Searches across all projects
        pass

    def get_runs(self, limit: int = 10, filter: SearchFilter = None, refresh: bool = False) -> List[Run]:
        # Searches across all projects
        pass
        
    def slowest_models(self, slowest_n: int = 5, last_n_runs: int = 1, filter: SearchFilter = None, refresh: bool = False) -> List[Model]:
        # Finds slowest models across all projects
        pass
        
    def longest_running_jobs(self, longest_n: int = 5, last_n_runs: int = 1, filter: SearchFilter = None, model_filter: ModelFilter = None, refresh: bool = False) -> List[Job]:
        # Finds longest running jobs across all projects
        pass
        
    def invalidate_cache(self, scope: str = "all") -> None:
        # Invalidate cache entries by scope
        pass

class Project:
    project_id: str
    models: List[Model]
    jobs: List[Job]
    model_count: int
    job_count: int
    caching_strategy: CachingStrategy
    
    def __init__(self, project_id: str, caching_strategy: Optional[CachingStrategy] = None):
        self._models_cache: Optional[List[Model]] = None
        self._jobs_cache: Optional[List[Job]] = None
        self.caching_strategy = caching_strategy

    def get_models(self, filter: SearchFilter = None, refresh: bool = False) -> List[Model]: 
        # Use caching strategy to determine if refresh is needed
        pass

    def get_jobs(self, filter: SearchFilter = None, refresh: bool = False) -> List[Job]:
        # Use caching strategy for job data
        pass

    def slowest_models(self, slowest_n: int = 5, last_n_runs: int = 1, filter: SearchFilter = None, refresh: bool = False) -> List[Model]:
        # Finds slowest models across all projects, by default uses last run if last_n_runs > 1 uses historical runs (requiring multiple queries)
        pass

    def longest_running_jobs(self, longest_n: int = 5, last_n_runs: int = 1, filter: SearchFilter = None, model_filter: ModelFilter = None, refresh: bool = False) -> List[Job]:
        # This should use job.get_average_job_runtime(), passing the filter params
        pass




class Model:
    model_id: str #this is project_name.model_name
    last_run_status: RunStatus
    last_run_runtime: float
    last_run_start_time: datetime
    last_run_end_time: datetime
    
    def __init__(self, model_name: str, project_name: str, caching_strategy: Optional[CachingStrategy] = None):
        # Initialize cache properties
        self._runs_cache: Dict[int, List[Run]] = {}
        self._sql_cache: Optional[str] = None
        self._jobs_cache: Optional[List[Job]] = None
        self.caching_strategy = caching_strategy
        
        # Load initial data from last run
        last_run = self.get_last_run()
        self.last_run_status = last_run.status
        ...

        def get_last_run(self, refresh: bool = False) -> Run:
            # Check caching strategy before fetching
            pass

        def get_runs(self, last_n: int = 5, filter: SearchFilter = None, refresh: bool = False) -> List[Run]:
            # Use _runs_cache if available and not refreshing
            cache_key = f"runs_{last_n}_{hash(filter) if filter else 'all'}"
            pass

        def get_sql(self, refresh: bool = False) -> str:
            # Use _sql_cache if available and not refreshing
            pass

        def freshness(self) -> RunStatus:
            pass

        def get_jobs(self, refresh: bool = False) -> List[Job]: 
            # Returns all jobs that this model is triggered in
            # Use _jobs_cache if available
            pass
        
class Job:
    job_id: str
    last_run_status: RunStatus
    last_run_runtime: float
    last_run_start_time: datetime
    last_run_end_time: datetime

    def __init__(self, job_id: str, caching_strategy: Optional[CachingStrategy] = None):
        # Initialize cache properties
        self._models_cache: Optional[List[Model]] = None
        self._runs_cache: Dict[int, List[Run]] = {}
        self._slowest_models_cache: Dict[str, List[Model]] = {}
        self.caching_strategy = caching_strategy
        
        # Load initial data
        last_run = self.get_last_run()
        self.last_run_status = last_run.status
        ...


    def get_models(self, filter: SearchFilter = None, refresh: bool = False) -> List[Model]:
        # Use caching based on filter parameters
        cache_key = f"models_{hash(filter) if filter else 'all'}"
        pass

    def get_last_run(self, refresh: bool = False) -> Run:
        # Check caching strategy before fetching
        pass

    def get_runs(self, last_n: int = 5, refresh: bool = False) -> List[Run]:
        # Use runs cache with last_n as key
        pass

    def get_slowest_models(self, slowest_n: int = 5, filter: SearchFilter = None, refresh: bool = False) -> List[Model]:
        # Use cached results if available
        cache_key = f"slowest_{slowest_n}_{hash(filter) if filter else 'all'}"
        pass

    def get_runtimes(self, last_n: int = 5, by_model: bool = False, refresh: bool = False) -> List[RuntimeReport]:
        # Returns the last N runtimes (not run objects) for the given job
        # Use cached data when appropriate
        pass

    def get_average_job_runtime(self, last_n: int = 5, filter: SearchFilter = None, model_filter: ModelFilter = None, refresh: bool = False) -> float: 
        # Filter by tags within models so we can get average_job_time for jobs containing models tagged with marketing
        pass

    def average_historical_model_runtime(self, slowest_n: int = 5, last_n_runs: int = 5, filter: SearchFilter = None, model_filter: ModelFilter = None, refresh: bool = False) -> float: 
        # Calculates the average runtime for a model over the last N runs
        # Use batch query to optimize multiple model runs fetching
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

    def __init__(self, run_id: str, caching_strategy: Optional[CachingStrategy] = None):
        self._models_cache: Optional[List[Model]] = None
        self.caching_strategy = caching_strategy
        pass

    def get_models(self, filter: SearchFilter = None, refresh: bool = False) -> List[Model]:
        # Use cached models if available
        cache_key = f"models_{hash(filter) if filter else 'all'}"
        pass

    def get_slowest_models(self, slowest_n: int = 5, filter: SearchFilter = None, refresh: bool = False) -> List[Model]:
        # Could use cached results if calculated previously
        pass

    def average_model_runtime(self, slowest_n: int = 5, filter: SearchFilter = None, model_filter: ModelFilter = None, refresh: bool = False) -> float: 
        # Calculates the average runtime, allowing it to be filtered to the worst offenders
        pass
```

## Endpoints

```python
GET /projects
GET /projects/{project_id}
GET /projects/{project_id}/models
GET /projects/{project_id}/jobs

GET /models
GET /models/{model_id}
GET /models/{model_id}/runs
GET /models/{model_id}/jobs
GET /models/{model_id}/sql

GET /jobs
GET /jobs/{job_id}
GET /jobs/{job_id}/models
GET /jobs/{job_id}/runs
GET /jobs/{job_id}/slowest_models

GET /runs
GET /runs/{run_id}
GET /runs/{run_id}/models

GET /account/slowest_models
GET /account/longest_running_jobs
```

## Caching Implementation Strategy

### Immediate Implementation
- Basic `CachingStrategy` class with TTL management
- Object-level caching for most frequently accessed properties
- Add `refresh` parameter to key data access methods

### Future Enhancements
- More sophisticated cache invalidation based on dependencies (e.g., invalidate model cache when job changes)
- External cache provider support (Redis, memcached) for distributed environments
- Adaptive TTL based on data update frequency patterns
- Cache persistence across application restarts for longer-lived data

The caching strategy should be implemented from the beginning as part of the core API design. This ensures that performance considerations are built into the architecture rather than added as an afterthought. Since the caching logic is cleanly encapsulated in the `CachingStrategy` class, it can be enhanced over time without disrupting the overall API design.
