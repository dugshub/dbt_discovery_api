"""Tests for base models."""

import pytest
from datetime import datetime
from src.discovery_api.models.base import RuntimeReport, RunStatus


def test_run_status_enum():
    """Test RunStatus enum values."""
    assert RunStatus.SUCCESS.value == "success"
    assert RunStatus.FAILURE.value == "failure"
    assert RunStatus.CANCELLED.value == "cancelled"

    # Test case insensitive
    assert RunStatus("SUCCESS") == RunStatus.SUCCESS
    assert RunStatus("success") == RunStatus.SUCCESS

    # Test invalid status
    with pytest.raises(ValueError):
        RunStatus("invalid")


def test_runtime_report():
    """Test RuntimeReport model."""
    # Test creation with minimal required fields
    now = datetime.now()
    report = RuntimeReport(
        job_id="123",
        run_id="456",
        runtime=10.5,
        start_time=now,
        end_time=now
    )
    
    assert report.job_id == "123"
    assert report.run_id == "456"
    assert report.runtime == 10.5
    assert report.start_time == now
    assert report.end_time == now
    assert report.model_id is None  # Optional field

    # Test creation with all fields
    report = RuntimeReport(
        job_id="123",
        run_id="456",
        model_id="789",
        runtime=10.5,
        start_time=now,
        end_time=now
    )
    
    assert report.model_id == "789"

    # Test validation
    with pytest.raises(ValueError):
        RuntimeReport(
            job_id="123",
            run_id="456",
            runtime="not a float",  # Invalid type
            start_time=now,
            end_time=now
        )