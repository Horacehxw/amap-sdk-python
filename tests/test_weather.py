"""Tests for WeatherAPI."""

import responses as responses_lib

from amap.client import AmapClient


class TestWeather:
    """Test weather queries."""

    @responses_lib.activate
    def test_weather_base(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/weather/weatherInfo",
            json={
                "status": "1",
                "info": "OK",
                "lives": [
                    {
                        "province": "重庆",
                        "city": "重庆市",
                        "weather": "晴",
                        "temperature": "22",
                    }
                ],
            },
        )
        client = AmapClient(api_key="test_fake_key")
        result = client.weather.weather("500000")
        assert result["lives"][0]["city"] == "重庆市"
        req_url = responses_lib.calls[0].request.url
        assert "city=500000" in req_url
        assert "extensions=base" in req_url

    @responses_lib.activate
    def test_weather_forecast(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/weather/weatherInfo",
            json={
                "status": "1",
                "info": "OK",
                "forecasts": [
                    {
                        "province": "重庆",
                        "city": "重庆市",
                        "casts": [{"date": "2026-03-17", "dayweather": "多云"}],
                    }
                ],
            },
        )
        client = AmapClient(api_key="test_fake_key")
        result = client.weather.weather("500000", extensions="all")
        assert "forecasts" in result
        req_url = responses_lib.calls[0].request.url
        assert "extensions=all" in req_url

    @responses_lib.activate
    def test_weather_default_extensions(self):
        responses_lib.get(
            "https://restapi.amap.com/v3/weather/weatherInfo",
            json={"status": "1", "info": "OK", "lives": []},
        )
        client = AmapClient(api_key="test_fake_key")
        client.weather.weather("110000")
        req_url = responses_lib.calls[0].request.url
        assert "extensions=base" in req_url
