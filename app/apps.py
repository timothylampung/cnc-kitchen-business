#  Copyright (c) 2021.
#  Volume Research & Development sdn. bhd.
#  Author : Timothy Lampung
#  Email : timothylampung@gmail.com
#  Contacts : +601165315133


from django.apps import AppConfig as Ac


class AppConfig(Ac):
    name = 'app'

    def ready(self):
       pass
