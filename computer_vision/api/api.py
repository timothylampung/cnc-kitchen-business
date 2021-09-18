#  Copyright (c) 2021.
#  Volume Research & Development sdn. bhd.
#  Author : Timothy Lampung
#  Email : timothylampung@gmail.com
#  Contacts : +601165315133
from django.conf.urls import url
from computer_vision.api.views import CameraAPI


urlpatterns = [
    url(r'^open_camera/(?P<module_id>\d+)/$', CameraAPI.as_view(), name='camera access'),
]
