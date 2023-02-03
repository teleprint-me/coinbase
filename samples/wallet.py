from json import load
from pprint import pprint

from coinbase.wallet import Wallet, get_client


def get_settings(filename: str) -> dict:
    data: dict = None
    with open(filename, "r") as file:
        data = load(file)
    return data


currency_code: str = "BTC"
bitcoin: dict = None
results: list = None

print("[Client] Loading wallet...")

settings: dict = get_settings("settings.json")["api"]
wallet: Wallet = get_client(settings)

print("[Client] Loading wallet account list...")

accounts: list[dict] = wallet.account.list()

print(f"[Client] Using: {currency_code}")

for account in accounts:
    if currency_code == account["currency"]["code"]:
        print(f"[Account] Found currency: {currency_code}")
        bitcoin = account
        break

print("[Client] Loading wallet transaction list...")

results = wallet.transaction.list(bitcoin["id"])
results += wallet.buy.list(bitcoin["id"])
results += wallet.sell.list(bitcoin["id"])

print(f"[Client] Total wallet transactions: {len(results)}")

print("[Client] Printing results...")
print()

for result in results:
    pprint(result)
    print()

print("[Client] Done!")
