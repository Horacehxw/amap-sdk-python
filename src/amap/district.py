"""District query API."""

from __future__ import annotations


class DistrictAPI:
    """District namespace: administrative district queries."""

    def __init__(self, client) -> None:
        self._client = client

    def query(
        self,
        keywords: str | None = None,
        subdistrict: int = 1,
        page: int = 1,
        offset: int = 20,
        extensions: str = "base",
        filter: str | None = None,
    ) -> dict:
        """Query administrative districts.

        Args:
            keywords: District name or adcode.
            subdistrict: Levels of sub-districts to return (0-3).
            page: Page number.
            offset: Results per page (max 20).
            extensions: "base" or "all" (includes boundary coordinates).
            filter: Adcode filter to narrow results.

        Returns:
            API response dict with districts list.
        """
        params: dict = {
            "subdistrict": str(subdistrict),
            "page": str(page),
            "offset": str(offset),
            "extensions": extensions,
        }
        if keywords:
            params["keywords"] = keywords
        if filter:
            params["filter"] = filter
        return self._client._request("/v3/config/district", params)
