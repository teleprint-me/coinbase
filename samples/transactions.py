from json import load
from pprint import pprint

from coinbase.wallet import Coinbase, get_client


def get_settings(filename: str) -> dict:
    data = None
    with open(filename, "r") as file:
        data = load(file)
    return data


currency_code = "BTC"
bitcoin: dict = None

print("[Client] Loading coinbase client...")
settings = get_settings("settings.json")["api"]
client: Coinbase = get_client(settings)
print("[Client] Loading client data...")
print("[Client] [Account] Loading account list...")
accounts: list[dict] = client.account.list()

print(f"[Account] Using currency code: {currency_code}")
for account in accounts:
    if account["currency"]["code"] == currency_code:
        print(f"[Account] Found currency: {currency_code}")
        bitcoin = account
        break

print("[Client] [Object] Loading transaction list...")
results = client.transaction.list(bitcoin["id"])
results += client.buy.list(bitcoin["id"])
results += client.sell.list(bitcoin["id"])
print(f"[Client] [Object] Total transactions loaded: {len(results)}")

print("[Client] [Object] Printing transaction list.")
print()
for result in results:
    pprint(result)
    print()
print("[Client] [Object] Done!")
