"""POI search API (v5)."""

from __future__ import annotations


class PoiAPI:
    """POI namespace: text, around, polygon search and detail lookup."""

    def __init__(self, client) -> None:
        self._client = client

    def text_search(
        self,
        keywords: str | None = None,
        types: str | None = None,
        region: str | None = None,
        city_limit: bool | None = None,
        show_fields: str | None = None,
        page_size: int = 10,
        page_num: int = 1,
    ) -> dict:
        """Search POIs by keywords and/or types.

        Args:
            keywords: Search keywords.
            types: POI type codes.
            region: City name or adcode.
            city_limit: Whether to limit results to region.
            show_fields: Extra fields: "business", "children", "indoor", "navi", "photos".
            page_size: Results per page (default 10).
            page_num: Page number (default 1).

        Returns:
            API response dict with pois list.
        """
        params: dict = {
            "page_size": str(page_size),
            "page_num": str(page_num),
        }
        if keywords:
            params["keywords"] = keywords
        if types:
            params["types"] = types
        if region:
            params["region"] = region
        if city_limit is not None:
            params["city_limit"] = "true" if city_limit else "false"
        if show_fields:
            params["show_fields"] = show_fields
        return self._client._request("/v5/place/text", params)

    def around_search(
        self,
        location: str,
        keywords: str | None = None,
        types: str | None = None,
        radius: int = 5000,
        sortrule: str = "distance",
        show_fields: str | None = None,
        page_size: int = 10,
        page_num: int = 1,
    ) -> dict:
        """Search POIs around a location.

        Args:
            location: Center point as "lng,lat".
            keywords: Search keywords.
            types: POI type codes.
            radius: Search radius in meters (default 5000).
            sortrule: Sort rule, "distance" or "weight".
            show_fields: Extra fields to return.
            page_size: Results per page (default 10).
            page_num: Page number (default 1).

        Returns:
            API response dict with pois list.
        """
        params: dict = {
            "location": location,
            "radius": str(radius),
            "sortrule": sortrule,
            "page_size": str(page_size),
            "page_num": str(page_num),
        }
        if keywords:
            params["keywords"] = keywords
        if types:
            params["types"] = types
        if show_fields:
            params["show_fields"] = show_fields
        return self._client._request("/v5/place/around", params)

    def polygon_search(
        self,
        polygon: str,
        keywords: str | None = None,
        types: str | None = None,
        show_fields: str | None = None,
        page_size: int = 10,
        page_num: int = 1,
    ) -> dict:
        """Search POIs within a polygon area.

        Args:
            polygon: Coordinate pairs separated by "|".
            keywords: Search keywords.
            types: POI type codes.
            show_fields: Extra fields to return.
            page_size: Results per page (default 10).
            page_num: Page number (default 1).

        Returns:
            API response dict with pois list.
        """
        params: dict = {
            "polygon": polygon,
            "page_size": str(page_size),
            "page_num": str(page_num),
        }
        if keywords:
            params["keywords"] = keywords
        if types:
            params["types"] = types
        if show_fields:
            params["show_fields"] = show_fields
        return self._client._request("/v5/place/polygon", params)

    def detail(
        self,
        id: str,
        show_fields: str | None = None,
    ) -> dict:
        """Get POI detail by ID(s).

        Args:
            id: Up to 10 POI IDs separated by "|".
            show_fields: Extra fields to return.

        Returns:
            API response dict with poi details.
        """
        params: dict = {"id": id}
        if show_fields:
            params["show_fields"] = show_fields
        return self._client._request("/v5/place/detail", params)
