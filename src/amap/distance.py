"""Distance measurement API."""

from __future__ import annotations


class DistanceAPI:
    """Distance namespace: distance measurement between points."""

    def __init__(self, client) -> None:
        self._client = client

    def measure(
        self,
        origins: str,
        destination: str,
        type: int = 1,
    ) -> dict:
        """Measure distance between origin(s) and a destination.

        Args:
            origins: Up to 100 coordinate pairs separated by "|",
                    each as "lng,lat".
            destination: Destination coordinate as "lng,lat".
            type: Distance type — 0=straight line, 1=driving, 3=walking.

        Returns:
            API response dict with distance results.
        """
        params: dict = {
            "origins": origins,
            "destination": destination,
            "type": str(type),
        }
        return self._client._request("/v3/distance", params)
