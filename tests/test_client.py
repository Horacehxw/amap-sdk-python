"""Tests for AmapClient core functionality."""

import os
from unittest.mock import patch

import pytest
import responses as responses_lib

from amap.client import AmapClient
from amap.exceptions import AmapAPIError, AmapNetworkError


class TestAmapClientInit:
    """Test client initialization and API key handling."""

    def test_explicit_key(self):
        client = AmapClient(api_key="test_fake_key")
        assert client.api_key == "test_fake_key"

    def test_env_key(self, monkeypatch):
        monkeypatch.setenv("AMAP_MAPS_API_KEY", "env_fake_key")
        client = AmapClient()
        assert client.api_key == "env_fake_key"

    def test_no_key_raises(self, monkeypatch):
        monkeypatch.delenv("AMAP_MAPS_API_KEY", raising=False)
        with pytest.raises(ValueError, match="API key"):
            AmapClient()


class TestAmapClientRequest:
    """Test _request method with HTTP mocking."""

    @responses_lib.activate
    def test_v3_success(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/geocode/geo",
            json={"status": "1", "info": "OK", "geocodes": [{"city": "北京"}]},
        )
        client = AmapClient(api_key="test_fake_key")
        result = client._request("/v3/geocode/geo", params={"address": "北京"})
        assert result["geocodes"][0]["city"] == "北京"
        # Verify key was injected
        assert "key=test_fake_key" in responses_lib.calls[0].request.url

    @responses_lib.activate
    def test_v3_business_error(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/geocode/geo",
            json={"status": "0", "info": "INVALID_USER_KEY", "infocode": "10001"},
        )
        client = AmapClient(api_key="test_fake_key")
        with pytest.raises(AmapAPIError, match="10001"):
            client._request("/v3/geocode/geo", params={"address": "北京"})

    @responses_lib.activate
    def test_v4_success(self):
        responses_lib.get(
            "https://restapi.amap.com/v4/search",
            json={"errcode": 0, "errmsg": "OK", "data": {"pois": []}},
        )
        client = AmapClient(api_key="test_fake_key")
        result = client._request(
            "/v4/search", params={"query": "test"}, api_version="v4"
        )
        assert result["data"]["pois"] == []

    @patch("amap.client.time.sleep")
    @responses_lib.activate
    def test_retry_on_5xx(self, mock_sleep):
        responses_lib.get(
            "https://restapi.amap.com/v3/geocode/geo",
            body="Service Unavailable",
            status=503,
        )
        responses_lib.get(
            "https://restapi.amap.com/v3/geocode/geo",
            body="Service Unavailable",
            status=503,
        )
        responses_lib.get(
            "https://restapi.amap.com/v3/geocode/geo",
            json={"status": "1", "info": "OK", "geocodes": []},
        )
        client = AmapClient(api_key="test_fake_key")
        result = client._request("/v3/geocode/geo", params={"address": "test"})
        assert result["status"] == "1"
        assert len(responses_lib.calls) == 3

    @patch("amap.client.time.sleep")
    @responses_lib.activate
    def test_max_retries_exceeded(self, mock_sleep):
        for _ in range(4):
            responses_lib.get(
                "https://restapi.amap.com/v3/geocode/geo",
                body="Service Unavailable",
                status=503,
            )
        client = AmapClient(api_key="test_fake_key")
        with pytest.raises(AmapNetworkError):
            client._request("/v3/geocode/geo", params={"address": "test"})
        assert len(responses_lib.calls) == 4
