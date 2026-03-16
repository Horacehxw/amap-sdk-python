"""Tests for TrafficAPI."""

import responses as responses_lib

from amap.client import AmapClient

ROAD_RESPONSE = {
    "status": "1",
    "info": "OK",
    "trafficinfo": {
        "description": "畅通",
        "evaluation": {"expedite": "1", "congested": "0"},
    },
}

CIRCLE_RESPONSE = {
    "status": "1",
    "info": "OK",
    "trafficinfo": {
        "description": "畅通",
        "evaluation": {"expedite": "1"},
    },
}

RECTANGLE_RESPONSE = {
    "status": "1",
    "info": "OK",
    "trafficinfo": {
        "description": "畅通",
    },
}


class TestRoad:
    """Test road traffic status."""

    @responses_lib.activate
    def test_road_basic(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/traffic/status/road",
            json=ROAD_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        result = client.traffic.road(name="长江路", city="重庆")
        assert result["status"] == "1"
        assert "trafficinfo" in result
        req_url = responses_lib.calls[0].request.url
        assert "name=" in req_url
        assert "city=" in req_url
        assert "extensions=base" in req_url

    @responses_lib.activate
    def test_road_with_level(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/traffic/status/road",
            json=ROAD_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        client.traffic.road(name="长江路", city="重庆", level=5)
        req_url = responses_lib.calls[0].request.url
        assert "level=5" in req_url

    @responses_lib.activate
    def test_road_no_level_omits_param(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/traffic/status/road",
            json=ROAD_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        client.traffic.road(name="长江路", city="重庆")
        req_url = responses_lib.calls[0].request.url
        assert "level=" not in req_url


class TestCircle:
    """Test circle traffic status."""

    @responses_lib.activate
    def test_circle_basic(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/traffic/status/circle",
            json=CIRCLE_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        result = client.traffic.circle(location="106.5,29.5")
        assert result["status"] == "1"
        req_url = responses_lib.calls[0].request.url
        assert "location=106.5" in req_url
        assert "radius=1000" in req_url
        assert "extensions=base" in req_url

    @responses_lib.activate
    def test_circle_custom_radius(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/traffic/status/circle",
            json=CIRCLE_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        client.traffic.circle(location="106.5,29.5", radius=500)
        req_url = responses_lib.calls[0].request.url
        assert "radius=500" in req_url

    @responses_lib.activate
    def test_circle_with_level_and_extensions(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/traffic/status/circle",
            json=CIRCLE_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        client.traffic.circle(
            location="106.5,29.5", level=6, extensions="all"
        )
        req_url = responses_lib.calls[0].request.url
        assert "level=6" in req_url
        assert "extensions=all" in req_url


class TestRectangle:
    """Test rectangle traffic status."""

    @responses_lib.activate
    def test_rectangle_basic(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/traffic/status/rectangle",
            json=RECTANGLE_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        result = client.traffic.rectangle(rectangle="106.5,29.5;106.6,29.6")
        assert result["status"] == "1"
        req_url = responses_lib.calls[0].request.url
        assert "rectangle=106.5" in req_url
        assert "extensions=base" in req_url

    @responses_lib.activate
    def test_rectangle_with_level(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/traffic/status/rectangle",
            json=RECTANGLE_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        client.traffic.rectangle(
            rectangle="106.5,29.5;106.6,29.6", level=4
        )
        req_url = responses_lib.calls[0].request.url
        assert "level=4" in req_url

    @responses_lib.activate
    def test_rectangle_no_level_omits_param(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/traffic/status/rectangle",
            json=RECTANGLE_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        client.traffic.rectangle(rectangle="106.5,29.5;106.6,29.6")
        req_url = responses_lib.calls[0].request.url
        assert "level=" not in req_url
