import pytest
import requests

from requests.auth import AuthBase

from coinbase.api import API
from coinbase.api import AdvancedAPI
from coinbase.api import WebSocketAPI

from coinbase.auth import Auth


class TestAuth:
    def test_type(self, auth: Auth):
        assert isinstance(auth, AuthBase)
        assert isinstance(auth, Auth)

    def test_attr(self, auth: Auth):
        assert hasattr(auth, "_Auth__api")
        assert hasattr(auth, "api")
        assert hasattr(auth, "signature")
        assert hasattr(auth, "header")

    def test_properties(self, auth: Auth):
        assert isinstance(auth.api.key, str)
        assert isinstance(auth.api.secret, str)

    def test_callable(self, auth: Auth):
        assert callable(auth)
        assert callable(auth.signature)
        assert callable(auth.header)

    @pytest.mark.private
    def test_auth(self, api: API, auth: Auth):
        assert "https://api.coinbase.com/v2/accounts" == api.url("/accounts")

        response = requests.get(api.url("/accounts"), auth=auth, timeout=30)
        assert 200 == response.status_code

        payload = response.json()
        assert "pagination" in payload and "data" in payload

        page = payload["pagination"]
        assert "limit" in page and "next_uri" in page

        data = payload["data"]
        assert isinstance(data, list)
        assert "id" in data[0] and "currency" in data[0]


class TestAdvancedAuth:
    def test_type(self, advanced_auth: Auth):
        assert isinstance(advanced_auth, AuthBase)
        assert isinstance(advanced_auth, Auth)

    def test_attr(self, advanced_auth: Auth):
        assert hasattr(advanced_auth, "_Auth__api")
        assert hasattr(advanced_auth, "api")
        assert hasattr(advanced_auth, "signature")
        assert hasattr(advanced_auth, "header")

    def test_properties(self, advanced_auth: Auth):
        assert isinstance(advanced_auth.api.key, str)
        assert isinstance(advanced_auth.api.secret, str)

    def test_callable(self, advanced_auth: Auth):
        assert callable(advanced_auth)
        assert callable(advanced_auth.signature)
        assert callable(advanced_auth.header)

    @pytest.mark.private
    def test_auth(self, advanced_api: AdvancedAPI, advanced_auth: Auth):
        url: str = "https://api.coinbase.com/api/v3/brokerage/products/BTC-USD"

        assert callable(advanced_api.url)
        assert url == advanced_api.url("/products/BTC-USD")

        # NOTE: brokerage endpoints require auth
        # authentication_error	401	Invalid auth (generic)
        # source: https://docs.cloud.coinbase.com/sign-in-with-coinbase/docs/error-response
        response = requests.get(url, auth=advanced_auth, timeout=30)
        assert 200 == response.status_code

        payload = response.json()
        assert "product_id" in payload and "price" in payload
