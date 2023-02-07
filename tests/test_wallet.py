# abstract
import datetime
import pytest

from dateutil.relativedelta import relativedelta

from tests.teardown import Teardown

from coinbase.messenger import Subscriber

from coinbase.wallet import User
from coinbase.wallet import Account
from coinbase.wallet import Address
from coinbase.wallet import Transaction
from coinbase.wallet import Buy
from coinbase.wallet import Sell
from coinbase.wallet import Deposit
from coinbase.wallet import Withdraw
from coinbase.wallet import Payment
from coinbase.wallet import Currency
from coinbase.wallet import Exchange
from coinbase.wallet import Price
from coinbase.wallet import Time
from coinbase.wallet import Wallet


class TestWallet(object):
    def test_instance(self, wallet: Wallet):
        assert isinstance(wallet, Wallet)

    def test_attributes(self, wallet: Wallet):
        attributes = (
            "messenger",
            "user",
            "account",
            "address",
            "transaction",
            "buy",
            "sell",
            "deposit",
            "withdraw",
            "payment",
            "currency",
            "exchange",
            "price",
            "time",
        )
        assert all(hasattr(wallet, attr) for attr in attributes)

    def test_properties(self, wallet: Wallet):
        assert all(hasattr(wallet, prop) for prop in ("key", "name"))

    def test_methods(self, wallet: Wallet):
        assert callable(wallet.plug)

    def test_plug(self, wallet: Wallet):
        class TestPlug:
            pass


class TestWalletAccount(Teardown):
    def test_list(self, wallet: Wallet):
        accounts = wallet.account.list()
        assert isinstance(accounts, list)
        for account in accounts:
            assert isinstance(account, dict)
            assert "id" in account
            assert "currency" in account
            assert "code" in account["currency"]

    def test_get(self, wallet: Wallet):
        currency_code = "BTC"
        account_id = next(
            (
                account["id"]
                for account in wallet.account.list()
                if account["currency"]["code"] == currency_code
            ),
            "",
        )
        response = wallet.account.get(account_id)
        assert isinstance(response, dict)
        assert "data" in response
        data = response["data"]
        assert all(
            (
                "id" in data and account_id == data["id"],
                "balance" in data and "currency" in data["balance"],
                currency_code == data["balance"]["currency"],
            )
        )


class TestWalletPrice(Teardown):
    def test_price_spot(self, wallet: Wallet):
        response: dict = wallet.price.spot("BTC-USD")
        expected_keys = {"data"}
        expected_data_keys = {"base", "currency", "amount"}
        assert isinstance(response, dict)
        assert expected_keys.issubset(response.keys())
        assert expected_data_keys.issubset(response.get("data", {}).keys())


class TestPublicTime(Teardown):
    def test_get(self, wallet: Wallet):
        response = wallet.time.get()
        assert isinstance(response, dict)
        assert "data" in response
        assert "iso" in response["data"] and "epoch" in response["data"]
