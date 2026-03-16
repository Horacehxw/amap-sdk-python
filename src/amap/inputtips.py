"""Input tips (autocomplete) API."""

from __future__ import annotations


class InputTipsAPI:
    """InputTips namespace: autocomplete suggestions."""

    def __init__(self, client) -> None:
        self._client = client

    def suggest(
        self,
        keywords: str,
        type: str | None = None,
        location: str | None = None,
        city: str | None = None,
        citylimit: bool = False,
        datatype: str = "all",
    ) -> dict:
        """Get autocomplete suggestions for input text.

        Args:
            keywords: Input text to autocomplete.
            type: POI type filter.
            location: Nearby location as "lng,lat" for relevance.
            city: City name or adcode.
            citylimit: Whether to limit results to the specified city.
            datatype: Data types to return: "all", "poi", "bus", "busline".

        Returns:
            API response dict with tips list.
        """
        params: dict = {
            "keywords": keywords,
            "datatype": datatype,
        }
        if citylimit:
            params["citylimit"] = "true"
        if type:
            params["type"] = type
        if location:
            params["location"] = location
        if city:
            params["city"] = city
        return self._client._request("/v3/assistant/inputtips", params)
