import json
import os
import pytest

from coinbase.api import API
from coinbase.api import AdvancedAPI
from coinbase.api import WebSocketAPI

from coinbase.auth import Auth

from coinbase.messenger import Messenger
from coinbase.messenger import AdvancedMessenger


def pytest_addoption(parser):
    parser.addoption(
        "--private",
        action="store_true",
        default=False,
        help="test private endpoints",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "private: test private endpoints")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--private"):
        # --no-skip given: do not skip tests
        return
    private = pytest.mark.skip(reason="need --private option to run")
    for item in items:
        if "private" in item.keywords:
            item.add_marker(private)


@pytest.fixture(scope="module")
def api() -> API:
    return API()


@pytest.fixture(scope="module")
def advanced_api() -> AdvancedAPI:
    return AdvancedAPI()


@pytest.fixture(scope="module")
def websocket_api() -> WebSocketAPI:
    return WebSocketAPI()


@pytest.fixture(scope="module")
def auth(api: API) -> Auth:
    return Auth(api)


@pytest.fixture(scope="module")
def advanced_auth(advanced_api: AdvancedAPI) -> Auth:
    return Auth(advanced_api)


@pytest.fixture(scope="module")
def messenger(auth: Auth) -> Messenger:
    return Messenger(auth)


@pytest.fixture(scope="module")
def advanced_messenger(advanced_auth: Auth) -> AdvancedMessenger:
    return AdvancedMessenger(advanced_auth)


# @pytest.fixture(scope="module")
# def wss(settings: dict) -> WSS:
#     return WSS(settings["api"])


# @pytest.fixture(scope="module")
# def token(wss: WSS) -> Token:
#     return Token(wss)

# @pytest.fixture(scope="module")
# def public_client(public_messenger: Messenger) -> CoinbasePro:
#     return CoinbasePro(public_messenger)


# @pytest.fixture(scope="module")
# def private_client(private_messenger: Messenger) -> CoinbasePro:
#     return CoinbasePro(private_messenger)


# @pytest.fixture(scope="module")
# def public_stream() -> Stream:
#     return Stream()


# @pytest.fixture(scope="module")
# def private_stream(token: Token) -> Stream:
#     return Stream(token)


# @pytest.fixture(scope="module")
# def account_id(private_client: CoinbasePro) -> str:
#     accounts = private_client.account.list()
#     account = [a for a in accounts if a["currency"] == "BTC"]
#     return account[0]["id"]


# @pytest.fixture(scope="module")
# def conversion_id(private_client: CoinbasePro) -> str:
#     data = {"from": "USD", "to": "USDC", "amount": 10.0}
#     conversion = private_client.convert.post(data)
#     return conversion["id"]
