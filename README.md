[![PyPI version][pypi-image]][pypi-url]
[![Python version][python-image]][python-url]
[![Build Status][action-image]][action-url]
# Fugle MarketData

[![PyPI version][pypi-image]][pypi-url]
[![Python version][python-image]][python-url]
[![Build Status][action-image]][action-url]

> Fugle MarketData API client library for Node.js

## Installation

```sh
$ pip install fugle-marketdata
```

## Importing

```py
from fugle_marketdata import WebSocketClient, RestClient

```

## Usage

The library is an isomorphic Python client that supports REST API and WebSocket.

### REST API

```py

# def main():
#     client = RestClient(api_key=TOKEN)
#     stock = client.stock
#     print(stock.intraday.quote(symbol="2330"))


client = RestClient(api_key = 'YOUR_API_KEY')
stock = client.stock  # Stock REST API client
print(stock.intraday.quote(symbol="2330"))
```

### WebSocket API

```py

from fugle_marketdata import WebSocketClient, RestClient
import asyncio

def handle_message(message):
    print(message)

async def main():
    client = WebSocketClient(api_key = 'YOUR_API_KEY')
    stock = client.stock
    stock.on("message", handle_message)
    await stock.connect()
    stock.subscribe({ 
        "channel": 'trades', 
        "symbol": '2330' 
        })
if __name__ == "__main__":
    asyncio.run(main())

```

## License

[MIT](LICENSE)

