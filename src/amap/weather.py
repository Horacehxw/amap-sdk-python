"""Weather API."""

from __future__ import annotations


class WeatherAPI:
    """Weather namespace: current conditions and forecasts."""

    def __init__(self, client) -> None:
        self._client = client

    def weather(self, city: str, extensions: str = "base") -> dict:
        """Get weather information.

        Args:
            city: Adcode for the city (e.g. "500000" for Chongqing).
            extensions: "base" for current weather (returns "lives"),
                       "all" for forecast (returns "forecasts").

        Returns:
            API response dict with lives or forecasts.
        """
        params: dict = {
            "city": city,
            "extensions": extensions,
        }
        return self._client._request("/v3/weather/weatherInfo", params)
