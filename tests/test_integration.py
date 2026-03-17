"""Integration tests that hit the real Amap API.

Run with: AMAP_MAPS_KEY=<key> pytest tests/test_integration.py -v -m integration
"""

import pytest

from amap.client import AmapClient

pytestmark = pytest.mark.integration


@pytest.fixture
def client():
    return AmapClient()  # reads AMAP_MAPS_KEY from env


def test_geocode_chongqing(client):
    result = client.geocoding.geocode("重庆市观音桥")
    assert result["geocodes"]
    loc = result["geocodes"][0]["location"]
    assert "106" in loc  # Chongqing longitude ~106


def test_poi_around_restaurants(client):
    result = client.poi.around_search(
        location="106.574,29.572", keywords="米粉", radius=500, show_fields="business"
    )
    assert int(result["count"]) > 0


def test_weather_chongqing(client):
    result = client.weather.weather(city="500000")
    assert result["lives"]


def test_distance_two_points(client):
    result = client.distance.measure(
        origins="106.574,29.572", destination="106.580,29.580"
    )
    assert result["results"]
