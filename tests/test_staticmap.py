"""Tests for StaticMapAPI."""

import responses as responses_lib

from amap.client import AmapClient

# A minimal fake PNG (8 bytes: PNG magic header)
FAKE_PNG = b"\x89PNG\r\n\x1a\n"


class TestStaticMap:
    """Test static map image generation."""

    @responses_lib.activate
    def test_generate_basic(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/staticmap",
            body=FAKE_PNG,
            content_type="image/png",
        )
        client = AmapClient(api_key="test_fake_key")
        result = client.staticmap.generate(location="106.5,29.5", zoom=10)
        assert isinstance(result, bytes)
        assert result == FAKE_PNG
        req_url = responses_lib.calls[0].request.url
        assert "location=106.5" in req_url
        assert "zoom=10" in req_url
        assert "size=400" in req_url
        assert "scale=1" in req_url
        assert "traffic=0" in req_url

    @responses_lib.activate
    def test_generate_with_markers(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/staticmap",
            body=FAKE_PNG,
            content_type="image/png",
        )
        client = AmapClient(api_key="test_fake_key")
        client.staticmap.generate(
            location="106.5,29.5",
            zoom=15,
            markers="mid,,A:106.5,29.5",
        )
        req_url = responses_lib.calls[0].request.url
        assert "markers=" in req_url

    @responses_lib.activate
    def test_generate_with_labels(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/staticmap",
            body=FAKE_PNG,
            content_type="image/png",
        )
        client = AmapClient(api_key="test_fake_key")
        client.staticmap.generate(
            location="106.5,29.5",
            zoom=15,
            labels="测试,2,0,16,0xFFFFFF,0x008000:106.5,29.5",
        )
        req_url = responses_lib.calls[0].request.url
        assert "labels=" in req_url

    @responses_lib.activate
    def test_generate_with_paths(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/staticmap",
            body=FAKE_PNG,
            content_type="image/png",
        )
        client = AmapClient(api_key="test_fake_key")
        client.staticmap.generate(
            location="106.5,29.5",
            zoom=15,
            paths="10,0x0000ff,1,,,:106.5,29.5;106.6,29.6",
        )
        req_url = responses_lib.calls[0].request.url
        assert "paths=" in req_url

    @responses_lib.activate
    def test_generate_no_markers_omits_param(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/staticmap",
            body=FAKE_PNG,
            content_type="image/png",
        )
        client = AmapClient(api_key="test_fake_key")
        client.staticmap.generate(location="106.5,29.5", zoom=10)
        req_url = responses_lib.calls[0].request.url
        assert "markers=" not in req_url
        assert "labels=" not in req_url
        assert "paths=" not in req_url

    @responses_lib.activate
    def test_generate_custom_size_and_scale(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/staticmap",
            body=FAKE_PNG,
            content_type="image/png",
        )
        client = AmapClient(api_key="test_fake_key")
        client.staticmap.generate(
            location="106.5,29.5", zoom=10, size="800*600", scale=2, traffic=1
        )
        req_url = responses_lib.calls[0].request.url
        assert "size=800" in req_url
        assert "scale=2" in req_url
        assert "traffic=1" in req_url
