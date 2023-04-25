import asyncio
import json
import time
import websocket
from pyee import EventEmitter

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
            on_open=self.on_open,
            on_close=self.on_close,
            on_error=self.on_error,
            on_message=self.on_message)
        self.loop = asyncio.get_event_loop()
        self.future = self.loop.run_in_executor(None, self.__ws.run_forever)
        self.is_connected=False
        self.is_authed=False
        
    async def check_connected(self):
        while not self.is_connected:
            await asyncio.sleep(0.1)


    def subscribe(self, params):
        message = {
            "event": "subscribe",
            "data": params
        }
        self.__send(message)

    def __authenticate(self, ws):
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
            None # error

        self.__send(auth_info)

    def __send(self, message):
        print(message)
        self.__ws.send(json.dumps(message))

    def on_open(self, ws):
        self.ee.emit(CONNECT_EVENT, ws)
        self.is_connected=True

    def on_close(self, close_status_code, close_msg):
        self.ee.emit(DISCONNECT_EVENT, close_msg)

    def on_message(self, ws, data):
        message = json.loads(data)
        self.ee.emit(MESSAGE_EVENT, data)
        if message['event'] == AUTHENTICATED_EVENT:
            self.ee.emit(AUTHENTICATED_EVENT, message)
            self.is_authed=True
        elif message['event'] == ERROR_EVENT:
            if message['data'] and message['data']['message'] == UNAUTHENTICATED_MESSAGE:
                self.ee.emit(UNAUTHENTICATED_EVENT, message)
                self.future.cancel()
                self.loop.close()
       

    def on_error(self, ws, error):
        self.ee.emit("error", ws, error)

    def on(self, event, listener):
        self.ee.on(event, listener)

    def off(self, event, listener):
        self.ee.off(event, listener)

    async def connect(self):
        self.future = self.loop.run_in_executor(None, self.__ws.run_forever)
        return await self.check_connected()

    def disconnect(self):
        if self.__ws is not None:
            self.__ws.close()
