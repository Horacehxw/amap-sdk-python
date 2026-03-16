"""Tests for GeocodingAPI."""

import responses as responses_lib

from amap.client import AmapClient


class TestGeocode:
    """Test forward geocoding."""

    @responses_lib.activate
    def test_geocode_basic(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/geocode/geo",
            json={
                "status": "1",
                "info": "OK",
                "geocodes": [
                    {"formatted_address": "北京市朝阳区", "location": "116.480881,39.989410"}
                ],
            },
        )
        client = AmapClient(api_key="test_fake_key")
        result = client.geocoding.geocode("北京市朝阳区")
        assert result["status"] == "1"
        assert len(result["geocodes"]) == 1
        assert "address=%E5%8C%97%E4%BA%AC" in responses_lib.calls[0].request.url

    @responses_lib.activate
    def test_geocode_with_city(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/geocode/geo",
            json={"status": "1", "info": "OK", "geocodes": []},
        )
        client = AmapClient(api_key="test_fake_key")
        client.geocoding.geocode("天安门", city="北京")
        req_url = responses_lib.calls[0].request.url
        assert "city=" in req_url

    @responses_lib.activate
    def test_geocode_no_city_omits_param(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/geocode/geo",
            json={"status": "1", "info": "OK", "geocodes": []},
        )
        client = AmapClient(api_key="test_fake_key")
        client.geocoding.geocode("北京")
        req_url = responses_lib.calls[0].request.url
        assert "city=" not in req_url


class TestReverseGeocode:
    """Test reverse geocoding."""

    @responses_lib.activate
    def test_reverse_geocode_basic(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/geocode/regeo",
            json={
                "status": "1",
                "info": "OK",
                "regeocode": {"formatted_address": "北京市朝阳区"},
            },
        )
        client = AmapClient(api_key="test_fake_key")
        result = client.geocoding.reverse_geocode("116.480881,39.989410")
        assert result["regeocode"]["formatted_address"] == "北京市朝阳区"
        req_url = responses_lib.calls[0].request.url
        assert "location=116.480881" in req_url
        assert "extensions=base" in req_url
        assert "radius=1000" in req_url

    @responses_lib.activate
    def test_reverse_geocode_with_options(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/geocode/regeo",
            json={"status": "1", "info": "OK", "regeocode": {}},
        )
        client = AmapClient(api_key="test_fake_key")
        client.geocoding.reverse_geocode(
            "116.480881,39.989410",
            extensions="all",
            radius=500,
            poitype="餐饮|商务",
        )
        req_url = responses_lib.calls[0].request.url
        assert "extensions=all" in req_url
        assert "radius=500" in req_url
        assert "poitype=" in req_url

    @responses_lib.activate
    def test_reverse_geocode_no_poitype_omits_param(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/geocode/regeo",
            json={"status": "1", "info": "OK", "regeocode": {}},
        )
        client = AmapClient(api_key="test_fake_key")
        client.geocoding.reverse_geocode("116.0,39.0")
        req_url = responses_lib.calls[0].request.url
        assert "poitype=" not in req_url
