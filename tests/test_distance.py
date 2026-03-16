"""Tests for DistanceAPI."""

import responses as responses_lib

from amap.client import AmapClient

DISTANCE_RESPONSE = {
    "status": "1",
    "info": "OK",
    "results": [
        {"origin_id": "1", "dest_id": "1", "distance": "12345", "duration": "600"}
    ],
}


class TestDistance:
    """Test distance measurement."""

    @responses_lib.activate
    def test_measure_driving(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/distance",
            json=DISTANCE_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        result = client.distance.measure(
            origins="106.504962,29.533155",
            destination="106.510000,29.540000",
        )
        assert result["results"][0]["distance"] == "12345"
        req_url = responses_lib.calls[0].request.url
        assert "origins=106.504962" in req_url
        assert "destination=106.510000" in req_url
        assert "type=1" in req_url

    @responses_lib.activate
    def test_measure_straight_line(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/distance",
            json=DISTANCE_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        client.distance.measure(
            origins="106.5,29.5",
            destination="106.6,29.6",
            type=0,
        )
        req_url = responses_lib.calls[0].request.url
        assert "type=0" in req_url

    @responses_lib.activate
    def test_measure_walking(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/distance",
            json=DISTANCE_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        client.distance.measure(
            origins="106.5,29.5",
            destination="106.6,29.6",
            type=3,
        )
        req_url = responses_lib.calls[0].request.url
        assert "type=3" in req_url

    @responses_lib.activate
    def test_measure_multiple_origins(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/distance",
            json=DISTANCE_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        client.distance.measure(
            origins="106.5,29.5|106.6,29.6|106.7,29.7",
            destination="106.8,29.8",
        )
        req_url = responses_lib.calls[0].request.url
        assert "origins=106.5" in req_url
