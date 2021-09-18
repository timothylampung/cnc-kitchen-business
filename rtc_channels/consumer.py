#  Copyright (c) 2021.
#  Volume Research & Development sdn. bhd.
#  Author : Timothy Lampung
#  Email : timothylampung@gmail.com
#  Contacts : +601165315133

import json
import uuid

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from app.models import Module
from business.machine_settings import MODULES
from rtc_channels.data import \
    MESSAGE_DATA, \
    REQUEST_PERMISSION_DATA, \
    GRANT_PERMISSION_DATA, \
    CAMERA_DATA, \
    CamOperation, ModuleControls
from stir_fry.core.wrapper.stir_fry_sdk import StirFrySDK


class MessageConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        self.instruction_uuid = uuid.uuid4()
        super().__init__(*args, **kwargs)

    def connect(self):
        module_name = self.scope['url_route']['kwargs']['module_name']
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
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
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
        if message['type'] == CamOperation.DATA:
            data = message['form']
            if data['class_name'] == 'Recipe':
                from app.models import Recipe
                recipe = Recipe.objects.get(pk=data['id'])
                recipe.cv_model_path = data['cv_model_path']
                recipe.number_of_class = data['number_of_class']
                recipe.save()
            elif data['class_name'] == 'Module':
                from app.models import Module
                module = Module.objects.get(pk=data['id'])
                module.camera_opened = data['camera_opened']
                module.save()

        data = CAMERA_DATA.copy()
        data["message"]["data"] = message
        self.send(text_data=json.dumps(data))

    def stream(self, event):
        message = event['message']
        data = CAMERA_DATA.copy()
        data["message"]["data"] = message
        self.send(text_data=json.dumps(data))

    def state(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))

    def module_controls(self, event):
        message = event['message']
        _id = message['module_id']
        module = Module.objects.get(pk=_id)
        _sdk: StirFrySDK = MODULES[Module.STIR_FRY_MODULE][module.name]['sdk']

        if self.instruction_uuid != message['instruction_uuid']:
            self.instruction_uuid = message['instruction_uuid']
            if message['instruction'] == ModuleControls.EMPTY:
                pass
            elif message['instruction'] == ModuleControls.ON_LED:
                _sdk.wrapper.on_light()
            elif message['instruction'] == ModuleControls.STOP_LED:
                _sdk.wrapper.off_light()
            elif message['instruction'] == ModuleControls.STOP_FAN:
                _sdk.wrapper.stop_cooling_fan()
            elif message['instruction'] == ModuleControls.START_FAN:
                _sdk.wrapper.start_cooling_fan()
            elif message['instruction'] == ModuleControls.STOP_HORIZONTAL:
                _sdk.wrapper.stop_horizontal()
            elif message['instruction'] == ModuleControls.ROTATE_HORIZONTAL:
                _sdk.wrapper.rotate_horizontal()
            elif message['instruction'] == ModuleControls.DEGREE_45:
                _sdk.wrapper.off_induction()
                _sdk.wrapper.set_vertical_0()
                _sdk.wrapper.set_vertical_45()
            elif message['instruction'] == ModuleControls.PLATE:
                print('plalting fucker')
                _sdk.wrapper.off_induction()
                _sdk.wrapper.set_vertical_0()
                _sdk.wrapper.set_vertical_plating()
            elif message['instruction'] == ModuleControls.RAISE:
                _sdk.wrapper.set_vertical_0()
            elif message['instruction'] == ModuleControls.CHANGE_TEMPERATURE:
                _sdk.change_temperature(message['value'])
