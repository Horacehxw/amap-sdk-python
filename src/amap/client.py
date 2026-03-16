"""Core HTTP client for the Amap Web Service API."""

from __future__ import annotations

import os
import time

import requests

from amap.distance import DistanceAPI
from amap.district import DistrictAPI
from amap.exceptions import AmapAPIError, AmapNetworkError
from amap.geocoding import GeocodingAPI
from amap.inputtips import InputTipsAPI
from amap.poi import PoiAPI
from amap.weather import WeatherAPI

BASE_URL = "https://restapi.amap.com"
TIMEOUT = 10
MAX_RETRIES = 3
BACKOFF_BASE = 0.5


class AmapClient:
    """Low-level client that handles auth, retries, and error mapping."""

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.environ.get("AMAP_MAPS_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key is required. Pass api_key= or set AMAP_MAPS_API_KEY."
            )
        self._session = requests.Session()

        # Namespace APIs
        self.geocoding = GeocodingAPI(self)
        self.poi = PoiAPI(self)
        self.weather = WeatherAPI(self)
        self.district = DistrictAPI(self)
        self.inputtips = InputTipsAPI(self)
        self.distance = DistanceAPI(self)

    def _request(
        self,
        path: str,
        params: dict | None = None,
        api_version: str = "v3",
    ) -> dict:
        """Send a GET request with key injection, retry, and error checking.

        Args:
            path: URL path starting with / (e.g. "/v3/geocode/geo").
            params: Query parameters (key is injected automatically).
            api_version: "v3" or "v4" — determines error-checking logic.

        Returns:
            Parsed JSON response dict.

        Raises:
            AmapAPIError: On business-level errors from Amap.
            AmapNetworkError: On HTTP failures after retries exhausted.
        """
        url = f"{BASE_URL}{path}"
        params = dict(params or {})
        params["key"] = self.api_key

        last_exc: Exception | None = None
        for attempt in range(MAX_RETRIES + 1):
            try:
                resp = self._session.get(url, params=params, timeout=TIMEOUT)
                if resp.status_code >= 500:
                    last_exc = AmapNetworkError(
                        f"HTTP {resp.status_code} from {url}"
                    )
                    if attempt < MAX_RETRIES:
                        time.sleep(BACKOFF_BASE * (2**attempt))
                        continue
                    raise last_exc
                resp.raise_for_status()
                data = resp.json()
            except requests.RequestException as exc:
                last_exc = AmapNetworkError(str(exc))
                if attempt < MAX_RETRIES:
                    time.sleep(BACKOFF_BASE * (2**attempt))
                    continue
                raise last_exc from exc

            # Business-error checking
            if api_version == "v3" and data.get("status") != "1":
                raise AmapAPIError(
                    infocode=data.get("infocode", ""),
                    info=data.get("info", ""),
                    url=url,
                )
            if api_version == "v4" and data.get("errcode", -1) != 0:
                raise AmapAPIError(
                    infocode=str(data.get("errcode", "")),
                    info=data.get("errmsg", ""),
                    url=url,
                )
            return data

        # Should not reach here, but just in case
        raise last_exc or AmapNetworkError("Request failed")
