import threading
import time
from fugle_marketdata import WebSocketClient
from fugle_marketdata.websocket.client import HealthCheckConfig, WebSocketClient as CoreWebSocketClient
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
    return WebSocketClient(api_key='test-key', base_url='wss://custom-ws.example.com')


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
        client = WebSocketClient(api_key='api-key', base_url='wss://custom-ws.example.com')
        assert isinstance(client, WebSocketClient)
        assert client.options['base_url'] == 'wss://custom-ws.example.com'


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
        assert stock.url == 'wss://custom-ws.example.com/v1.0/stock/streaming'

    def test_futopt_with_custom_base_url(self, custom_base_url_client):
        futopt = custom_base_url_client.futopt
        assert isinstance(futopt, WebSocketFutOptClient)
        assert futopt.url == 'wss://custom-ws.example.com/v1.1/futopt/streaming'

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
        assert stock.url == 'wss://api.fugle.tw/marketdata/v1.0/stock/streaming'
        
        futopt = api_key_client.futopt
        assert futopt.url == 'wss://api.fugle.tw/marketdata/v1.1/futopt/streaming'

    def test_custom_base_url_construction(self, custom_base_url_client):
        # 測試自訂 base_url 的 WebSocket URL 構造
        stock = custom_base_url_client.stock
        assert stock.url == 'wss://custom-ws.example.com/v1.0/stock/streaming'
        
        futopt = custom_base_url_client.futopt
        assert futopt.url == 'wss://custom-ws.example.com/v1.1/futopt/streaming'

    def test_url_construction_with_trailing_slash(self):
        # 測試帶有結尾斜線的 base_url，確保沒有雙斜線
        client = WebSocketClient(api_key='test-key', base_url='wss://ws.example.com/marketdata/')
        stock = client.stock
        assert stock.url == 'wss://ws.example.com/marketdata/v1.0/stock/streaming'

    def test_multiple_clients_independent_base_urls(self):
        # 測試多個 WebSocket 客戶端的 base_url 是獨立的
        client1 = WebSocketClient(api_key='key1', base_url='wss://ws1.example.com')
        client2 = WebSocketClient(api_key='key2', base_url='wss://ws2.example.com')

        stock1 = client1.stock
        stock2 = client2.stock

        assert stock1.url == 'wss://ws1.example.com/v1.0/stock/streaming'
        assert stock2.url == 'wss://ws2.example.com/v1.0/stock/streaming'


class TestWebSocketClientFactoryVersion:
    BASE = 'wss://api.fugle.tw/marketdata'

    def test_defaults_to_each_product_latest(self, api_key_client):
        assert api_key_client.futopt.url == f'{self.BASE}/v1.1/futopt/streaming'
        assert api_key_client.stock.url == f'{self.BASE}/v1.0/stock/streaming'

    def test_empty_mapping_matches_no_version_at_all(self):
        client = WebSocketClient(api_key='api-key', version={})
        assert client.futopt.url == f'{self.BASE}/v1.1/futopt/streaming'
        assert client.stock.url == f'{self.BASE}/v1.0/stock/streaming'

    def test_scalar_version_is_rejected(self):
        client = WebSocketClient(api_key='api-key', version='v1.1')
        with pytest.raises(TypeError) as excinfo:
            client.futopt
        assert str(excinfo.value) == (
            "version must be a per-product mapping, not the bare string 'v1.1'. "
            "Use version={'futopt': 'v1.1'}."
        )

    def test_rejected_scalar_names_every_product_that_serves_it(self):
        client = WebSocketClient(api_key='api-key', version='v1.0')
        with pytest.raises(TypeError) as excinfo:
            client.stock
        assert str(excinfo.value) == (
            "version must be a per-product mapping, not the bare string 'v1.0'. "
            "Use version={'stock': 'v1.0', 'futopt': 'v1.0'}."
        )

    def test_version_mapping(self):
        client = WebSocketClient(api_key='api-key', version={'futopt': 'v1.1'})
        assert client.futopt.url == f'{self.BASE}/v1.1/futopt/streaming'
        assert client.stock.url == f'{self.BASE}/v1.0/stock/streaming'

    def test_version_mapping_pins_futopt_back_to_v1_0(self):
        client = WebSocketClient(api_key='api-key', version={'futopt': 'v1.0'})
        assert client.futopt.url == f'{self.BASE}/v1.0/futopt/streaming'

    def test_version_mapping_raises_for_unsupported_pair(self):
        client = WebSocketClient(api_key='api-key', version={'stock': 'v1.1'})
        with pytest.raises(TypeError) as excinfo:
            client.stock
        assert 'stock streaming does not support v1.1' in str(excinfo.value)

    def test_custom_base_url_is_versioned_per_product_without_version_option(self):
        client = WebSocketClient(api_key='api-key', base_url='wss://fubon-api.fugle.tw/marketdata')
        assert client.futopt.url == 'wss://fubon-api.fugle.tw/marketdata/v1.1/futopt/streaming'
        assert client.stock.url == 'wss://fubon-api.fugle.tw/marketdata/v1.0/stock/streaming'

    def test_version_option_applies_to_custom_base_url(self):
        client = WebSocketClient(
            api_key='api-key',
            base_url='wss://api-dev.fugle.tw/marketdata',
            version={'futopt': 'v1.0'},
        )
        assert client.futopt.url == 'wss://api-dev.fugle.tw/marketdata/v1.0/futopt/streaming'
        assert client.stock.url == 'wss://api-dev.fugle.tw/marketdata/v1.0/stock/streaming'

    def test_base_url_carrying_a_version_segment_is_rejected(self):
        client = WebSocketClient(api_key='api-key', base_url='wss://api-dev.fugle.tw/marketdata/v1.0')
        with pytest.raises(TypeError) as excinfo:
            client.futopt
        assert str(excinfo.value) == (
            "base_url must not include a version segment (found '/v1.0'). "
            "Pass the host and path prefix only: 'wss://api-dev.fugle.tw/marketdata'. "
            "The version comes from the `version` option, e.g. version={'futopt': 'v1.1'}."
        )

    def test_versioned_base_url_is_rejected_after_trailing_slashes_are_trimmed(self):
        client = WebSocketClient(api_key='api-key', base_url='wss://api-dev.fugle.tw/marketdata/v1.0//')
        with pytest.raises(TypeError) as excinfo:
            client.futopt
        assert "base_url must not include a version segment (found '/v1.0')" in str(excinfo.value)


