# Fugle MarketData

> Fugle MarketData API client library for Python

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

client = RestClient(api_key = 'YOUR_API_KEY')
stock = client.stock  # Stock REST API client
print(stock.intraday.quote(symbol="2330"))
```

### WebSocket API

```py
from fugle_marketdata import WebSocketClient, RestClient


def handle_message(message):
    print(f'message: {message}')


def handle_connect():
    print('connected')


def handle_disconnect(code, message):
    print(f'disconnect: {code}, {message}')


def handle_error(error):
    print(f'error: {error}')


def main():
    client = WebSocketClient(api_key='YOUR_API_KEY')
    stock = client.stock
    stock.on("connect", handle_connect)
    stock.on("message", handle_message)
    stock.on("disconnect", handle_disconnect)
    stock.on("error", handle_error)
    stock.connect()
    stock.subscribe({
        "channel": 'trades',
        "symbol": '2330'
    })


if __name__ == "__main__":
    main()

```

## License

[MIT](LICENSE)
