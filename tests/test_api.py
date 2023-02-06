import pytest
import requests

from coinbase.api import get_api_settings, API, AdvancedAPI, WebSocketAPI


def test_get_api_settings():
    api_settings = get_api_settings()

    assert isinstance(api_settings, dict)
    assert all(key in api_settings for key in ("key", "secret", "rest", "feed"))

    for key in api_settings.keys():
        assert isinstance(api_settings[key], str)

    assert all(api_settings.values())


class TestAPI:
    def test_type(self, api: API):
        assert isinstance(api, API)

    def test_attributes(self, api: API):
        attributes = ["settings", "key", "secret", "rest", "version"]
        for attribute in attributes:
            assert hasattr(api, attribute)

    def test_properties(self, api: API):
        assert isinstance(api.settings, dict)
        assert isinstance(api.key, str)
        assert isinstance(api.secret, str)
        assert isinstance(api.rest, str)

    def test_rest(self, api: API):
        assert "https://api.coinbase.com" == api.rest

    def test_version(self, api: API):
        assert 2 == api.version

    def test_path(self, api: API):
        assert callable(api.path)
        assert "/v2/time" == api.path("/time")


class TestAdvancedAPI(TestAPI):
    def test_type(self, advanced_api: AdvancedAPI):
        assert isinstance(advanced_api, AdvancedAPI)

    def test_version(self, advanced_api: AdvancedAPI):
        assert 3 == advanced_api.version

    def test_path(self, advanced_api: AdvancedAPI):
        endpoint: str = "/api/v3/brokerage/products/BTC-USD"

        assert callable(advanced_api.path)
        assert endpoint == advanced_api.path("/products/BTC-USD")


class TestWebSocketAPI(TestAdvancedAPI):
    def test_feed(self, websocket_api: WebSocketAPI):
        assert "wss://advanced-trade-ws.coinbase.com" == websocket_api.feed
