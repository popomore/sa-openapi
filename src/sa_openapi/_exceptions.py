"""Exception classes for sa-openapi."""


class SensorsAnalyticsError(Exception):
    """Base exception for all SDK errors."""

    def __init__(self, message: str, code: str | None = None):
        self.message = message
        self.code = code
        super().__init__(self.message)


class AuthenticationError(SensorsAnalyticsError):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, code="AUTH_ERROR")


class NotFoundError(SensorsAnalyticsError):
    """Raised when a resource is not found."""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, code="NOT_FOUND")


class ValidationError(SensorsAnalyticsError):
    """Raised when request validation fails."""

    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, code="VALIDATION_ERROR")


class RateLimitError(SensorsAnalyticsError):
    """Raised when rate limit is exceeded."""

    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, code="RATE_LIMIT_ERROR")


class ServerError(SensorsAnalyticsError):
    """Raised when server returns an error."""

    def __init__(self, message: str = "Server error"):
        super().__init__(message, code="SERVER_ERROR")


class NetworkError(SensorsAnalyticsError):
    """Raised when network request fails."""

    def __init__(self, message: str = "Network error"):
        super().__init__(message, code="NETWORK_ERROR")


class TimeoutError(SensorsAnalyticsError):
    """Raised when request times out."""

    def __init__(self, message: str = "Request timeout"):
        super().__init__(message, code="TIMEOUT_ERROR")
