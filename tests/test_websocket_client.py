import threading
from fugle_marketdata import WebSocketClient
from fugle_marketdata.websocket.futopt.client import WebSocketFutOptClient
from fugle_marketdata.websocket.stock.client import WebSocketStockClient
import pytest
import websocket
import asyncio


@pytest.fixture
def api_key_client():
    return WebSocketClient(api_key='api-key')


@pytest.fixture
def bearer_client():
    return WebSocketClient(bearer_token='bearer-token')

@pytest.fixture
def custom_base_url_client():
    return WebSocketClient(api_key='test-key', base_url='wss://custom-ws.example.com/v2.0')


class TestWebSocketClientConstructor(object):
    def test_with_apiKey(self):
        # 建立 WebSocketClient 實例並測試是否為 WebSocketClient 物件
        client = WebSocketClient(api_key='api-key')
        assert isinstance(client, WebSocketClient)

    def test_with_bearerToken(self):
        # 建立 WebSocketClient 實例並測試是否為 WebSocketClient 物件
        client = WebSocketClient(bearer_token='bearer-token')
        assert isinstance(client, WebSocketClient)

    def test_with_no_options(self):
        # 測試是否會拋出錯誤
        with pytest.raises(Exception):
            WebSocketClient()

    def test_with_both_apiKey_and_bearerToken(self):
        # 測試是否會拋出錯誤
        with pytest.raises(Exception):
            WebSocketClient(api_key='api-key', bearer_token='bearer-token')

    def test_with_custom_base_url(self):
        # 測試自訂 base_url 是否正確設定
        client = WebSocketClient(api_key='api-key', base_url='wss://custom-ws.example.com/v2.0')
        assert isinstance(client, WebSocketClient)
        assert client.options['base_url'] == 'wss://custom-ws.example.com/v2.0'


class TestWebSocketClient:

    def test_return_web_socket_stock_client(self):
        client = WebSocketClient(api_key='api-key')
        stock = client.stock
        assert isinstance(stock, WebSocketStockClient)

    def test_return_web_socket_futopt_client(self):
        client = WebSocketClient(api_key='api-key')
        futopt = client.futopt
        assert isinstance(futopt, WebSocketFutOptClient)

    def test_stock_with_custom_base_url(self, custom_base_url_client):
        stock = custom_base_url_client.stock
        assert isinstance(stock, WebSocketStockClient)
        assert stock.config['base_url'] == 'wss://custom-ws.example.com/v2.0/stock/streaming'

    def test_futopt_with_custom_base_url(self, custom_base_url_client):
        futopt = custom_base_url_client.futopt
        assert isinstance(futopt, WebSocketFutOptClient)
        assert futopt.config['base_url'] == 'wss://custom-ws.example.com/v2.0/futopt/streaming'

    def test_stock_and_futopt_different_instances(self, api_key_client):
        stock = api_key_client.stock
        futopt = api_key_client.futopt
        assert stock is not futopt

    def test_stock_same_instance_caching(self, api_key_client):
        stock1 = api_key_client.stock
        stock2 = api_key_client.stock
        assert stock1 is stock2


