""" ASGI config for business project.
It exposes the ASGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/ """

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import threading
from rtc_channels.routing import websocket_patterns
import pyfiglet

ascii_banner = pyfiglet.figlet_format("VRND SDN. BHD.")


def prepare():
    from business.machine_settings import MODULES
    from stir_fry.core.wrapper.stir_fry_sdk import StirFrySDK
    from app.models import Module

    modules = Module.objects.all()
    tappers = []
    for module in modules:

        from utils.utils import ping
        if ping(module.ip_address):
            module.connectivity = Module.CONNECTED
        else:
            module.connectivity = Module.DISCONNECTED
        module.status = Module.AVAILABLE
        module.save()

        def check_state(_sdk: StirFrySDK):
            while True:
                _sdk.wrapper.get_temperature()

        if module.type == Module.STIR_FRY_MODULE:
            sdk = StirFrySDK(module.ip_address, module.name)
            # sdk.wrapper.start_cooling_fan()
            sdk.on_light()
            # sdk.wrapper.start_board_fan()
            sdk.wrapper.rotate_horizontal()
            sdk.wrapper.set_vertical_0()
            sdk.wrapper.set_vertical_washing()
            sdk.wrapper.set_vertical_0()
            MODULES[module.type][module.name] = {'sdk': sdk}
            t = threading.Thread(target=check_state, args=(sdk,))
            t.start()

        elif module.type == Module.TRANSPORTER_MODULE:
            from app.models import Coordinates
            home: Coordinates = Coordinates.objects.get(name='HOME')
            from transporter.core.wrapper.transporter_wrappers import TransporterSingleton
            transporter: TransporterSingleton = TransporterSingleton.get_instance()
            transporter.connect(module.ip_address)
            coordinate = Coordinates.objects.get(name='SOLID_1')
            requester = Coordinates.objects.get(pk=20)
            claim_id = transporter.claim_transporter()
            transporter.test_coordinate(coordinate, requester)

            coordinates = Coordinates.objects.filter(id__lte=16)
            shuffeled = []

            for coordinate in coordinates:
                print(coordinate.name)
                shuffeled.append(coordinate)

            for coordinate in coordinates:
                print(coordinate.name)
                shuffeled.append(coordinate)

            import random
            random.shuffle(shuffeled)

            for coordinate in shuffeled:
                if isinstance(coordinate, Coordinates):
                    caller = None
                    if coordinate.type == Coordinates.GRANULAR or coordinate.type == Coordinates.LIQUID:
                        caller = random.randint(18, 19)
                    elif coordinate.type == Coordinates.SOLID:
                        caller = random.randint(20, 21)
                    requester = Coordinates.objects.get(pk=caller)
                    print(f'ITS A {coordinate.type}')
                    transporter.test_coordinate(coordinate, requester)

            transporter.move_to_coordinate(home.linear, home.center, claim_id)
            transporter.release_transporter(claim_id)

            MODULES[module.type][module.name] = {
                'sdk': transporter,
            }


prepare()
# t = threading.Thread(targt=)
# t.start()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'business.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_patterns
        )
    )
})
