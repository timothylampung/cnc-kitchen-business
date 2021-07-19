#  Copyright (c) 2021.
#  Volume Research & Development sdn. bhd.
#  Author : Timothy Lampung
#  Email : timothylampung@gmail.com
#  Contacts : +601165315133

from django.urls import re_path

from rtc_channels.consumer import MessageConsumer

websocket_patterns = [
    re_path(r'ws/message/(?P<module_name>\w+)/$', MessageConsumer.as_asgi())
]
