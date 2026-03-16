"""Static map image API."""

from __future__ import annotations


class StaticMapAPI:
    """Static map namespace: generate static map PNG images."""

    def __init__(self, client) -> None:
        self._client = client

    def generate(
        self,
        location: str,
        zoom: int,
        size: str = "400*400",
        scale: int = 1,
        markers: str | None = None,
        labels: str | None = None,
        paths: str | None = None,
        traffic: int = 0,
    ) -> bytes:
        """Generate a static map image.

        Args:
            location: Center coordinate as "lng,lat".
            zoom: Zoom level (1-17).
            size: Image size as "width*height" (max 1024*1024).
            scale: 1 for normal, 2 for retina.
            markers: Marker specification string per Amap spec.
            labels: Label specification string per Amap spec.
            paths: Path specification string per Amap spec.
            traffic: 0=no traffic layer, 1=show traffic.

        Returns:
            PNG image bytes.
        """
        params: dict = {
            "location": location,
            "zoom": str(zoom),
            "size": size,
            "scale": str(scale),
            "traffic": str(traffic),
        }
        if markers:
            params["markers"] = markers
        if labels:
            params["labels"] = labels
        if paths:
            params["paths"] = paths
        return self._client._request_raw("/v3/staticmap", params)
