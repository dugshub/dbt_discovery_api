#!/usr/bin/env python

import os
import json
from dotenv import load_dotenv
from src.service_api.DbtCloudService import DbtCloudService

# Load environment variables from .env file
load_dotenv()

def main():
    # Get token from environment variable or use a default for testing
    token = os.environ.get("DBT_CLOUD_TOKEN")
    
    # Initialize the service
    service = DbtCloudService(token=token)
    
    # Account ID to query
    account_id = 19751
    
    try:
        # Get jobs for the account
        print(f"Fetching jobs for account {account_id}...")
        jobs = service.get_jobs(account_id=account_id)
        
        # Pretty print the result
        print("\nJobs:")
        print(json.dumps(jobs, indent=2))
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
