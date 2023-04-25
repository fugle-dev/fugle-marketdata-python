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


class TestWebSocketClient:

    def test_return_web_socket_stock_client(self):
        client = WebSocketClient(api_key='api-key')
        stock = client.stock
        assert isinstance(stock, WebSocketStockClient)


    def test_return_web_socket_stock_client(self):
        client = WebSocketClient(api_key='api-key')
        futopt = client.futopt
        assert isinstance(futopt, WebSocketFutOptClient)