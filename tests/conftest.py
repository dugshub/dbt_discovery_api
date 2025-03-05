import pytest
import os
import sys
import logging

# Add project root to python path if not already there
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

def pytest_configure(config):
    """Add custom markers and configure logging."""
    # Add custom markers
    config.addinivalue_line(
        "markers", "integration: mark test as integration test requiring API access"
    )
    
    # Create a logs directory if it doesn't exist
    if not os.path.exists("logs"):
        os.makedirs("logs")
        
    # Create a file handler for performance logging
    file_handler = logging.FileHandler("logs/performance.log", mode="w")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    
    # Get the logger and add the file handler
    logger = logging.getLogger("dbt_discovery_api")
    logger.addHandler(file_handler)
    
    # Set pytest's capturing log level to show INFO+ logs
    config.option.log_cli_level = "INFO"
    config.option.log_cli = True

def pytest_addoption(parser):
    """Add command line options to pytest."""
    parser.addoption(
        "--run-integration",
        action="store_true",
        default=False,
        help="Run integration tests requiring API access",
    )

def pytest_collection_modifyitems(config, items):
    """Skip integration tests unless --run-integration is specified."""
    if not config.getoption("--run-integration"):
        skip_integration = pytest.mark.skip(reason="Need --run-integration option to run")
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip_integration)