# teleprint-me/coinbase - Another Unofficial Python Wrapper for Coinbase
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
from coinbase.api import API

from coinbase.auth import Auth

from coinbase.messenger import Messenger
from coinbase.messenger import Subscriber


class User(Subscriber):
    """Manage User account details and authentication.

    :param Subscriber: The subscriber class to inherit from.
    :param messenger: An instance of Messenger to send API requests
    """

    def get(self) -> dict:
        """Get the authenticated User's details.

        :return: A dictionary containing the User's details.
        """
        return self.messenger.get("/user").json()

    def auth(self) -> dict:
        """Get the authenticated User's authorization information.

        :return: A dictionary containing the User's authorization information.
        """
        return self.messenger.get("/user/auth").json()

    def profile(self, user_id: str) -> dict:
        """Get the User's profile information by User ID.

        :param user_id: The User's unique identifier.
        :return: A dictionary containing the User's profile information.
        """
        return self.messenger.get(f"/users/{user_id}").json()

    def update(self, data: dict) -> dict:
        """Update the authenticated User's profile information.

        :param data: A dictionary containing the User's updated information.
        :return: A dictionary containing the User's updated profile information.
        """
        return self.messenger.put("/user", data).json()


class Account(Subscriber):
    """Interact with the Coinbase Pro account API endpoints.

    :param Subscriber: The subscriber class to inherit from.
    :param messenger: Messenger object used to make API requests.
    """

    def list(self, data: dict = None) -> list[dict]:
        """Get a list of all accounts.

        :param data: Additional data to include in the request query parameters.
        :return: A list of dictionaries representing the accounts.
        """
        pages = self.messenger.page("/accounts", data)
        return [result for page in pages for result in page.json()["data"]]

    def get(self, account_id: str) -> dict:
        """Get a specific account.

        :param account_id: The ID of the account to retrieve.
        :return: A dictionary representing the account.
        """
        return self.messenger.get(f"/accounts/{account_id}").json()

    def update(self, account_id: str, data: dict) -> dict:
        """Update a specific account.

        :param account_id: The ID of the account to update.
        :param data: Data to include in the request body.
        :return: A dictionary representing the updated account.
        """
        return self.messenger.put(f"/accounts/{account_id}", data).json()

    def delete(self, account_id: str) -> dict:
        """Delete a specific account.

        :param account_id: The ID of the account to delete.
        :return: A dictionary representing the deleted account.
        """
        return self.messenger.delete(f"/accounts/{account_id}").json()


class Address(Subscriber):
    """Interact with the Coinbase addresses API endpoints.

    :param Subscriber: The subscriber class to inherit from.
    :param messenger: Messenger object used to make API requests.
    """

    def list(self, account_id: str, data: dict = None) -> list[dict]:
        """Get a list of addresses for a given account.

        :param account_id: The ID of the account to retrieve addresses for.
        :param data: Optional parameters for the API request.
        :return: List of dictionaries representing addresses.
        """
        pages = self.messenger.page(f"/accounts/{account_id}/addresses", data)
        return [result for page in pages for result in page.json()["data"]]

    def get(self, account_id: str, address_id: str) -> dict:
        """Get a specific address for a given account.

        :param account_id: The ID of the account the address belongs to.
        :param address_id: The ID of the address to retrieve.
        :return: Dictionary representing the address.
        """
        return self.messenger.get(
            f"/accounts/{account_id}/addresses/{address_id}"
        ).json()

    def transactions(
        self, account_id: str, address_id: str, data: dict = None
    ) -> list:
        """Get a list of transactions for a given address.

        :param account_id: The ID of the account the address belongs to.
        :param address_id: The ID of the address to retrieve transactions for.
        :param data: Optional parameters for the API request.
        :return: List of dictionaries representing transactions.
        """
        pages = self.messenger.page(
            f"/accounts/{account_id}/addresses/{address_id}/transactions", data
        )
        return [tx for page in pages for tx in page.json()["data"]]

    def create(self, account_id: str, data: dict) -> dict:
        """Create a new address for a given account.

        :param account_id: The ID of the account to create the address for.
        :param data: Data to use in creating the address.
        :return: Dictionary representing the newly created address.
        """
        return self.messenger.post(
            f"/accounts/{account_id}/addresses", data
        ).json()


