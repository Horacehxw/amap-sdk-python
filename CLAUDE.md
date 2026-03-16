# amap-sdk-python

Python SDK for Amap (高德地图) Web Service REST API.

## Commands
pip install -e ".[dev]"
pytest
pytest -v -m "not integration"

## Conventions
- One namespace class per API module (e.g., GeocodingAPI, PoiAPI)
- Attached to AmapClient as attributes (client.geocoding, client.poi)
- Unit tests mock HTTP with `responses` library
- Integration tests marked @pytest.mark.integration
