"""
Tests for API layer Pydantic models.
"""

from datetime import datetime
from src.models import Model, ModelHistoricalRun
from src.api import ModelMetadata, RunStatus, ProjectMetadata


def test_model_orm_mode():
    """Test that service models work with from_attributes mode."""
    model = Model(name="test_model", unique_id="model.test.test_model")
    model_dict = model.model_dump()
    new_model = Model.model_validate(model_dict)
    assert new_model.name == model.name
    assert new_model.unique_id == model.unique_id


def test_model_metadata_from_orm():
    """Test creating API model from service model using model_validate."""
    # Create a service model
    service_model = Model(
        name="test_model",
        unique_id="model.test.test_model",
        materialized_type="table",
        tags=["finance", "daily"],
        database="analytics",
        db_schema="public",
        description="A test model"
    )
    
    # Convert to API model using model_validate
    api_model = ModelMetadata.model_validate(service_model)
    
    # Verify the conversion was successful
    assert api_model.name == service_model.name
    assert api_model.unique_id == service_model.unique_id
    assert api_model.materialized == service_model.materialized_type
    assert api_model.tags == service_model.tags
    assert api_model.database == service_model.database
    assert api_model.schema == service_model.db_schema
    assert api_model.description == service_model.description


def test_run_status_from_orm():
    """Test creating RunStatus from ModelHistoricalRun using model_validate."""
    # Create a service model run
    now = datetime.now()
    run = ModelHistoricalRun(
        name="test_model",
        resource_type="model",  # Required field
        run_id="1234",
        status="success",
        run_generated_at=now,
        execution_time=15.5,
        error=None
    )
    
    # Convert to API model using model_validate
    api_run = RunStatus.model_validate(run)
    
    # Verify the conversion was successful
    assert api_run.status == run.status
    assert api_run.run_id == run.run_id
    assert api_run.run_time == run.run_generated_at
    assert api_run.execution_time == run.execution_time
    assert api_run.error_message is None


def test_project_metadata_from_orm():
    """Test creating ProjectMetadata from dictionary using model_validate."""
    # Create a dictionary that simulates the environment service response
    environment_data = {
        "dbt_project_name": "test_project",
        "adapter_type": "snowflake",
        "environment_id": 12345,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    
    # Convert to API model using model_validate
    project_metadata = ProjectMetadata.model_validate(environment_data)
    
    # Verify the conversion was successful
    assert project_metadata.dbt_project_name == environment_data["dbt_project_name"]
    assert project_metadata.adapter_type == environment_data["adapter_type"]
    assert project_metadata.environment_id == environment_data["environment_id"]
    assert project_metadata.created_at == environment_data["created_at"]
    assert project_metadata.updated_at == environment_data["updated_at"]