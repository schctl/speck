# Module \<`errors`\>
All exceptions that can be raised during handling of a weatherapi request.

#

<sup>*class*</sup> `WeatherApiError(Exception)`
--------------------------------------
Base exception.

<sup>*class*</sup> `NoApiKey(WeatherApiError)`
-------------------------------------
Raised when no weatherapi key has been provided.

<sup>*class*</sup> `InvalidApiKey(WeatherApiError)`
------------------------------------------
Raised when an invalid weatherapi key has been provided.

<sup>*class*</sup> `QuotaExceeded(WeatherApiError)`
------------------------------------------
Raised when monthly requests limit has been reached.

<sup>*class*</sup> `ApiKeyDisabled(WeatherApiError)`
-------------------------------------------
Raised when weatherapi key is disabled.

<sup>*class*</sup> `QueryNotProvided(WeatherApiError)`
---------------------------------------------
Raised when a query parameter has not been provided.

<sup>*class*</sup> `InvalidRequestUrl(WeatherApiError)`
----------------------------------------------
Raised when weatherapi request url is invalid.

<sup>*class*</sup> `InvalidLocation(WeatherApiError)`
--------------------------------------------
Raised when location request is not found.

<sup>*class*</sup> `InternalError(WeatherApiError)`
------------------------------------------
Raised when an internal weatherapi error is encountered.