import websocket
import json
import hmac
import hashlib
import time

# Derived from your Coinbase Retail API Key
#  SIGNING_KEY: the signing key provided as a part of your API key. Also called the "SECRET KEY"
#  API_KEY: the api key provided as a part of your API key. also called the "PUBLIC KEY"
SIGNING_KEY = ""
API_KEY = ""

if not SIGNING_KEY or not API_KEY:
    raise Exception("missing mandatory environment variable(s)")

# the various websocket channels you can subscribe to
# add to this as we go
CHANNEL_NAMES = {
    "level2": "level2",
    "user": "user",
    "tickers": "ticker",
    "ticker_batch": "ticker_batch",
    "status": "status",
    "market_trades": "market_trades",
}

# The base URL of the API
WS_API_URL = "wss://advanced-trade-ws.coinbase.com"


def sign(str, secret):
    hash = hmac.new(secret.encode("utf-8"), str.encode("utf-8"), hashlib.sha256)
    return hash.hexdigest()


def timestamp_and_sign(message, channel, products=[]):
    timestamp = str(int(time.time()))
    str_to_sign = timestamp + channel + ",".join(products)
    sig = sign(str_to_sign, SIGNING_KEY)
    message.update({"signature": sig, "timestamp": timestamp})
    return message


def on_message(ws, message):
    parsed_data = json.loads(message)
    with open("output.txt", "a") as f:
        f.write(message + "\n")


def on_open(ws):
    products = ["BTC-USD"]
    message = {
        "type": "subscribe",
        "channel": CHANNEL_NAMES["user"],
        "api_key": API_KEY,
        "product_ids": products,
    }
    subscribe_msg = timestamp_and_sign(message, CHANNEL_NAMES["user"], products)
    ws.send(json.dumps(subscribe_msg))


def on_close(ws):
    products = ["BTC-USD"]
    message = {
        "type": "unsubscribe",
        "channel": CHANNEL_NAMES["user"],
        "api_key": API_KEY,
        "product_ids": products,
    }
    subscribe_msg = timestamp_and_sign(message, CHANNEL_NAMES["user"], products)
    ws.send(json.dumps(subscribe_msg))


def start_websocket():
    ws = websocket.WebSocketApp(
        WS_API_URL, on_message=on_message, on_close=on_close, on_open=on_open
    )
    ws.run_forever()


start_websocket()