class TestWebSocketClientFactoryUrlConstruction:
    def test_default_base_url_construction(self, api_key_client):
        # 測試預設 base_url 的 WebSocket URL 構造
        stock = api_key_client.stock
        assert stock.config['base_url'] == 'wss://api.fugle.tw/marketdata/v1.0/stock/streaming'
        
        futopt = api_key_client.futopt
        assert futopt.config['base_url'] == 'wss://api.fugle.tw/marketdata/v1.0/futopt/streaming'

    def test_custom_base_url_construction(self, custom_base_url_client):
        # 測試自訂 base_url 的 WebSocket URL 構造
        stock = custom_base_url_client.stock
        assert stock.config['base_url'] == 'wss://custom-ws.example.com/v2.0/stock/streaming'
        
        futopt = custom_base_url_client.futopt
        assert futopt.config['base_url'] == 'wss://custom-ws.example.com/v2.0/futopt/streaming'

    def test_url_construction_with_trailing_slash(self):
        # 測試帶有結尾斜線的 base_url，確保沒有雙斜線
        client = WebSocketClient(api_key='test-key', base_url='wss://ws.example.com/v1/')
        stock = client.stock
        assert stock.config['base_url'] == 'wss://ws.example.com/v1/stock/streaming'

    def test_multiple_clients_independent_base_urls(self):
        # 測試多個 WebSocket 客戶端的 base_url 是獨立的
        client1 = WebSocketClient(api_key='key1', base_url='wss://ws1.example.com')
        client2 = WebSocketClient(api_key='key2', base_url='wss://ws2.example.com')
        
        stock1 = client1.stock
        stock2 = client2.stock
        
        assert stock1.config['base_url'] == 'wss://ws1.example.com/stock/streaming'
        assert stock2.config['base_url'] == 'wss://ws2.example.com/stock/streaming'


class TestWebSocketClientRegressionTests:
    def test_default_behavior_without_base_url(self, api_key_client):
        # 回歸測試：確保不提供 base_url 時使用預設值
        stock = api_key_client.stock
        assert 'wss://api.fugle.tw/marketdata/v1.0/stock/streaming' in stock.config['base_url']
        
        futopt = api_key_client.futopt
        assert 'wss://api.fugle.tw/marketdata/v1.0/futopt/streaming' in futopt.config['base_url']

    def test_api_key_authentication_preserved(self, api_key_client):
        # 回歸測試：確保 API key 認證仍然正常
        stock = api_key_client.stock
        assert stock.config['api_key'] == 'api-key'
        assert 'bearer_token' not in stock.config

    def test_bearer_token_authentication_preserved(self, bearer_client):
        # 回歸測試：確保 Bearer token 認證仍然正常
        stock = bearer_client.stock
        assert stock.config['bearer_token'] == 'bearer-token'
        assert 'api_key' not in stock.config

    def test_websocket_client_methods_preserved(self, api_key_client):
        # 回歸測試：確保 WebSocket 客戶端方法仍然存在
        stock = api_key_client.stock
        
        # 確保基本方法仍然存在
        assert hasattr(stock, 'connect')
        assert hasattr(stock, 'disconnect')
        assert hasattr(stock, 'subscribe')
        assert hasattr(stock, 'unsubscribe')
        assert hasattr(stock, 'on')
        assert hasattr(stock, 'off')
        
        # 確保配置正確傳遞
        assert stock.config['api_key'] == 'api-key'


class TestWebSocketClientUrlNormalization:
    def test_no_trailing_slash_base_url(self):
        # 測試沒有結尾斜線的 base_url
        client = WebSocketClient(api_key='test-key', base_url='wss://ws.example.com/v1')
        stock = client.stock
        assert stock.config['base_url'] == 'wss://ws.example.com/v1/stock/streaming'
        
    def test_single_trailing_slash_base_url(self):
        # 測試單一結尾斜線的 base_url
        client = WebSocketClient(api_key='test-key', base_url='wss://ws.example.com/v1/')
        stock = client.stock
        assert stock.config['base_url'] == 'wss://ws.example.com/v1/stock/streaming'
        
    def test_multiple_trailing_slashes_base_url(self):
        # 測試多個結尾斜線的 base_url
        client = WebSocketClient(api_key='test-key', base_url='wss://ws.example.com/v1///')
        stock = client.stock
        assert stock.config['base_url'] == 'wss://ws.example.com/v1/stock/streaming'
        
    def test_base_url_with_path_and_trailing_slash(self):
        # 測試帶有路徑和結尾斜線的 base_url
        client = WebSocketClient(api_key='test-key', base_url='wss://ws.example.com/api/v2/')
        stock = client.stock
        assert stock.config['base_url'] == 'wss://ws.example.com/api/v2/stock/streaming'
        futopt = client.futopt
        assert futopt.config['base_url'] == 'wss://ws.example.com/api/v2/futopt/streaming'