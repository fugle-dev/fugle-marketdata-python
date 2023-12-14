import asyncio
import json
import websocket
from pyee import EventEmitter
import sys

from ..constants import (
    CONNECT_EVENT,
    DISCONNECT_EVENT,
    MESSAGE_EVENT,
    ERROR_EVENT,
    AUTHENTICATED_EVENT,
    UNAUTHENTICATED_EVENT,
    UNAUTHENTICATED_MESSAGE
)


class WebSocketClient():
    def __init__(self, **config):
        self.config = config
        # config: base_url, api_key?, bearer_token?
        self.ee = EventEmitter()
        self.ee.on(CONNECT_EVENT, self.__authenticate)
        self.__ws = websocket.WebSocketApp(
            self.config.get('base_url'),
            on_open=self.__on_open,
            on_close=self.__on_close,
            on_error=self.__on_error,
            on_message=self.__on_message)
        self.loop = asyncio.get_event_loop()
        self.future = self.loop.create_future()

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
    
    def ping(self, params):
        message = {
            "event": "ping",
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
            self.loop.call_soon_threadsafe(self.future.set_result, 'success')
        elif message['event'] == ERROR_EVENT:
            if message['data'] and message['data']['message'] == UNAUTHENTICATED_MESSAGE:
                self.ee.emit(UNAUTHENTICATED_EVENT, message)
                self.loop.call_soon_threadsafe(
                    self.future.set_exception, 'login fail')

    def __on_error(self, ws, error):
        self.ee.emit(ERROR_EVENT, error)
        
    def on(self, event, listener):
        self.ee.on(event, listener)

    def off(self, event, listener):
        self.ee.off(event, listener)

    async def connect(self):
        self.loop.run_in_executor(None, self.__ws.run_forever)
        await self.future

    def disconnect(self):
        if self.__ws is not None:
            self.__ws.close()
