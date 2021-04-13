# Module \<`errors`\>
All exceptions that can be raised during handling of a weatherapi request.

class \<`WeatherApiError(Exception)`\>
--------------------------------------
Base exception.

class \<`NoApiKey(WeatherApiError)`\>
-------------------------------------
Raised when no weatherapi key has been provided.

class \<`InvalidApiKey(WeatherApiError)`\>
------------------------------------------
Raised when an invalid weatherapi key has been provided.

class \<`QuotaExceeded(WeatherApiError)`\>
------------------------------------------
Raised when monthly requests limit has been reached.

class \<`ApiKeyDisabled(WeatherApiError)`\>
-------------------------------------------
Raised when weatherapi key is disabled.

class \<`QueryNotProvided(WeatherApiError)`\>
---------------------------------------------
Raised when a query parameter has not been provided.

class \<`InvalidRequestUrl(WeatherApiError)`\>
----------------------------------------------
Raised when weatherapi request url is invalid.

class \<`InvalidLocation(WeatherApiError)`\>
--------------------------------------------
Raised when location request is not found.

class \<`InternalError(WeatherApiError)`\>
------------------------------------------
Raised when an internal weatherapi error is encountered.