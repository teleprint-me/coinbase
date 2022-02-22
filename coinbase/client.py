# teleprint-me/coinbase - A Python Wrapper for Coinbase
# Copyright (C) 2021 teleprint.me
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from coinbase.abstract import AbstractClient
from coinbase.messenger import API, Auth, Messenger, Subscriber


class User(Subscriber):
    def get(self) -> dict:
        return self.messenger.get("/user").json()

    def auth(self) -> dict:
        return self.messenger.get("/user/auth").json()

    def profile(self, user_id: str) -> dict:
        return self.messenger.get(f"/users/{user_id}").json()

    def update(self, data: dict) -> dict:
        return self.messenger.put("/user", data).json()


class Account(Subscriber):
    def list(self, data: dict = None) -> list:
        pages = self.messenger.page("/accounts", data)
        return [account for page in pages for account in page.json()["data"]]

    def get(self, account_id: str) -> dict:
        return self.messenger.get(f"/accounts/{account_id}").json()

    def update(self, account_id: str, data: dict) -> dict:
        return self.messenger.put(f"/accounts/{account_id}", data).json()

    def delete(self, account_id: str) -> dict:
        return self.messenger.delete(f"/accounts/{account_id}").json()


class Address(Subscriber):
    def list(self, account_id: str, data: dict = None) -> list:
        path = f"/accounts/{account_id}/addresses"
        pages = self.messenger.page(path, data)
        return [address for page in pages for address in page.json()["data"]]

    def get(self, account_id: str, address_id: str) -> dict:
        return self.messenger.get(f"/accounts/{account_id}/addresses/{address_id}")

    def transactions(self, account_id: str, address_id: str, data: dict = None) -> list:
        path = f"/accounts/{account_id}/addresses/{address_id}/transactions"
        pages = self.messenger.page(path, data)
        return [tx for page in pages for tx in page.json()["data"]]

    def create(self, account_id: str, data: dict) -> dict:
        return self.messenger.post(f"/accounts/{account_id}/addresses", data).json()


class Transaction(Subscriber):
    def list(self, account_id: str, data: dict = None) -> list:
        path = f"/accounts/{account_id}/transactions"
        pages = self.messenger.page(path, data)
        return [tx for page in pages for tx in page.json()["data"]]

    def get(self, account_id: str, transaction_id: str) -> dict:
        path = f"/accounts/{account_id}/transactions/{transaction_id}"
        return self.messenger.get(path).json()

    def send(self, account_id: str, data: dict) -> dict:
        path = f"/accounts/{account_id}/transactions"
        return self.messenger.post(path, data).json()

    def complete(self, account_id: str, transaction_id: str) -> dict:
        path = f"/accounts/{account_id}/transactions/{transaction_id}/complete"
        return self.messenger.post(path).json()

    def resend(self, account_id: str, transaction_id: str) -> dict:
        path = f"/accounts/{account_id}/transactions/{transaction_id}/resend"
        return self.messenger.post(path).json()

    def cancel(self, account_id: str, transaction_id: str) -> dict:
        path = f"/accounts/{account_id}/transactions/{transaction_id}"
        return self.messenger.delete(path).json()


class Buy(Subscriber):
    def list(self, account_id: str, data: dict = None) -> list:
        pages = self.messenger.page(f"/accounts/{account_id}/buys", data)
        return [buy for page in pages for buy in page.json()["data"]]

    def get(self, account_id: str, buy_id: str) -> dict:
        return self.messenger.get(f"/accounts/{account_id}/buys/{buy_id}").json()

    def order(self, account_id: str, data: dict) -> dict:
        return self.messenger.post(f"/accounts/{account_id}/buys", data).json()

    def commit(self, account_id: str, buy_id: str) -> dict:
        path = f"/accounts/{account_id}/buys/{buy_id}/commit"
        return self.messenger.post(path).json()


class Sell(Subscriber):
    def list(self, account_id: str, data: dict = None) -> list:
        pages = self.messenger.page(f"/accounts/{account_id}/sells", data)
        return [buy for page in pages for buy in page.json()["data"]]

    def get(self, account_id: str, sell_id: str) -> dict:
        return self.messenger.get(f"/accounts/{account_id}/sells/{sell_id}").json()

    def order(self, account_id: str, data: dict) -> dict:
        return self.messenger.post(f"/accounts/{account_id}/sells", data).json()

    def commit(self, account_id: str, sell_id: str) -> dict:
        path = f"/accounts/{account_id}/sells/{sell_id}/commit"
        return self.messenger.post(path).json()


class Time(Subscriber):
    def get(self) -> dict:
        # NOTE: The `epoch` field represents decimal seconds since Unix Epoch
        return self.messenger.get("/time").json()


class Coinbase(AbstractClient):
    def __init__(self, messenger: Messenger):
        self.messenger = messenger
        self.user = User(messenger)
        self.account = Account(messenger)
        self.address = Address(messenger)
        self.transaction = Transaction(messenger)
        self.buy = Buy(messenger)
        self.sell = Sell(messenger)
        self.time = Time(messenger)

    def __repr__(self) -> str:
        return f"Coinbase(name={self.name}, key={self.key})"

    def __str__(self) -> str:
        return self.name.capitalize()

    @property
    def key(self) -> str:
        return self.messenger.auth.api.key

    @property
    def name(self):
        return "coinbase"

    def plug(self, cls: object, name: str):
        instance = cls(self.messenger)
        setattr(self, name, instance)


def get_messenger(settings: dict = None) -> Messenger:
    return Messenger(Auth(API(settings)))


def get_client(settings: dict = None) -> Coinbase:
    return Coinbase(Messenger(Auth(API(settings))))
