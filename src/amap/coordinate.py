"""Coordinate conversion API."""

from __future__ import annotations


class CoordinateAPI:
    """Coordinate namespace: convert between coordinate systems."""

    def __init__(self, client) -> None:
        self._client = client

    def convert(self, locations: str, coordsys: str = "gps") -> dict:
        """Convert coordinates from other systems to Amap (GCJ-02).

        Args:
            locations: Up to 40 coordinate pairs, "|" separated, each as "lng,lat".
            coordsys: Source coordinate system — "gps", "mapbar", "baidu", or "autonavi".

        Returns:
            API response dict with converted locations.
        """
        params: dict = {
            "locations": locations,
            "coordsys": coordsys,
        }
        return self._client._request("/v3/assistant/coordinate/convert", params)
