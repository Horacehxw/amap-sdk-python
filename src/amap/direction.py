"""Direction / route planning API."""

from __future__ import annotations


class DirectionAPI:
    """Direction namespace: walking, driving, transit, and bicycling routes."""

    def __init__(self, client) -> None:
        self._client = client

    def walking(self, origin: str, destination: str) -> dict:
        """Plan a walking route.

        Args:
            origin: Start coordinate as "lng,lat".
            destination: End coordinate as "lng,lat".

        Returns:
            API response dict with route info.
        """
        params: dict = {"origin": origin, "destination": destination}
        return self._client._request("/v3/direction/walking", params)

    def driving(
        self,
        origin: str,
        destination: str,
        strategy: int | None = None,
        waypoints: str | None = None,
        extensions: str = "base",
    ) -> dict:
        """Plan a driving route.

        Args:
            origin: Start coordinate as "lng,lat".
            destination: End coordinate as "lng,lat".
            strategy: Route strategy (0=speed, 13=no highways, 14=avoid tolls, etc.).
            waypoints: Up to 16 intermediate points, "|" separated.
            extensions: "base" or "all".

        Returns:
            API response dict with route info.
        """
        params: dict = {
            "origin": origin,
            "destination": destination,
            "extensions": extensions,
        }
        if strategy is not None:
            params["strategy"] = str(strategy)
        if waypoints:
            params["waypoints"] = waypoints
        return self._client._request("/v3/direction/driving", params)

    def transit(
        self,
        origin: str,
        destination: str,
        city: str,
        cityd: str | None = None,
        strategy: int = 0,
    ) -> dict:
        """Plan a public transit route.

        Args:
            origin: Start coordinate as "lng,lat".
            destination: End coordinate as "lng,lat".
            city: Origin city name or adcode (REQUIRED).
            cityd: Destination city name or adcode (for cross-city transit).
            strategy: Transit strategy (0=fastest, 1=min cost, etc.).

        Returns:
            API response dict with transit route info.
        """
        params: dict = {
            "origin": origin,
            "destination": destination,
            "city": city,
            "strategy": str(strategy),
        }
        if cityd:
            params["cityd"] = cityd
        return self._client._request("/v3/direction/transit/integrated", params)

    def bicycling(self, origin: str, destination: str) -> dict:
        """Plan a bicycling route (v4 API).

        Args:
            origin: Start coordinate as "lng,lat".
            destination: End coordinate as "lng,lat".

        Returns:
            API response dict with bicycling route info.
        """
        params: dict = {"origin": origin, "destination": destination}
        return self._client._request(
            "/v4/direction/bicycling", params, api_version="v4"
        )
