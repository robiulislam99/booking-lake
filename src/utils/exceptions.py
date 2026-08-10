"""Shared exception hierarchy."""


class BookingLakeError(Exception):
    """Base error for repository-level failures."""


class ConfigurationError(BookingLakeError):
    """Raised when required configuration is missing or invalid."""


class DataProcessingError(BookingLakeError):
    """Raised when a record cannot be transformed safely."""
