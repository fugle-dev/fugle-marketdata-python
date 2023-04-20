from fugle_marketdata import WebSocketClient
import pytest
# import websocket


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