class Transaction(Subscriber):
    """Interact with the Coinbase transaction API endpoints.

    :param Subscriber: The subscriber class to inherit from.
    :param messenger: Messenger object used to make API requests.
    """

    def list(self, account_id: str, data: dict = None) -> list[dict]:
        """List all transactions for an account.

        :param account_id: Coinbase account id.
        :param data: Dictionary of query parameters.

        :return: List of transactions.
        """
        pages = self.messenger.page(
            f"/accounts/{account_id}/transactions", data
        )
        return [tx for page in pages for tx in page.json()["data"]]

    def get(self, account_id: str, transaction_id: str) -> dict:
        """Get a transaction for a specific account.

        :param account_id: Coinbase account id.
        :param transaction_id: Coinbase transaction id.

        :return: Dictionary of transaction details.
        """
        return self.messenger.get(
            f"/accounts/{account_id}/transactions/{transaction_id}"
        ).json()

    def send(self, account_id: str, data: dict) -> dict:
        """Send money to a Bitcoin address, email address, or phone number.

        :param account_id: Coinbase account id.
        :param data: Dictionary of transaction details.

        :return: Dictionary of transaction details.
        """
        return self.messenger.post(
            f"/accounts/{account_id}/transactions", data
        ).json()

    def complete(self, account_id: str, transaction_id: str) -> dict:
        """Mark a transaction as complete.

        :param account_id: Coinbase account id.
        :param transaction_id: Coinbase transaction id.

        :return: Dictionary of transaction details.
        """
        return self.messenger.post(
            f"/accounts/{account_id}/transactions/{transaction_id}/complete"
        ).json()

    def resend(self, account_id: str, transaction_id: str) -> dict:
        """Resend a transaction receipt.

        :param account_id: Coinbase account id.
        :param transaction_id: Coinbase transaction id.

        :return: Dictionary of transaction details.
        """
        return self.messenger.post(
            f"/accounts/{account_id}/transactions/{transaction_id}/resend"
        ).json()

    def cancel(self, account_id: str, transaction_id: str) -> dict:
        """Cancel a transaction.

        :param account_id: Coinbase account id.
        :param transaction_id: Coinbase transaction id.

        :return: Dictionary of transaction details.
        """
        return self.messenger.delete(
            f"/accounts/{account_id}/transactions/{transaction_id}"
        ).json()


class Buy(Subscriber):
    """Class for handling buy related API requests.

    :param Subscriber: The subscriber class to inherit from.
    :param self.messenger: Messenger object used to make API requests.
    """

    def list(self, account_id: str, data: dict = None) -> list[dict]:
        """Get a list of buys associated with an account.

        :param account_id: The id of the account to get buys for.
        :param data: (optional) Additional data to send with the API request.
        :return: List of buy orders.
        """
        pages = self.messenger.page(f"/accounts/{account_id}/buys", data)
        return [result for page in pages for result in page.json()["data"]]

    def get(self, account_id: str, buy_id: str) -> dict:
        """Get a specific buy order for an account.

        :param account_id: The id of the account associated with the buy order.
        :param buy_id: The id of the buy order to retrieve.
        :return: Buy order details.
        """
        return self.messenger.get(
            f"/accounts/{account_id}/buys/{buy_id}"
        ).json()

    def order(self, account_id: str, data: dict) -> dict:
        """Create a new buy order for an account.

        :param account_id: The id of the account to create the buy order for.
        :param data: Data to send with the API request.
        :return: Buy order details.
        """
        return self.messenger.post(f"/accounts/{account_id}/buys", data).json()

    def commit(self, account_id: str, buy_id: str) -> dict:
        """Commit a specific buy order for an account.

        :param account_id: The id of the account associated with the buy order.
        :param buy_id: The id of the buy order to commit.
        :return: Buy order details.
        """
        return self.messenger.post(
            f"/accounts/{account_id}/buys/{buy_id}/commit"
        ).json()


class Sell(Subscriber):
    """Interact with the Coinbase sell API endpoints.

    :param Subscriber: The base subscriber class
    :param self.messenger: An instance of Messenger to send API requests
    """

    def list(self, account_id: str, data: dict = None) -> list[dict]:
        """List all sells for an account.

        :param account_id: The identifier for the account.
        :param data: Query parameters for the request.
        :return: A list of dictionaries containing information about each sell.
        """
        pages = self.messenger.page(f"/accounts/{account_id}/sells", data)
        return [result for page in pages for result in page.json()["data"]]

    def get(self, account_id: str, sell_id: str) -> dict:
        """Get information about a specific sell.

        :param account_id: The identifier for the account.
        :param sell_id: The identifier for the sell.
        :return: A dictionary containing information about the sell.
        """
        return self.messenger.get(
            f"/accounts/{account_id}/sells/{sell_id}"
        ).json()

    def order(self, account_id: str, data: dict) -> dict:
        """Create a sell order.

        :param account_id: The identifier for the account.
        :param data: The parameters for the sell order.
        :return: A dictionary containing information about the created sell order.
        """
        return self.messenger.post(
            f"/accounts/{account_id}/sells", data
        ).json()

    def commit(self, account_id: str, sell_id: str) -> dict:
        """Commit a sell.

        :param account_id: The identifier for the account.
        :param sell_id: The identifier for the sell.
        :return: A dictionary containing information about the committed sell.
        """
        return self.messenger.post(
            f"/accounts/{account_id}/sells/{sell_id}/commit"
        ).json()


