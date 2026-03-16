"""Geocoding and reverse geocoding API."""

from __future__ import annotations


class GeocodingAPI:
    """Geocoding namespace: forward and reverse geocoding."""

    def __init__(self, client) -> None:
        self._client = client

    def geocode(self, address: str, city: str | None = None) -> dict:
        """Forward geocode an address to coordinates.

        Args:
            address: Structured address string.
            city: Optional city name or adcode to narrow results.

        Returns:
            API response dict with geocodes list.
        """
        params: dict = {"address": address}
        if city:
            params["city"] = city
        return self._client._request("/v3/geocode/geo", params)

    def reverse_geocode(
        self,
        location: str,
        extensions: str = "base",
        radius: int = 1000,
        poitype: str | None = None,
    ) -> dict:
        """Reverse geocode coordinates to address.

        Args:
            location: Coordinates as "lng,lat".
            extensions: "base" for basic info, "all" for detailed.
            radius: Search radius in meters (0-3000).
            poitype: POI type filter, "|" separated.

        Returns:
            API response dict with regeocode info.
        """
        params: dict = {
            "location": location,
            "extensions": extensions,
            "radius": str(radius),
        }
        if poitype:
            params["poitype"] = poitype
        return self._client._request("/v3/geocode/regeo", params)
