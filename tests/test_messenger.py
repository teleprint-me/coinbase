import pytest

from requests import Response
from requests import Session

from tests.teardown import Teardown

from coinbase.messenger import API
from coinbase.messenger import Auth
from coinbase.messenger import Messenger
from coinbase.messenger import AdvancedMessenger
from coinbase.messenger import Subscriber


class TestMessenger(Teardown):
    def test_type(self, messenger: Messenger):
        assert isinstance(messenger, Messenger)

    def test_attributes(self, messenger: Messenger):
        attributes: list[str] = ["auth", "api", "session", "timeout"]
        for attribute in attributes:
            assert hasattr(messenger, attribute)

    def test_properties(self, messenger: Messenger):
        assert isinstance(messenger.api, API)
        assert isinstance(messenger.auth, Auth)
        assert isinstance(messenger.session, Session)
        assert isinstance(messenger.timeout, int)

    def test_methods(self, messenger: Messenger):
        methods: list[object] = [
            messenger.get,
            messenger.post,
            messenger.put,
            messenger.delete,
            messenger.page,
        ]
        for method in methods:
            assert callable(method)

    def test_get(self, messenger: Messenger):
        response: Response = messenger.get("/time")
        assert isinstance(response, Response)
        assert response.status_code == 200

        payload: dict = response.json()
        assert isinstance(payload, dict)
        assert "data" in payload
        assert "iso" in payload["data"] and "epoch" in payload["data"]

    @pytest.mark.private
    def test_page(self, messenger: Messenger):
        responses: list[Response] = messenger.page("/accounts")
        assert isinstance(responses, list)

        if not responses:
            return

        assert all(
            isinstance(response, Response) and response.status_code == 200
            for response in responses
        )

        pages = [response.json() for response in responses]
        assert all(
            isinstance(page, dict) for page in pages
        ), "all pages should be dictionaries"

        page = pages[0]
        assert all(
            key in page for key in ("pagination",)
        ), "page must have a pagination key"

        pagination = page["pagination"]
        assert all(
            key in pagination for key in ("next_uri", "next_starting_after")
        ), "pagination keys not present"

        accounts = page["data"]
        assert isinstance(accounts, list), "accounts should be a list"

        account = accounts[0]
        assert all(
            key in account for key in ("id", "currency")
        ), "id and currency keys not present in account"


class TestAdvancedMessenger(TestMessenger):
    @pytest.mark.private
    def test_get(self, advanced_messenger: AdvancedMessenger):
        response: Response = advanced_messenger.get("/products/BTC-USD")

        assert isinstance(response, Response)
        assert response.status_code == 200

        payload: dict = response.json()
        assert isinstance(payload, dict)
        assert "product_id" in payload and "price" in payload

    @pytest.mark.private
    def test_page(self, advanced_messenger: AdvancedMessenger):
        responses = advanced_messenger.page("/accounts")
        assert isinstance(responses, list)

        if not responses:
            return

        assert all(
            isinstance(response, Response) and response.status_code == 200
            for response in responses
        )

        pages = [response.json() for response in responses]
        assert isinstance(pages, list) and isinstance(pages[0], dict)

        page = pages[0]
        assert isinstance(page, dict) and all(
            key in page for key in ("has_next", "cursor", "accounts")
        )

        accounts = page["accounts"]
        assert isinstance(accounts, list)

        account = accounts[0]
        assert all(key in account for key in ("uuid", "currency"))


def test_subscriber(messenger):
    class Dummy(Subscriber):
        pass

    dummy = Dummy(messenger)

    assert isinstance(dummy, Subscriber)
    assert isinstance(dummy, Dummy)
    assert isinstance(dummy.messenger, Messenger)

    assert hasattr(dummy, "messenger")
    assert hasattr(dummy, "error")

    assert callable(dummy.error)