class Deposit(Subscriber):
    """Manage account deposits for an authenticated user.

    :param Subscriber: The base subscriber class
    :param self.messenger: An instance of Messenger to send API requests

    :return: JSON data returned from API requests.
    """

    def list(self, account_id: str, data: dict = None) -> list[dict]:
        """Get a list of deposits for a given account.

        :param account_id: ID of the account to retrieve deposits for.
        :param data: (Optional) Query parameters to pass to the API request.

        :return: List of dictionaries representing each deposit.
        """
        pages = self.messenger.page(f"/accounts/{account_id}/deposits", data)
        return [deposit for page in pages for deposit in page.json()["data"]]

    def get(self, account_id: str, deposit_id: str) -> dict:
        """Get details for a specific deposit.

        :param account_id: ID of the account the deposit belongs to.
        :param deposit_id: ID of the deposit to retrieve details for.

        :return: Dictionary representing the deposit.
        """
        return self.messenger.get(
            f"/accounts/{account_id}/deposits/{deposit_id}"
        ).json()

    def funds(self, account_id: str, data: dict) -> dict:
        """Deposit funds into the given account.

        :param account_id: ID of the account to deposit funds into.
        :param data: Dictionary containing the deposit details.

        :return: Dictionary representing the deposit.
        """
        return self.messenger.post(
            f"/accounts/{account_id}/deposits", data
        ).json()

    def commit(self, account_id: str, deposit_id: str) -> dict:
        """Commit a deposit for the given account.

        :param account_id: ID of the account the deposit belongs to.
        :param deposit_id: ID of the deposit to commit.

        :return: Dictionary representing the deposit.
        """
        return self.messenger.post(
            f"/accounts/{account_id}/deposits/{deposit_id}/commit"
        ).json()


class Withdraw(Subscriber):
    """Interact with the Coinbase Pro withdrawals API endpoints.

    :param Subscriber: The subscriber class to inherit from.
    :param messenger: Messenger object used to make API requests.
    """

    def list(self, account_id: str, data: dict = None) -> list[dict]:
        """List withdrawal history for an account.

        :param account_id: The ID of the account to list withdrawals for.
        :param data: Additional data to pass to the API request.
        :return: A list of withdrawal records.
        """
        pages = self.messenger.page(
            f"/accounts/{account_id}/withdrawals", data
        )
        return [result for page in pages for result in page.json()["data"]]

    def get(self, account_id: str, withdrawal_id: str) -> dict:
        """Get a single withdrawal record for an account.

        :param account_id: The ID of the account to get the withdrawal from.
        :param withdrawal_id: The ID of the withdrawal to retrieve.
        :return: A withdrawal record.
        """
        return self.messenger.get(
            f"/accounts/{account_id}/withdrawals/{withdrawal_id}"
        ).json()

    def funds(self, account_id: str, data: dict) -> dict:
        """Withdraw funds from an account.

        :param account_id: The ID of the account to withdraw from.
        :param data: Data for the withdrawal request.
        :return: A response from the API indicating success or failure.
        """
        return self.messenger.post(
            f"/accounts/{account_id}/withdrawals", data
        ).json()

    def commit(self, account_id: str, withdrawal_id: str) -> dict:
        """Commit a withdrawal.

        :param account_id: The ID of the account to commit the withdrawal from.
        :param withdrawal_id: The ID of the withdrawal to commit.
        :return: A response from the API indicating success or failure.
        """
        return self.messenger.post(
            f"/accounts/{account_id}/withdrawals/{withdrawal_id}/commit"
        ).json()


