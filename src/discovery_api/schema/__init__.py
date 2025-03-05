"""
Schema package for dbt discovery API.

Contains the generated GraphQL schema types for interacting with dbt Cloud.
"""

from src.discovery_api.schema.schema import DefinitionResourcesFilter

__all__ = ["DefinitionResourcesFilter"]