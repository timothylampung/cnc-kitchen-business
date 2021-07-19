#  Copyright (c) 2021.
#  Volume Research & Development sdn. bhd.
#  Author : Timothy Lampung
#  Email : timothylampung@gmail.com
#  Contacts : +601165315133

from django.apps import AppConfig as Ac

from utils.utils import ping


class AppConfig(Ac):
    name = 'app'

    def prepare(self):
        from transporter.core.wrapper.transporter_wrappers import TransporterSingleton
        from app.models import Coordinates

        home: Coordinates = Coordinates.objects.get(name="HOME")
        claim_id = '#4521349#$(*&!@4-03'
        t = TransporterSingleton.get_instance()
        # coordinates = Coordinates.objects.all()
        # for coordinate in coordinates:
        #     if isinstance(coordinate, Coordinates):
        #         t.move_to_coordinate(coordinate.linear, coordinate.center, claim_id)
        # t.move_to_coordinate(home.linear, home.center, claim_id)

    def ready(self):
        print("initializing")
        from stir_fry.core.wrapper.states import ModuleStateFactory
        from business.machine_settings import MODULES
        from stir_fry.core.wrapper.stir_fry_sdk import StirFrySDK
        from stir_fry.core.wrapper.states import ModuleState

        state_factory = ModuleStateFactory()
        from app.models import Module
        for module in Module.objects.all():
            if ping(module.ip_address):
                module.connectivity = Module.CONNECTED
            else:
                module.connectivity = Module.DISCONNECTED

            module.status = Module.AVAILABLE
            module.save()
            MODULES[module.type][module.name] = {
                'sdk': StirFrySDK(module.ip_address, module.name),
                'state': ModuleState(module.name, by_pass_arm=False)
            }
            state_factory.register(module, by_pass_arm=False)

        print(MODULES)
        from transporter.core.wrapper.transporter_wrappers import TransporterSingleton
