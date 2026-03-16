class AmapAPIError(Exception):
    """Raised when Amap API returns a business error."""

    def __init__(self, infocode: str, info: str, url: str = ""):
        self.infocode = infocode
        self.info = info
        self.url = url
        super().__init__(f"Amap API error {infocode}: {info}")


class AmapNetworkError(Exception):
    """Raised on HTTP-level failures (timeout, 5xx, connection error)."""
