FUGLE_MARKETDATA_API_REST_BASE_URL = 'https://api.fugle.tw/marketdata'
FUGLE_MARKETDATA_API_WEBSOCKET_BASE_URL = 'wss://api.fugle.tw/marketdata'
FUGLE_MARKETDATA_API_VERSION = 'v1.0'

# WebSocket streaming versions available per product, oldest first — the last
# entry is the product's latest and is what you get when no `version` option is
# supplied.
#
# futopt v1.1 is v1.0 plus trial-matching (試撮, TAIFEX I022/I082) frames on the
# `trades` and `books` channels, which carry a top-level `isTrial: true`.
# Stock has no v1.1: its trials have always been streamed, so there was no
# compatibility break to gate.
FUGLE_MARKETDATA_WS_SUPPORTED_VERSIONS = {
    'stock': ('v1.0',),
    'futopt': ('v1.0', 'v1.1'),
}

CONNECT_EVENT = 'connect'
DISCONNECT_EVENT = 'disconnect'
MESSAGE_EVENT = 'message'
ERROR_EVENT = 'error'
AUTHENTICATED_EVENT = 'authenticated'
UNAUTHENTICATED_EVENT = 'unauthenticated'
UNAUTHENTICATED_MESSAGE = 'Invalid authentication credentials'
AUTHENTICATION_TIMEOUT_MESSAGE = 'authentication timeout'
MISSING_CREDENTIALS_MESSAGE= 'missing authentication credentials'
