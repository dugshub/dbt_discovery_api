"""Custom exceptions for the discovery API."""


class DiscoveryApiError(Exception):
    """Base exception for all discovery API errors."""
    pass


class AuthenticationError(DiscoveryApiError):
    """Raised when authentication fails."""
    pass


class ResourceNotFoundError(DiscoveryApiError):
    """Raised when a requested resource is not found."""
    pass


class QueryError(DiscoveryApiError):
    """Raised when a query fails."""
    pass


class FilterError(DiscoveryApiError):
    """Raised when a filter specification is invalid."""
    pass


class ServiceUnavailableError(DiscoveryApiError):
    """Raised when the dbt Cloud API is unavailable."""
    pass