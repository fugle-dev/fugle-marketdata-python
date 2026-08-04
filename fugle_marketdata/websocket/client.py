import time
import orjson
import websocket
from typing import Optional
from pyee import EventEmitter
from threading import Thread, Timer

from ..constants import (
    AUTHENTICATION_TIMEOUT_MESSAGE,
    CONNECT_EVENT,
    DISCONNECT_EVENT,
    MESSAGE_EVENT,
    ERROR_EVENT,
    AUTHENTICATED_EVENT,
    MISSING_CREDENTIALS_MESSAGE,
    UNAUTHENTICATED_EVENT,
    UNAUTHENTICATED_MESSAGE
)

websocket.setdefaulttimeout(5)


class HealthCheckConfig:
    def __init__(self, enabled: bool = False, ping_interval: int = 30000, max_missed_pongs: int = 2):
        self.enabled = enabled
        self.ping_interval = ping_interval
        self.max_missed_pongs = max_missed_pongs


class AuthenticationState:
    PENDING = 0
    AUTHENTICATING = 1
    AUTHENTICATED = 2
    UNAUTHENTICATED = 3


class WebSocketClient():
    def __init__(self, **config):
        self.config = config
        self.health_check: Optional[HealthCheckConfig] = config.get('health_check')
        self.ee = EventEmitter()
        self.ee.on(CONNECT_EVENT, self.__authenticate)
        self.__ws = websocket.WebSocketApp(
            self.url,
            on_open=self.__on_open,
            on_close=self.__on_close,
            on_error=self.__on_error,
            on_message=self.__on_message)

        self.auth_timer = None
        self.auth_status = AuthenticationState.PENDING
        self.error = None

        # Health check properties
        self.ping_timer = None
        self.consecutive_misses = 0
        self.last_message_at = 0.0
        self.last_ping_at = 0.0
        self.__disconnect_reason = None

    @property
    def url(self):
        """The endpoint this client connects to, fully resolved — host, version
        segment, product and `/streaming`.

        The version segment is chosen by the SDK from the `version` option
        rather than written by the caller, so this is the only way to see which
        version a client actually ended up on.
        """
        return self.config['url']

    def ping(self, message):
        message = {
            "event": "ping",
            "data": {
                "state": message
            }
        }
        self.__send(message)

    def subscribe(self, params):
        message = {
            "event": "subscribe",
            "data": params
        }
        self.__send(message)

    def unsubscribe(self, params):
        message = {
            "event": "unsubscribe",
            "data": params
        }
        self.__send(message)

    def subscriptions(self):
        message = {
            "event": "subscriptions"
        }
        self.__send(message)

    def __authenticate(self):
        if self.config.get('api_key'):
            auth_info = {
                'event': 'auth',
                'data': {
                    'apikey': self.config['api_key']
                }
            }
        elif self.config.get('bearer_token'):
            auth_info = {
                'event': 'auth',
                'data': {
                    'token': self.config['bearer_token']
                }
            }
        elif self.config.get('sdk_token'):
            auth_info = {
                'event': 'auth',
                'data': {
                    'sdkToken': self.config['sdk_token']
                }
            }
        else:
            self.auth_status = AuthenticationState.UNAUTHENTICATED
            self.error = Exception(MISSING_CREDENTIALS_MESSAGE)

        self.__send(auth_info)
        self.auth_status = AuthenticationState.AUTHENTICATING
        self.auth_timer = Timer(5, self.check_auth_status)
        self.auth_timer.start()

    def __send(self, message):
        self.__ws.send(orjson.dumps(message).decode('utf-8'))

    def __on_open(self, ws):
        self.ee.emit(CONNECT_EVENT)

    def __on_close(self, ws, close_status_code, close_msg):
        reason = self.__disconnect_reason
        self.__disconnect_reason = None
        if reason is not None:
            self.ee.emit(DISCONNECT_EVENT, close_status_code, close_msg, reason)
        else:
            self.ee.emit(DISCONNECT_EVENT, close_status_code, close_msg)

    def __on_message(self, ws, data):
        # Any inbound message counts as freshness.
        self.last_message_at = time.monotonic()
        message = orjson.loads(data)
        self.ee.emit(MESSAGE_EVENT, data)
        if message['event'] == AUTHENTICATED_EVENT:
            self.ee.emit(AUTHENTICATED_EVENT, message)
            self.auth_status = AuthenticationState.AUTHENTICATED

            # Start health check if enabled
            if self.health_check and self.health_check.enabled:
                self.__start_health_check()
        elif message['event'] == ERROR_EVENT:
            if message['data'] and message['data']['message'] == UNAUTHENTICATED_MESSAGE:
                self.ee.emit(UNAUTHENTICATED_EVENT, message)
                self.auth_status = AuthenticationState.UNAUTHENTICATED
                self.error = Exception(UNAUTHENTICATED_MESSAGE)

    def __on_error(self, ws, error):
        self.ee.emit(ERROR_EVENT, error)

    def on(self, event, listener):
        self.ee.on(event, listener)

    def off(self, event, listener):
        self.ee.off(event, listener)

    def check_auth_status(self):
        if self.auth_status == AuthenticationState.AUTHENTICATING:
            self.auth_status = AuthenticationState.UNAUTHENTICATED
            self.error = Exception(AUTHENTICATION_TIMEOUT_MESSAGE)

    def __start_health_check(self):
        """Start the freshness-based health check ping/pong mechanism"""
        if self.health_check and self.health_check.enabled:
            self.consecutive_misses = 0
            # Seed timestamps so the first tick treats the connection as fresh.
            now = time.monotonic()
            self.last_message_at = now
            self.last_ping_at = now
            self.__schedule_next_ping()

    def __schedule_next_ping(self):
        if not self.health_check or not self.health_check.enabled:
            return
        interval_seconds = self.health_check.ping_interval / 1000.0
        self.ping_timer = Timer(interval_seconds, self.__health_check_tick)
        self.ping_timer.daemon = True
        self.ping_timer.start()

    def __health_check_tick(self):
        """Run one freshness check, then send a ping and reschedule."""
        if not self.health_check or not self.health_check.enabled:
            return

        # Freshness check: did anything arrive since our last ping?
        if self.last_message_at < self.last_ping_at:
            self.consecutive_misses += 1
        else:
            self.consecutive_misses = 0

        # Clamp to >= 1: max_missed_pongs of 0 would disconnect a healthy
        # connection on the first tick (consecutive_misses starts at 0).
        max_missed = max(1, self.health_check.max_missed_pongs)
        if self.consecutive_misses >= max_missed:
            self.__disconnect_reason = {"reason": "health-check-timeout"}
            self.disconnect()
            return

        try:
            self.ping("")
            self.last_ping_at = time.monotonic()
            self.__schedule_next_ping()
        except Exception as error:
            print(f"Failed to send ping: {error}")
            self.__disconnect_reason = {"reason": "health-check-timeout"}
            self.disconnect()

    def connect(self):
        Thread(target=self.__ws.run_forever).start()
        while True:
            if self.auth_status in [AuthenticationState.AUTHENTICATED, AuthenticationState.UNAUTHENTICATED]:
                break
        if self.error is not None:
            self.__ws.close()
            self.auth_timer.cancel()
            raise self.error

    def disconnect(self):
        if self.__ws is not None:
            self.__ws.close()

        if self.auth_timer is not None:
            self.auth_timer.cancel()
            self.auth_timer = None

        if self.ping_timer is not None:
            self.ping_timer.cancel()
            self.ping_timer = None

        self.auth_status = AuthenticationState.PENDING
        self.error = None
