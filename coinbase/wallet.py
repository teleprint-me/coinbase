# teleprint-me/coinbase - A Python Wrapper for Coinbase
# Copyright (C) 2021 Austin Berrio
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
        return [result for page in pages for result in page.json()["data"]]

    def get(self, account_id: str) -> dict:
        return self.messenger.get(f"/accounts/{account_id}").json()

    def update(self, account_id: str, data: dict) -> dict:
        return self.messenger.put(f"/accounts/{account_id}", data).json()

    def delete(self, account_id: str) -> dict:
        return self.messenger.delete(f"/accounts/{account_id}").json()


class Address(Subscriber):
    def list(self, account_id: str, data: dict = None) -> list:
        pages = self.messenger.page(f"/accounts/{account_id}/addresses", data)
        return [result for page in pages for result in page.json()["data"]]

    def get(self, account_id: str, address_id: str) -> dict:
        return self.messenger.get(f"/accounts/{account_id}/addresses/{address_id}")

    def transactions(self, account_id: str, address_id: str, data: dict = None) -> list:
        pages = self.messenger.page(
            f"/accounts/{account_id}/addresses/{address_id}/transactions", data
        )
        return [tx for page in pages for tx in page.json()["data"]]

    def create(self, account_id: str, data: dict) -> dict:
        return self.messenger.post(f"/accounts/{account_id}/addresses", data).json()


class Transaction(Subscriber):
    def list(self, account_id: str, data: dict = None) -> list:
        pages = self.messenger.page(f"/accounts/{account_id}/transactions", data)
        return [tx for page in pages for tx in page.json()["data"]]

    def get(self, account_id: str, transaction_id: str) -> dict:
        return self.messenger.get(
            f"/accounts/{account_id}/transactions/{transaction_id}"
        ).json()

    def send(self, account_id: str, data: dict) -> dict:
        return self.messenger.post(f"/accounts/{account_id}/transactions", data).json()

    def complete(self, account_id: str, transaction_id: str) -> dict:
        return self.messenger.post(
            f"/accounts/{account_id}/transactions/{transaction_id}/complete"
        ).json()

    def resend(self, account_id: str, transaction_id: str) -> dict:
        return self.messenger.post(
            f"/accounts/{account_id}/transactions/{transaction_id}/resend"
        ).json()

    def cancel(self, account_id: str, transaction_id: str) -> dict:
        return self.messenger.delete(
            f"/accounts/{account_id}/transactions/{transaction_id}"
        ).json()


class Buy(Subscriber):
    def list(self, account_id: str, data: dict = None) -> list:
        pages = self.messenger.page(f"/accounts/{account_id}/buys", data)
        return [result for page in pages for result in page.json()["data"]]

    def get(self, account_id: str, buy_id: str) -> dict:
        return self.messenger.get(f"/accounts/{account_id}/buys/{buy_id}").json()

    def order(self, account_id: str, data: dict) -> dict:
        return self.messenger.post(f"/accounts/{account_id}/buys", data).json()

    def commit(self, account_id: str, buy_id: str) -> dict:
        return self.messenger.post(
            f"/accounts/{account_id}/buys/{buy_id}/commit"
        ).json()


class Sell(Subscriber):
    def list(self, account_id: str, data: dict = None) -> list:
        pages = self.messenger.page(f"/accounts/{account_id}/sells", data)
        return [result for page in pages for result in page.json()["data"]]

    def get(self, account_id: str, sell_id: str) -> dict:
        return self.messenger.get(f"/accounts/{account_id}/sells/{sell_id}").json()

    def order(self, account_id: str, data: dict) -> dict:
        return self.messenger.post(f"/accounts/{account_id}/sells", data).json()

    def commit(self, account_id: str, sell_id: str) -> dict:
        return self.messenger.post(
            f"/accounts/{account_id}/sells/{sell_id}/commit"
        ).json()


class Deposit(Subscriber):
    def list(self, account_id: str, data: dict = None) -> list:
        pages = self.messenger.page(f"/accounts/{account_id}/deposits", data)
        return [buy for page in pages for buy in page.json()["data"]]

    def get(self, account_id: str, deposit_id: str) -> dict:
        return self.messenger.get(
            f"/accounts/{account_id}/deposits/{deposit_id}"
        ).json()

    def funds(self, account_id: str, data: dict) -> dict:
        return self.messenger.post(f"/accounts/{account_id}/deposits", data).json()

    def commit(self, account_id: str, deposit_id: str) -> dict:
        return self.messenger.post(
            f"/accounts/{account_id}/deposits/{deposit_id}/commit"
        ).json()


class Withdraw(Subscriber):
    def list(self, account_id: str, data: dict = None) -> list:
        pages = self.messenger.page(f"/accounts/{account_id}/withdrawals", data)
        return [result for page in pages for result in page.json()["data"]]

    def get(self, account_id: str, withdrawal_id: str) -> dict:
        return self.messenger.get(
            f"/accounts/{account_id}/withdrawals/{withdrawal_id}"
        ).json()

    def funds(self, account_id: str, data: dict) -> dict:
        return self.messenger.post(f"/accounts/{account_id}/withdrawals", data).json()

    def commit(self, account_id: str, withdrawal_id: str) -> dict:
        return self.messenger.post(
            f"/accounts/{account_id}/withdrawals/{withdrawal_id}/commit"
        ).json()


class Payment(Subscriber):
    def list(self, data: dict = None) -> dict:
        return self.messenger.get("/payment-methods", data).json()

    def get(self, payment_method_id: str) -> dict:
        return self.messenger.get(f"/payment-methods/{payment_method_id}").json()


class Currency(Subscriber):
    def get(self) -> dict:
        return self.messenger.get("/currencies").json()


class Exchange(Subscriber):
    def rates(self) -> dict:
        return self.messenger.get("/exchange-rates").json()


class Price(Subscriber):
    def buy(self, currency_pair: str, data: dict = None) -> dict:
        return self.messenger.get(f"/prices/{currency_pair}/buy", data).json()

    def sell(self, currency_pair: str, data: dict = None) -> dict:
        return self.messenger.get(f"/prices/{currency_pair}/sell", data).json()

    def spot(self, currency_pair: str, data: dict = None) -> dict:
        return self.messenger.get(f"/prices/{currency_pair}/spot", data).json()


class Time(Subscriber):
    def get(self) -> dict:
        # NOTE: The `epoch` field represents decimal seconds since Unix Epoch
        return self.messenger.get("/time").json()


class Wallet(AbstractClient):
    def __init__(self, messenger: Messenger):
        self.messenger = messenger
        self.user = User(messenger)
        self.account = Account(messenger)
        self.address = Address(messenger)
        self.transaction = Transaction(messenger)
        self.buy = Buy(messenger)
        self.sell = Sell(messenger)
        self.deposit = Deposit(messenger)
        self.withdraw = Withdraw(messenger)
        self.payment = Payment(messenger)
        self.currency = Currency(messenger)
        self.exchange = Exchange(messenger)
        self.price = Price(messenger)
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
    return Messenger(Auth(API(settings if settings else dict())))


def get_client(settings: dict = None) -> Wallet:
    return Wallet(Messenger(Auth(API(settings if settings else dict()))))
