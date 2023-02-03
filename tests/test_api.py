import pytest
import requests

from coinbase.api import CoinbaseAPI, BrokerageAPI


class TestCoinbaseAPI:
    def test_type(self, coinbase_api: CoinbaseAPI):
        assert isinstance(coinbase_api, CoinbaseAPI)

    def test_attributes(self, coinbase_api: CoinbaseAPI):
        assert hasattr(coinbase_api, "settings")
        assert hasattr(coinbase_api, "key")
        assert hasattr(coinbase_api, "secret")
        assert hasattr(coinbase_api, "rest")

    def test_properties(self, coinbase_api: CoinbaseAPI):
        assert isinstance(coinbase_api.settings, dict)
        assert isinstance(coinbase_api.key, str)
        assert isinstance(coinbase_api.secret, str)
        assert isinstance(coinbase_api.rest, str)

    def test_version(self, coinbase_api: CoinbaseAPI):
        assert 2 == coinbase_api.version

    def test_path(self, coinbase_api: CoinbaseAPI):
        assert callable(coinbase_api.path)
        assert "/v2/time" == coinbase_api.path("/time")

    def test_url(self, coinbase_api: CoinbaseAPI):
        assert callable(coinbase_api.url)

        assert "https://api.coinbase.com/v2/time" == coinbase_api.url("/time")

        response = requests.get(coinbase_api.url("/time"), timeout=30)
        assert 200 == response.status_code

        payload = response.json()
        assert "data" in payload

        assert "iso" in payload["data"] and "epoch" in payload["data"]


class TestBrokerageAPI(TestCoinbaseAPI):
    def test_type(self, brokerage_api: BrokerageAPI):
        assert isinstance(brokerage_api, BrokerageAPI)

    def test_version(self, brokerage_api: BrokerageAPI):
        assert 3 == brokerage_api.version

    def test_path(self, brokerage_api: BrokerageAPI):
        endpoint: str = "/api/v3/brokerage/products/BTC-USD"

        assert callable(brokerage_api.path)
        assert endpoint == brokerage_api.path("/products/BTC-USD")

    # NOTE: Brokerage endpoints require authentication
    @pytest.mark.private
    def test_url(self, brokerage_api: BrokerageAPI):
        url: str = "https://api.coinbase.com/api/v3/brokerage/products/BTC-USD"

        assert callable(brokerage_api.url)
        assert url == brokerage_api.url("/products/BTC-USD")

        # NOTE: Fix this to include authy
        # authentication_error	401	Invalid auth (generic)
        # source: https://docs.cloud.coinbase.com/sign-in-with-coinbase/docs/error-response
        response = requests.get(url, timeout=30)
        assert 200 == response.status_code

        payload = response.json()
        assert "product_id" in payload and "price" in payload
