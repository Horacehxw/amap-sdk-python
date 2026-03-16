"""Traffic status API."""

from __future__ import annotations


class TrafficAPI:
    """Traffic namespace: real-time traffic status queries."""

    def __init__(self, client) -> None:
        self._client = client

    def road(
        self,
        name: str,
        city: str,
        level: int | None = None,
        extensions: str = "base",
    ) -> dict:
        """Query traffic status for a specific road.

        Args:
            name: Road name.
            city: City name or adcode.
            level: Road level filter (optional).
            extensions: "base" or "all".

        Returns:
            API response dict with traffic status.
        """
        params: dict = {
            "name": name,
            "city": city,
            "extensions": extensions,
        }
        if level is not None:
            params["level"] = str(level)
        return self._client._request("/v3/traffic/status/road", params)

    def circle(
        self,
        location: str,
        radius: int = 1000,
        level: int | None = None,
        extensions: str = "base",
    ) -> dict:
        """Query traffic status within a circular area.

        Args:
            location: Center coordinate as "lng,lat".
            radius: Search radius in meters (default 1000).
            level: Road level filter (optional).
            extensions: "base" or "all".

        Returns:
            API response dict with traffic status.
        """
        params: dict = {
            "location": location,
            "radius": str(radius),
            "extensions": extensions,
        }
        if level is not None:
            params["level"] = str(level)
        return self._client._request("/v3/traffic/status/circle", params)

    def rectangle(
        self,
        rectangle: str,
        level: int | None = None,
        extensions: str = "base",
    ) -> dict:
        """Query traffic status within a rectangular area.

        Args:
            rectangle: Bounding box as "x1,y1;x2,y2" (lower-left;upper-right).
            level: Road level filter (optional).
            extensions: "base" or "all".

        Returns:
            API response dict with traffic status.
        """
        params: dict = {
            "rectangle": rectangle,
            "extensions": extensions,
        }
        if level is not None:
            params["level"] = str(level)
        return self._client._request("/v3/traffic/status/rectangle", params)
