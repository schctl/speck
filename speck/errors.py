"""
All errors that can be raised during a weatherapi request.
https://www.weatherapi.com/docs/
"""

# Functions that make a request to weatherapi.com have the possibility
# of raising one of these errors depending on the response.

class WeatherApiError(Exception): # We use these custom error classes to convert the error code into something more understandable
    """Raised when an unknown weatherapi error is encountered."""
    def __init__(self, message, internal_code):
        self.internal_code = internal_code
        super().__init__(message)

class NoApiKey(WeatherApiError):
    """Raised when no weatherapi key has been provided."""
    pass

class InvalidApiKey(WeatherApiError):
    """Raised when an invalid weatherapi key has been provided."""
    pass

class QuotaExceeded(WeatherApiError):
    """Raised when monthly weatherapi requests has been exceeded."""
    pass

class ApiKeyDisabled(WeatherApiError):
    """Raised when weatherapi key is disabled."""
    pass

class QueryNotProvided(WeatherApiError):
    """Raised when location request has not been provided."""
    pass

class InvalidRequestUrl(WeatherApiError):
    """Raised when weatherapi request url is invalid."""
    pass

class InvalidLocation(WeatherApiError):
    """Raised when location request is not found."""
    pass

class InternalError(WeatherApiError):
    """Raised when an internal weatherapi error is encountered."""
    pass
