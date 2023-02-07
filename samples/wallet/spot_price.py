from pprint import pprint
from coinbase.api import get_api_settings
from coinbase.wallet import get_wallet

# Get API settings
settings: dict = get_api_settings()

# Get wallet instance
wallet: wallet = get_wallet(settings)

# Get time information
time: dict = wallet.time.get()

# Get spot price for BTC-USD
spot_price: dict = wallet.price.spot("BTC-USD")

# Print time and spot price
pprint(time)
pprint(spot_price)
