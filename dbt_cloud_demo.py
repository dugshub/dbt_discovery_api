#!/usr/bin/env python

import os

from src.service_api.DbtCloudService import DbtCloudService
from src.service_api.models import DbtJobsResponse, DbtAccountResponse, DbtJob

# Get token from environment variable or use a default for testing
token = os.environ.get("DBT_SERVICE_TOKEN")

# Initialize the service
service = DbtCloudService(token=token)

# Account ID to query
ACCOUNT_ID = 19751


print(f"Fetching account information for account {ACCOUNT_ID}...")
account_info: DbtAccountResponse = service.get_account(account_id=ACCOUNT_ID)

# Pretty print the result
print("\nAccount Information:")
print(account_info.to_json())

# Get jobs as well
print(f"\nFetching jobs for account {ACCOUNT_ID}...")

jobs_response: DbtJobsResponse = service.get_jobs(account_id=ACCOUNT_ID)
print("\nJobs:")
print(jobs_response.to_json())

# Example of accessing typed data
if jobs_response.data:
    first_job: DbtJob = jobs_response.data[0]
    print(f"\nFirst job: {first_job.name}")
    print(f"Job type: {first_job.job_type}")
    print(f"Created at: {first_job.created_at}")
    
    if first_job.schedule and first_job.schedule.cron:
        print(f"Schedule: {first_job.schedule.cron}")

