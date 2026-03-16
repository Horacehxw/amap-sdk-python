"""Tests for DistrictAPI."""

import responses as responses_lib

from amap.client import AmapClient

DISTRICT_RESPONSE = {
    "status": "1",
    "info": "OK",
    "districts": [
        {
            "citycode": "023",
            "adcode": "500000",
            "name": "重庆市",
            "level": "province",
            "districts": [],
        }
    ],
}


class TestDistrict:
    """Test district queries."""

    @responses_lib.activate
    def test_query_basic(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/config/district",
            json=DISTRICT_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        result = client.district.query(keywords="重庆")
        assert result["districts"][0]["name"] == "重庆市"
        req_url = responses_lib.calls[0].request.url
        assert "keywords=" in req_url
        assert "subdistrict=1" in req_url

    @responses_lib.activate
    def test_query_with_options(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/config/district",
            json=DISTRICT_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        client.district.query(
            keywords="北京",
            subdistrict=2,
            page=2,
            offset=10,
            extensions="all",
            filter="110000",
        )
        req_url = responses_lib.calls[0].request.url
        assert "subdistrict=2" in req_url
        assert "page=2" in req_url
        assert "offset=10" in req_url
        assert "extensions=all" in req_url
        assert "filter=110000" in req_url

    @responses_lib.activate
    def test_query_defaults(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/config/district",
            json=DISTRICT_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        client.district.query()
        req_url = responses_lib.calls[0].request.url
        assert "subdistrict=1" in req_url
        assert "page=1" in req_url
        assert "offset=20" in req_url
        assert "extensions=base" in req_url
        assert "keywords=" not in req_url
        assert "filter=" not in req_url