class Payment(Subscriber):
    """Interact with the Coinbase API payment methods endpoints.

    :param Subscriber: The subscriber class to inherit from.
    :param self.messenger: Messenger object used to make API requests.
    """

    def list(self, data: dict = None) -> dict:
        """Get a list of payment methods available for the authenticated user.

        :param data: (optional) Query parameters for API request.
        :type data: dict, optional
        :return: JSON data returned from API request.
        :rtype: dict
        """
        return self.messenger.get("/payment-methods", data).json()

    def get(self, payment_method_id: str) -> dict:
        """Get information for a payment method.

        :param payment_method_id: ID of the payment method to retrieve.
        :type payment_method_id: str
        :return: JSON data returned from API request.
        :rtype: dict
        """
        return self.messenger.get(
            f"/payment-methods/{payment_method_id}"
        ).json()


class Currency(Subscriber):
    """Get the currency codes and names supported by the API.

    :param Subscriber: The subscriber class to inherit from.
    :type Subscriber: Subscriber
    :param self.messenger: Messenger object used to make API requests.
    :type self.messenger: Messenger
    """

    def get(self) -> dict:
        """Get a list of all currencies supported by the API.

        :return: JSON response from the API.
        :rtype: dict
        """
        return self.messenger.get("/currencies").json()


class Exchange(Subscriber):
    """Get the exchange rates for all supported currencies.

    :param Subscriber: The subscriber class to inherit from.
    :type Subscriber: Subscriber
    :param self.messenger: Messenger object used to make API requests.
    :type self.messenger: Messenger
    """

    def rates(self) -> dict:
        """Get the exchange rates for all supported currencies.

        :return: JSON response from the API.
        :rtype: dict
        """
        return self.messenger.get("/exchange-rates").json()


class Price(Subscriber):
    """Get prices for buying and selling currencies.

    :param Subscriber: The subscriber class to inherit from.
    :param self.messenger: Messenger object used to make API requests.
    """

    def buy(self, currency_pair: str, data: dict = None) -> dict:
        """Get the current buy price for a currency pair.

        :param currency_pair: The currency pair to get the buy price for.
        :type currency_pair: str
        :param data: Additional data to include in the API request.
        :type data: dict, optional
        :return: JSON response from the API.
        :rtype: dict
        """
        return self.messenger.get(f"/prices/{currency_pair}/buy", data).json()

    def sell(self, currency_pair: str, data: dict = None) -> dict:
        """Get the current sell price for a currency pair.

        :param currency_pair: The currency pair to get the sell price for.
        :type currency_pair: str
        :param data: Additional data to include in the API request.
        :type data: dict, optional
        :return: JSON response from the API.
        :rtype: dict
        """
        return self.messenger.get(f"/prices/{currency_pair}/sell", data).json()

    def spot(self, currency_pair: str, data: dict = None) -> dict:
        """Get the current spot price for a currency pair.

        :param currency_pair: The currency pair to get the spot price for.
        :type currency_pair: str
        :param data: Additional data to include in the API request.
        :type data: dict, optional
        :return: JSON response from the API.
        :rtype: dict
        """
        return self.messenger.get(f"/prices/{currency_pair}/spot", data).json()


class Time(Subscriber):
    """Get the current time of the API server.

    :param Subscriber: The subscriber class to inherit from.
    :param self.messenger: Messenger object used to make API requests.
    """

    def get(self) -> dict:
        """Get the current time of the API server.

        :return: JSON response from the API, including the `epoch` field representing decimal seconds since Unix Epoch.
        :rtype: dict
        """
        return self.messenger.get("/time").json()


class Wallet:
    """Class for handling API requests for a coinbase wallet.

    :param messenger: Messenger object for handling API requests.
    """

    def __init__(self, messenger: Messenger):
        """Initialize the wallet with a messenger object.

        :param messenger: Messenger object for handling API requests.
        """
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
        """Return a string representation of the wallet object.

        :return: String representation of the wallet object.
        """
        return f"Wallet(name={self.name}, key={self.key})"

    def __str__(self) -> str:
        """Return the capitalized name of the wallet.

        :return: Capitalized name of the wallet.
        """
        return self.name.capitalize()

    @property
    def key(self) -> str:
        """Return the API key for the wallet.

        :return: API key for the wallet.
        """
        return self.messenger.auth.api.key

    @property
    def name(self):
        """Return the name of the wallet.

        :return: Name of the wallet.
        """
        return "coinbase"

    def plug(self, cls: object, name: str):
        """Add an object to the wallet for handling API requests.

        :param cls: Class to be added to the wallet.
        :param name: Name to give the object when added to the wallet.
        """
        instance = cls(self.messenger)
        setattr(self, name, instance)


def get_wallet(settings: dict) -> Wallet:
    """Return a Wallet object for handling API requests.

    :param settings: Dictionary containing API settings.
    :return: Wallet object for handling API requests.
    """
    return Wallet(Messenger(Auth(API(settings))))
