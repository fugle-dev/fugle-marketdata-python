import json
import websocket
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


class AuthenticationState:
    PENDING = 0
    AUTHENTICATING = 1
    AUTHENTICATED = 2
    UNAUTHENTICATED = 3


class WebSocketClient():
    def __init__(self, **config):
        self.config = config
        self.ee = EventEmitter()
        self.ee.on(CONNECT_EVENT, self.__authenticate)
        self.__ws = websocket.WebSocketApp(
            self.config.get('base_url'),
            on_open=self.__on_open,
            on_close=self.__on_close,
            on_error=self.__on_error,
            on_message=self.__on_message)

        self.auth_timer = None
        self.auth_status = AuthenticationState.PENDING
        self.error = None

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
        else:
            self.auth_status = AuthenticationState.UNAUTHENTICATED
            self.error = Exception(MISSING_CREDENTIALS_MESSAGE)

        self.__send(auth_info)
        self.auth_status = AuthenticationState.AUTHENTICATING
        self.auth_timer = Timer(5, self.check_auth_status)
        self.auth_timer.start()

    def __send(self, message):
        self.__ws.send(json.dumps(message))

    def __on_open(self, ws):
        self.ee.emit(CONNECT_EVENT)

    def __on_close(self, ws, close_status_code, close_msg):
        self.ee.emit(DISCONNECT_EVENT, close_status_code, close_msg)

    def __on_message(self, ws, data):
        message = json.loads(data)
        self.ee.emit(MESSAGE_EVENT, data)
        if message['event'] == AUTHENTICATED_EVENT:
            self.ee.emit(AUTHENTICATED_EVENT, message)
            self.auth_status = AuthenticationState.AUTHENTICATED
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
            self.auth_timer.cancel()
            self.auth_timer = None
            self.auth_status = AuthenticationState.PENDING
            self.error = None
