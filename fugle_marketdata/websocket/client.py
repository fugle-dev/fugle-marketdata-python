import time
import json
import websocket
from pyee import EventEmitter
from threading import Thread, Timer
from typing import Generic, TypeVar

from ..constants import (
    AUTHENTICATION_TIMEOUT_MESSAGE,
    CONNECT_EVENT,
    DISCONNECT_EVENT,
    MESSAGE_EVENT,
    ERROR_EVENT,
    AUTHENTICATED_EVENT,
    UNAUTHENTICATED_EVENT,
    UNAUTHENTICATED_MESSAGE
)

T = TypeVar('T')
E = TypeVar('E')


class Ok(Generic[T]):
    def __init__(self, value: T):
        self.value = value

    def is_ok(self):
        return True

    def is_err(self):
        return False

    def __repr__(self):
        return f"Ok({repr(self.value)})"


class Err(Generic[E]):
    def __init__(self, error: E):
        self.error = error

    def is_ok(self):
        return False

    def is_err(self):
        return True

    def __repr__(self):
        return f"Err({repr(self.error)})"


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

        self.auth_result = None

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
            None  # error

        self.__send(auth_info)

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
            self.auth_result = Ok("success")
        elif message['event'] == ERROR_EVENT:
            if message['data'] and message['data']['message'] == UNAUTHENTICATED_MESSAGE:
                self.ee.emit(UNAUTHENTICATED_EVENT, message)
                self.auth_result = Err(UNAUTHENTICATED_MESSAGE)

    def __on_error(self, ws, error):
        self.ee.emit(ERROR_EVENT, error)

    def on(self, event, listener):
        self.ee.on(event, listener)

    def off(self, event, listener):
        self.ee.off(event, listener)

    def connect(self):
        Thread(target=self.__ws.run_forever).start()
        auth_timer = 0
        while True:
            if auth_timer > 5000:
                self.auth_result = Err(AUTHENTICATION_TIMEOUT_MESSAGE)
            auth_timer += 50
            time.sleep(50/1000)
            if self.auth_result is not None:
                break

        if self.auth_result.is_ok():
            return ""
        elif self.auth_result.is_err():
            raise Exception(self.auth_result.error)

    def disconnect(self):
        if self.__ws is not None:
            self.__ws.close()
            self.auth_result = None
