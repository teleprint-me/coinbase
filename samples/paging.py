from pprint import pprint

from requests import Response

from coinbase.api import get_api_settings

from coinbase.messenger import get_advanced_messenger
from coinbase.messenger import AdvancedMessenger

settings: dict = get_api_settings()
advanced_messenger: AdvancedMessenger = get_advanced_messenger(settings)
responses: list[Response] = advanced_messenger.page("/accounts")
accounts: list[dict] = []

pprint(responses)

for response in responses:
    page = response.json()
    accounts.append([account for account in page["accounts"]])

pprint(accounts)