class TestWebSocketClientRegressionTests:
    def test_default_behavior_without_base_url(self, api_key_client):
        # 回歸測試：確保不提供 base_url 時使用預設值
        stock = api_key_client.stock
        assert 'wss://api.fugle.tw/marketdata/v1.0/stock/streaming' in stock.url
        
        futopt = api_key_client.futopt
        assert 'wss://api.fugle.tw/marketdata/v1.1/futopt/streaming' in futopt.url

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
        client = WebSocketClient(api_key='test-key', base_url='wss://ws.example.com/marketdata')
        stock = client.stock
        assert stock.url == 'wss://ws.example.com/marketdata/v1.0/stock/streaming'

    def test_single_trailing_slash_base_url(self):
        # 測試單一結尾斜線的 base_url
        client = WebSocketClient(api_key='test-key', base_url='wss://ws.example.com/marketdata/')
        stock = client.stock
        assert stock.url == 'wss://ws.example.com/marketdata/v1.0/stock/streaming'

    def test_multiple_trailing_slashes_base_url(self):
        # 測試多個結尾斜線的 base_url
        client = WebSocketClient(api_key='test-key', base_url='wss://ws.example.com/marketdata///')
        stock = client.stock
        assert stock.url == 'wss://ws.example.com/marketdata/v1.0/stock/streaming'

    def test_non_version_path_segment_stays_part_of_the_prefix(self):
        # 測試 /api/v2 這種不是 vX.Y 的路徑段會原樣保留在 prefix 裡
        client = WebSocketClient(api_key='test-key', base_url='wss://ws.example.com/api/v2/')
        stock = client.stock
        assert stock.url == 'wss://ws.example.com/api/v2/v1.0/stock/streaming'
        futopt = client.futopt
        assert futopt.url == 'wss://ws.example.com/api/v2/v1.1/futopt/streaming'


def _build_health_client(max_missed_pongs=2, ping_interval=30000):
    """Build a core client with health check enabled, with the send and the
    disconnect side effects stubbed so the freshness logic can be unit-tested
    without a live socket."""
    health = HealthCheckConfig(
        enabled=True,
        ping_interval=ping_interval,
        max_missed_pongs=max_missed_pongs,
    )
    client = CoreWebSocketClient(
        url='wss://ws.example.com/stock/streaming',
        api_key='api-key',
        health_check=health,
    )

    sent = []
    # Stub the name-mangled private __send so ping() does not touch the socket.
    client._WebSocketClient__send = lambda message: sent.append(message)
    client._sent = sent

    closed = {'count': 0}

    def fake_disconnect():
        closed['count'] += 1
        if client.ping_timer is not None:
            client.ping_timer.cancel()
            client.ping_timer = None
        # Mimic real on_close emitting the disconnect event with the reason.
        reason = client._WebSocketClient__disconnect_reason
        client._WebSocketClient__disconnect_reason = None
        if reason is not None:
            client.ee.emit('disconnect', None, None, reason)
        else:
            client.ee.emit('disconnect', None, None)

    client.disconnect = fake_disconnect
    client._closed = closed
    return client


