from pprint import pprint
from coinbase.api import get_api_settings
from coinbase.wallet import get_wallet
from coinbase.wallet import Wallet


def get_account_id(wallet: Wallet, currency_code: str) -> str:
    """
    Given a `wallet` and `currency_code`, returns the account ID for the
    specified currency. If no such account exists, returns an empty string.
    """
    return next(
        (
            account["id"]
            for account in wallet.account.list()
            if account["currency"]["code"] == currency_code
        ),
        "",
    )


# Get the API settings and create a Wallet object
settings: dict = get_api_settings()
wallet: Wallet = get_wallet(settings)

# Get the time and account information
time: dict = wallet.time.get()
account_id: str = get_account_id(wallet, "BTC")
account: dict = wallet.account.get(account_id)

# Print the time and account information for debugging purposes
pprint(time)
pprint(account)
