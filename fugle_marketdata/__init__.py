from .rest import RestClientFactory as RestClient
from .websocket import WebSocketClientFactory as WebSocketClient, HealthCheckConfig
from .exceptions import FugleAPIError

__version__ = '2.5.0rc5'

__all__ = ['RestClient', 'WebSocketClient', 'HealthCheckConfig', 'FugleAPIError', '__version__']
