import requests

from coinbase.api import get_api_settings
from coinbase.messenger import get_advanced_messenger, Messenger

settings: dict = get_api_settings()
messenger: Messenger = get_advanced_messenger(settings)

url: str = "https://api.coinbase.com/api/v3/brokerage/products/BTC-USD"

# Test that the advanced API generates the correct URL
assert callable(messenger.api.url)
assert url == messenger.api.url("/products/BTC-USD")

# Get the product information for Bitcoin to USD
response = messenger.get("/products/BTC-USD")

# Ensure that the request was successful
assert 200 == response.status_code

# Parse the JSON response
payload = response.json()

# Check that the expected keys are present in the payload
assert "product_id" in payload and "price" in payload

# Clean up the session
messenger.session.close()
