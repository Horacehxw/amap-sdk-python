import os

import pytest


def pytest_collection_modifyitems(config, items):
    if os.environ.get("AMAP_LIVE") == "1":
        return
    skip_live = pytest.mark.skip(reason="Amap live integration tests require AMAP_LIVE=1")
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip_live)
