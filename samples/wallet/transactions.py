from json import load
from pprint import pprint
from coinbase.api import get_api_settings
from coinbase.wallet import Wallet, get_wallet


def get_account(wallet: Wallet, currency_code: str) -> dict:
    """Returns the account with the specified currency code.

    Arguments:
    - wallet: Wallet: a Coinbase API wallet instance
    - currency_code: str: the currency code to retrieve the account for

    Returns:
    dict: the account with the specified currency code
    """
    accounts = wallet.account.list()
    for account in accounts:
        if currency_code == account["currency"]["code"]:
            return account


def get_transactions(wallet: Wallet, account_id: str) -> list:
    """Returns a list of transactions for the specified account.

    Arguments:
    - wallet: Wallet: a Coinbase API wallet instance
    - account_id: str: the ID of the account to retrieve transactions for

    Returns:
    list: a list of transactions for the specified account
    """
    results = wallet.transaction.list(account_id)
    results += wallet.buy.list(account_id)
    results += wallet.sell.list(account_id)
    return results


def main():
    currency_code: str = "BTC"
    bitcoin: dict = None
    results: list = None

    print("[Client] Loading wallet...")

    settings: dict = get_api_settings()
    wallet: Wallet = get_wallet(settings)

    print("[Client] Loading wallet account list...")

    bitcoin = get_account(wallet, currency_code)

    if not bitcoin:
        raise ValueError(f"No {currency_code} account found")

    print(f"[Client] Using: {currency_code}")

    print("[Client] Loading wallet transaction list...")

    results = get_transactions(wallet, bitcoin["id"])

    print(f"[Client] Total wallet transactions: {len(results)}")

    print("[Client] Printing results...")
    print()

    for result in results:
        pprint(result)
        print()

    print("[Client] Done!")


if __name__ == "__main__":
    main()
