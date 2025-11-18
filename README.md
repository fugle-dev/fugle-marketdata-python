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

## Error Handling

The library provides a custom `FugleAPIError` exception for API-related errors, which includes detailed debugging information.

### Catching API Errors

```py
from fugle_marketdata import RestClient, FugleAPIError

client = RestClient(api_key='YOUR_API_KEY')

try:
    data = client.stock.intraday.quote(symbol="2330")
except FugleAPIError as e:
    # Access error details for debugging
    print(f"Error: {e.message}")
    print(f"URL: {e.url}")
    print(f"Status Code: {e.status_code}")
    print(f"Request Params: {e.params}")
    print(f"Response: {e.response_text}")
```

### Error Attributes

The `FugleAPIError` exception provides the following attributes:

- `message`: Error description
- `url`: The API endpoint that was called
- `status_code`: HTTP status code (if available)
- `params`: Request parameters that were sent
- `response_text`: Raw response text from the API (truncated to 200 chars)

### Common Error Scenarios

**HTTP Errors (4xx, 5xx):**
```py
try:
    data = client.stock.intraday.quote(symbol="INVALID_SYMBOL")
except FugleAPIError as e:
    if e.status_code == 404:
        print("Symbol not found")
    elif e.status_code >= 500:
        print("Server error, please try again later")
```

**Network Errors:**
```py
try:
    data = client.stock.intraday.quote(symbol="2330")
except FugleAPIError as e:
    if e.status_code is None:
        print("Network error occurred")
```

## License

[MIT](LICENSE)
