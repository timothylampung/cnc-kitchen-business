#  Copyright (c) 2021.
#  Volume Research & Development sdn. bhd.
#  Author : Timothy Lampung
#  Email : timothylampung@gmail.com
#  Contacts : +601165315133

import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from rtc_channels.data import MESSAGE_DATA, REQUEST_PERMISSION_DATA, GRANT_PERMISSION_DATA, CAMERA_DATA


class MessageConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def connect(self):
        module_name = self.scope['url_route']['kwargs']['module_name']
        print(module_name)
        async_to_sync(self.channel_layer.group_add)(
            module_name,
            self.channel_name
        )

        async_to_sync(self.channel_layer.group_send)(
            module_name, {
                'type': 'message',
                'message': {
                    'message': 'CONNECTED',
                    'handler_type': 'message'
                }
            }
        )

        self.accept()

    def disconnect(self, code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        module_name = self.scope['url_route']['kwargs']['module_name']
        print(text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)
        handler_type = message['handler_type']

        async_to_sync(self.channel_layer.group_send)(
            module_name, {
                'type': handler_type,
                'message': message['data']
            }
        )

    def message(self, event):
        message = event['message']
        data = MESSAGE_DATA.copy()
        data["message"]["data"] = message
        self.send(text_data=json.dumps(data))

    def request_permission(self, event):
        message = event['message']
        data = REQUEST_PERMISSION_DATA.copy()
        data["message"]["data"] = message
        self.send(text_data=json.dumps(data))

    def grant_permission(self, event):
        message = event['message']
        data = GRANT_PERMISSION_DATA.copy()
        data["message"]["data"] = message
        self.send(text_data=json.dumps(data))

    def camera(self, event):
        message = event['message']
        print(f'CAMERA MESSAGE {message}')
        data = CAMERA_DATA.copy()
        data["message"]["data"] = message
        self.send(text_data=json.dumps(data))

    def stream(self, event):
        message = event['message']
        print(f'CAMERA MESSAGE {message}')
        data = CAMERA_DATA.copy()
        data["message"]["data"] = message
        self.send(text_data=json.dumps(data))