def _tick(client):
    """Run a single health-check tick synchronously."""
    client._WebSocketClient__health_check_tick()


class TestWebSocketHealthCheck:
    def test_config_defaults(self):
        cfg = HealthCheckConfig()
        assert cfg.enabled is False
        assert cfg.ping_interval == 30000
        assert cfg.max_missed_pongs == 2

    def test_tick_sends_ping_and_updates_last_ping_at(self):
        client = _build_health_client()
        client.last_message_at = time.monotonic()
        client.last_ping_at = client.last_message_at
        before = client.last_ping_at
        _tick(client)
        # A ping is sent and last_ping_at advances.
        assert any(m['event'] == 'ping' for m in client._sent)
        assert client.last_ping_at >= before
        assert client._closed['count'] == 0
        if client.ping_timer:
            client.ping_timer.cancel()

    def test_inbound_message_resets_freshness_no_disconnect(self):
        client = _build_health_client(max_missed_pongs=2)
        client.last_message_at = time.monotonic()
        client.last_ping_at = client.last_message_at

        for _ in range(5):
            _tick(client)
            if client.ping_timer:
                client.ping_timer.cancel()
                client.ping_timer = None
            # Simulate any inbound message arriving after the ping.
            client._WebSocketClient__on_message(
                None, b'{"event":"data","data":{}}'
            )

        assert client.consecutive_misses == 0
        assert client._closed['count'] == 0

    def test_consecutive_misses_accumulate_then_disconnect(self):
        client = _build_health_client(max_missed_pongs=2)
        client.last_message_at = time.monotonic()
        client.last_ping_at = client.last_message_at

        # First tick: fresh (seeded equal), sends ping, advances last_ping_at.
        _tick(client)
        if client.ping_timer:
            client.ping_timer.cancel()
            client.ping_timer = None
        assert client.consecutive_misses == 0

        # No inbound message arrives -> miss 1
        _tick(client)
        if client.ping_timer:
            client.ping_timer.cancel()
            client.ping_timer = None
        assert client.consecutive_misses == 1
        assert client._closed['count'] == 0

        # Still nothing -> miss 2 reaches max -> disconnect
        _tick(client)
        assert client._closed['count'] == 1

    def test_disconnect_event_has_timeout_reason_on_miss(self):
        client = _build_health_client(max_missed_pongs=1)
        received = {}

        def on_disconnect(*args):
            received['args'] = args

        client.on('disconnect', on_disconnect)

        # Seed so the connection is already stale relative to a future ping.
        client.last_ping_at = time.monotonic()
        client.last_message_at = client.last_ping_at - 1.0

        _tick(client)
        assert client._closed['count'] == 1
        # disconnect emitted with (code, msg, reason)
        assert received['args'][-1] == {"reason": "health-check-timeout"}

    def test_max_missed_pongs_zero_is_clamped_to_one(self):
        # max_missed_pongs=0 must not disconnect a healthy connection on the
        # first tick; it is clamped to a minimum of 1.
        client = _build_health_client(max_missed_pongs=0)
        client.last_message_at = time.monotonic()
        client.last_ping_at = client.last_message_at

        _tick(client)
        if client.ping_timer:
            client.ping_timer.cancel()
            client.ping_timer = None

        assert client._closed['count'] == 0

    def test_normal_disconnect_has_no_reason(self):
        # Use a real (un-stubbed) core client to check on_close threading.
        health = HealthCheckConfig(enabled=True)
        client = CoreWebSocketClient(
            url='wss://ws.example.com/stock/streaming',
            api_key='api-key',
            health_check=health,
        )
        received = {}
        client.on('disconnect', lambda *args: received.update(args=args))

        # No pending reason -> normal close, second-style arg absent.
        client._WebSocketClient__on_close(None, 1000, 'normal')
        assert received['args'] == (1000, 'normal')
        # Only two args: no reason payload.
        assert len(received['args']) == 2


class TestWebSocketClientConfigKeys:
    # `url` 本身由上面每一組 URL 測試涵蓋——它們都是讀 `.url` 斷言的。
    # 這裡釘住的是 factory 不會把自己的 `base_url` 語意漏進 client。
    def test_client_config_carries_the_endpoint_under_url_only(self):
        futopt = WebSocketClient(api_key='api-key', base_url='wss://ws.example.com/marketdata').futopt
        assert futopt.config['url'] == futopt.url
        # factory 的 `base_url` 是 host prefix，跟 client 的完整 endpoint 同名異義，
        # 所以不沿用——留著會是個看起來合理、意思卻不同的值。
        assert 'base_url' not in futopt.config
