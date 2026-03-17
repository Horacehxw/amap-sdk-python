# amap-sdk-python

[![PyPI version](https://img.shields.io/pypi/v/amap-sdk.svg)](https://pypi.org/project/amap-sdk/)
[![Python](https://img.shields.io/pypi/pyversions/amap-sdk.svg)](https://pypi.org/project/amap-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/Horacehxw/amap-sdk-python/actions/workflows/tests.yml/badge.svg)](https://github.com/Horacehxw/amap-sdk-python/actions/workflows/tests.yml)

Python SDK for the [Amap (高德地图)](https://lbs.amap.com/) Web Service REST API.

> **Disclaimer:** This is an unofficial, community-maintained SDK. 高德地图 is a trademark of AutoNavi Software Co., Ltd. (Alibaba Group). This project is not affiliated with or endorsed by Amap/AutoNavi.

## Features

- 10 API modules covering geocoding, POI search, routing, weather, and more
- POI search uses the latest v5 API
- Type-annotated, minimal dependencies (`requests` only)
- Comprehensive test suite (68 unit + 4 integration tests)

## Installation

```bash
pip install amap-sdk
```

For development:

```bash
git clone https://github.com/Horacehxw/amap-sdk-python.git
cd amap-sdk-python
pip install -e ".[dev]"
```

## Quick Start

```python
from amap import AmapClient

# Via environment variable AMAP_MAPS_KEY, or pass directly:
client = AmapClient(api_key="your_api_key")

# Geocoding
result = client.geocoding.geocode("北京市朝阳区阜通东大街6号")

# POI search (v5)
pois = client.poi.text_search("火锅", city="重庆")

# Weather
weather = client.weather.get_weather("110101")  # adcode for 东城区

# Routing
route = client.direction.driving("116.481028,39.989643", "116.465302,40.004717")

# Static map (returns PNG bytes)
img = client.staticmap.get_map(location="116.481028,39.989643", zoom=15)
```

Get your API key from the [Amap Developer Portal](https://console.amap.com/).

## API Modules

| Module | Attribute | Description |
|--------|-----------|-------------|
| Geocoding | `client.geocoding` | Address ↔ coordinate conversion |
| POI (v5) | `client.poi` | Place search: text, nearby, polygon, detail |
| Weather | `client.weather` | Current weather and forecasts |
| District | `client.district` | Administrative region queries |
| Input Tips | `client.inputtips` | Search autocomplete suggestions |
| Distance | `client.distance` | Distance measurement between points |
| Direction | `client.direction` | Walk, drive, transit, bicycle routing |
| Static Map | `client.staticmap` | Static map image generation (PNG) |
| Coordinate | `client.coordinate` | Coordinate system conversion (GPS/Baidu → GCJ-02) |
| Traffic | `client.traffic` | Real-time traffic status (road, circle, rectangle) |

## Testing

```bash
# Unit tests (no API key needed)
pytest -v

# Skip integration tests
pytest -v -m "not integration"

# Integration tests (requires real API key)
AMAP_MAPS_KEY=your_key pytest -v -m integration
```

## License

[MIT](LICENSE)

---

## 中文说明

高德地图 Web Service REST API 的 Python SDK，覆盖地理编码、POI 搜索、路线规划、天气查询等 10 个模块。

**安装：**
```bash
pip install amap-sdk
```

**特性：**
- POI 搜索使用最新 v5 API
- 完整类型注解，仅依赖 `requests`
- 72 个测试（68 单元 + 4 集成），无需 API Key 即可运行单元测试
- 支持坐标系转换（GPS/百度 → GCJ-02）

**使用前需要：** 在[高德开放平台](https://console.amap.com/)注册并获取 API Key。
