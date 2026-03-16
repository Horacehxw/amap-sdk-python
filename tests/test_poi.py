"""Tests for PoiAPI."""

import responses as responses_lib

from amap.client import AmapClient

V5_POI_RESPONSE = {
    "status": "1",
    "info": "OK",
    "infocode": "10000",
    "count": "1",
    "pois": [
        {"name": "海底捞", "id": "B000A8UIN8", "type": "餐饮服务"}
    ],
}


class TestTextSearch:
    """Test POI text search."""

    @responses_lib.activate
    def test_text_search_with_keywords(self):
        responses_lib.get(
            "https://restapi.amap.com/v5/place/text",
            json=V5_POI_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        result = client.poi.text_search(keywords="海底捞")
        assert result["pois"][0]["name"] == "海底捞"
        req_url = responses_lib.calls[0].request.url
        assert "keywords=" in req_url
        assert "page_size=10" in req_url
        assert "page_num=1" in req_url

    @responses_lib.activate
    def test_text_search_with_all_params(self):
        responses_lib.get(
            "https://restapi.amap.com/v5/place/text",
            json=V5_POI_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        client.poi.text_search(
            keywords="火锅",
            types="050000",
            region="重庆",
            city_limit=True,
            show_fields="business",
            page_size=20,
            page_num=2,
        )
        req_url = responses_lib.calls[0].request.url
        assert "types=050000" in req_url
        assert "city_limit=true" in req_url
        assert "show_fields=business" in req_url
        assert "page_size=20" in req_url
        assert "page_num=2" in req_url

    @responses_lib.activate
    def test_text_search_city_limit_false(self):
        responses_lib.get(
            "https://restapi.amap.com/v5/place/text",
            json=V5_POI_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        client.poi.text_search(keywords="test", city_limit=False)
        req_url = responses_lib.calls[0].request.url
        assert "city_limit=false" in req_url


class TestAroundSearch:
    """Test POI around search."""

    @responses_lib.activate
    def test_around_search_basic(self):
        responses_lib.get(
            "https://restapi.amap.com/v5/place/around",
            json=V5_POI_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        result = client.poi.around_search("106.504962,29.533155")
        assert result["pois"][0]["name"] == "海底捞"
        req_url = responses_lib.calls[0].request.url
        assert "location=106.504962" in req_url
        assert "radius=5000" in req_url
        assert "sortrule=distance" in req_url

    @responses_lib.activate
    def test_around_search_with_options(self):
        responses_lib.get(
            "https://restapi.amap.com/v5/place/around",
            json=V5_POI_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        client.poi.around_search(
            "106.5,29.5",
            keywords="餐饮",
            types="050000",
            radius=1000,
            sortrule="weight",
            show_fields="business,photos",
            page_size=5,
            page_num=3,
        )
        req_url = responses_lib.calls[0].request.url
        assert "keywords=" in req_url
        assert "types=050000" in req_url
        assert "radius=1000" in req_url
        assert "sortrule=weight" in req_url
        assert "show_fields=business" in req_url


class TestPolygonSearch:
    """Test POI polygon search."""

    @responses_lib.activate
    def test_polygon_search_basic(self):
        responses_lib.get(
            "https://restapi.amap.com/v5/place/polygon",
            json=V5_POI_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        polygon = "106.5,29.5|106.6,29.5|106.6,29.6|106.5,29.6"
        result = client.poi.polygon_search(polygon)
        assert result["status"] == "1"
        req_url = responses_lib.calls[0].request.url
        assert "polygon=" in req_url

    @responses_lib.activate
    def test_polygon_search_with_options(self):
        responses_lib.get(
            "https://restapi.amap.com/v5/place/polygon",
            json=V5_POI_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        client.poi.polygon_search(
            "106.5,29.5|106.6,29.6",
            keywords="火锅",
            types="050000",
            show_fields="children",
            page_size=15,
            page_num=2,
        )
        req_url = responses_lib.calls[0].request.url
        assert "keywords=" in req_url
        assert "types=050000" in req_url
        assert "show_fields=children" in req_url
        assert "page_size=15" in req_url


class TestDetail:
    """Test POI detail lookup."""

    @responses_lib.activate
    def test_detail_single_id(self):
        responses_lib.get(
            "https://restapi.amap.com/v5/place/detail",
            json=V5_POI_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        result = client.poi.detail("B000A8UIN8")
        assert result["pois"][0]["id"] == "B000A8UIN8"
        req_url = responses_lib.calls[0].request.url
        assert "id=B000A8UIN8" in req_url

    @responses_lib.activate
    def test_detail_multiple_ids(self):
        responses_lib.get(
            "https://restapi.amap.com/v5/place/detail",
            json=V5_POI_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        client.poi.detail("B000A8UIN8|B000A8UIN9", show_fields="business,navi")
        req_url = responses_lib.calls[0].request.url
        assert "show_fields=business" in req_url
