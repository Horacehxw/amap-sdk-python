"""Tests for DirectionAPI."""

import responses as responses_lib

from amap.client import AmapClient

WALKING_RESPONSE = {
    "status": "1",
    "info": "OK",
    "route": {"origin": "106.5,29.5", "destination": "106.6,29.6", "paths": []},
}

DRIVING_RESPONSE = {
    "status": "1",
    "info": "OK",
    "route": {"origin": "106.5,29.5", "destination": "106.6,29.6", "paths": []},
}

TRANSIT_RESPONSE = {
    "status": "1",
    "info": "OK",
    "route": {"origin": "106.5,29.5", "destination": "106.6,29.6", "transits": []},
}

BICYCLING_RESPONSE = {
    "errcode": 0,
    "errmsg": "OK",
    "data": {"origin": "106.5,29.5", "destination": "106.6,29.6", "paths": []},
}


class TestWalking:
    """Test walking direction."""

    @responses_lib.activate
    def test_walking_basic(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/direction/walking",
            json=WALKING_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        result = client.direction.walking("106.5,29.5", "106.6,29.6")
        assert result["status"] == "1"
        assert "route" in result
        req_url = responses_lib.calls[0].request.url
        assert "origin=106.5" in req_url
        assert "destination=106.6" in req_url


class TestDriving:
    """Test driving direction."""

    @responses_lib.activate
    def test_driving_basic(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/direction/driving",
            json=DRIVING_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        result = client.direction.driving("106.5,29.5", "106.6,29.6")
        assert result["status"] == "1"
        req_url = responses_lib.calls[0].request.url
        assert "origin=106.5" in req_url
        assert "extensions=base" in req_url

    @responses_lib.activate
    def test_driving_with_strategy(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/direction/driving",
            json=DRIVING_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        client.direction.driving("106.5,29.5", "106.6,29.6", strategy=13)
        req_url = responses_lib.calls[0].request.url
        assert "strategy=13" in req_url

    @responses_lib.activate
    def test_driving_no_strategy_omits_param(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/direction/driving",
            json=DRIVING_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        client.direction.driving("106.5,29.5", "106.6,29.6")
        req_url = responses_lib.calls[0].request.url
        assert "strategy=" not in req_url

    @responses_lib.activate
    def test_driving_with_waypoints(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/direction/driving",
            json=DRIVING_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        client.direction.driving(
            "106.5,29.5",
            "106.6,29.6",
            waypoints="106.55,29.55|106.58,29.58",
        )
        req_url = responses_lib.calls[0].request.url
        assert "waypoints=106.55" in req_url

    @responses_lib.activate
    def test_driving_with_extensions_all(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/direction/driving",
            json=DRIVING_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        client.direction.driving("106.5,29.5", "106.6,29.6", extensions="all")
        req_url = responses_lib.calls[0].request.url
        assert "extensions=all" in req_url


class TestTransit:
    """Test transit direction."""

    @responses_lib.activate
    def test_transit_basic(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/direction/transit/integrated",
            json=TRANSIT_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        result = client.direction.transit("106.5,29.5", "106.6,29.6", city="重庆")
        assert result["status"] == "1"
        req_url = responses_lib.calls[0].request.url
        assert "city=" in req_url
        assert "strategy=0" in req_url

    @responses_lib.activate
    def test_transit_requires_city(self):
        """City is a required parameter — verify it's always sent."""
        responses_lib.get(
            "https://restapi.amap.com/v3/direction/transit/integrated",
            json=TRANSIT_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        client.direction.transit("106.5,29.5", "106.6,29.6", city="500000")
        req_url = responses_lib.calls[0].request.url
        assert "city=500000" in req_url

    @responses_lib.activate
    def test_transit_cross_city(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/direction/transit/integrated",
            json=TRANSIT_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        client.direction.transit(
            "106.5,29.5", "104.0,30.6", city="重庆", cityd="成都"
        )
        req_url = responses_lib.calls[0].request.url
        assert "cityd=" in req_url


class TestBicycling:
    """Test bicycling direction (v4 API)."""

    @responses_lib.activate
    def test_bicycling_basic(self):
        responses_lib.get(
            "https://restapi.amap.com/v4/direction/bicycling",
            json=BICYCLING_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        result = client.direction.bicycling("106.5,29.5", "106.6,29.6")
        assert result["errcode"] == 0
        assert "data" in result

    @responses_lib.activate
    def test_bicycling_uses_v4_endpoint(self):
        """Verify bicycling hits the v4 URL, not v3."""
        responses_lib.get(
            "https://restapi.amap.com/v4/direction/bicycling",
            json=BICYCLING_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        client.direction.bicycling("106.5,29.5", "106.6,29.6")
        req_url = responses_lib.calls[0].request.url
        assert "/v4/direction/bicycling" in req_url

    @responses_lib.activate
    def test_bicycling_v4_error_checking(self):
        """Verify v4 error checking: errcode != 0 should raise AmapAPIError."""
        responses_lib.get(
            "https://restapi.amap.com/v4/direction/bicycling",
            json={"errcode": 10001, "errmsg": "invalid key"},
        )
        client = AmapClient(api_key="test_fake_key")
        import pytest

        from amap.exceptions import AmapAPIError

        with pytest.raises(AmapAPIError):
            client.direction.bicycling("106.5,29.5", "106.6,29.6")
