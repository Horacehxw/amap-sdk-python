"""Tests for CoordinateAPI."""

import responses as responses_lib

from amap.client import AmapClient

CONVERT_RESPONSE = {
    "status": "1",
    "info": "OK",
    "locations": "106.504962,29.533155",
}


class TestCoordinate:
    """Test coordinate conversion."""

    @responses_lib.activate
    def test_convert_gps(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/assistant/coordinate/convert",
            json=CONVERT_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        result = client.coordinate.convert("106.5,29.5")
        assert result["status"] == "1"
        assert "locations" in result
        req_url = responses_lib.calls[0].request.url
        assert "locations=106.5" in req_url
        assert "coordsys=gps" in req_url

    @responses_lib.activate
    def test_convert_baidu(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/assistant/coordinate/convert",
            json=CONVERT_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        client.coordinate.convert("106.5,29.5", coordsys="baidu")
        req_url = responses_lib.calls[0].request.url
        assert "coordsys=baidu" in req_url

    @responses_lib.activate
    def test_convert_multiple_locations(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/assistant/coordinate/convert",
            json={
                "status": "1",
                "info": "OK",
                "locations": "106.504962,29.533155;106.510000,29.540000",
            },
        )
        client = AmapClient(api_key="test_fake_key")
        client.coordinate.convert("106.5,29.5|106.6,29.6")
        req_url = responses_lib.calls[0].request.url
        assert "locations=106.5" in req_url

    @responses_lib.activate
    def test_convert_mapbar(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/assistant/coordinate/convert",
            json=CONVERT_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        client.coordinate.convert("106.5,29.5", coordsys="mapbar")
        req_url = responses_lib.calls[0].request.url
        assert "coordsys=mapbar" in req_url
