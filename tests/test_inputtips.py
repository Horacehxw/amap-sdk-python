"""Tests for InputTipsAPI."""

import responses as responses_lib

from amap.client import AmapClient

TIPS_RESPONSE = {
    "status": "1",
    "info": "OK",
    "tips": [
        {"name": "重庆火锅", "id": "B000A8UIN8", "address": "解放碑"},
    ],
}


class TestInputTips:
    """Test autocomplete suggestions."""

    @responses_lib.activate
    def test_suggest_basic(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/assistant/inputtips",
            json=TIPS_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        result = client.inputtips.suggest("重庆火锅")
        assert result["tips"][0]["name"] == "重庆火锅"
        req_url = responses_lib.calls[0].request.url
        assert "keywords=" in req_url
        assert "datatype=all" in req_url

    @responses_lib.activate
    def test_suggest_with_all_options(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/assistant/inputtips",
            json=TIPS_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        client.inputtips.suggest(
            "火锅",
            type="050000",
            location="106.5,29.5",
            city="重庆",
            citylimit=True,
            datatype="poi",
        )
        req_url = responses_lib.calls[0].request.url
        assert "type=050000" in req_url
        assert "location=106.5" in req_url
        assert "city=" in req_url
        assert "citylimit=true" in req_url
        assert "datatype=poi" in req_url

    @responses_lib.activate
    def test_suggest_citylimit_default_false(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/assistant/inputtips",
            json=TIPS_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        client.inputtips.suggest("test")
        req_url = responses_lib.calls[0].request.url
        assert "citylimit=" not in req_url

    @responses_lib.activate
    def test_suggest_optional_params_omitted(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/assistant/inputtips",
            json=TIPS_RESPONSE,
        )
        client = AmapClient(api_key="test_fake_key")
        client.inputtips.suggest("test")
        req_url = responses_lib.calls[0].request.url
        assert "&type=" not in req_url and "?type=" not in req_url
        assert "location=" not in req_url
        assert "&city=" not in req_url and "?city=" not in req_url
