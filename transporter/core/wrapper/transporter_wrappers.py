#  Copyright (c) 2021.
#  Volume Research & Development sdn. bhd.
#  Author : Timothy Lampung
#  Email : timothylampung@gmail.com
#  Contacts : +601165315133

import time
import traceback

from comm.arduino.arduino_udp import ArduinoUdp, UpdPacket
from transporter.core.config.config import TTConf
from utils.utils import obj_to_json_string

locals_keys = list(locals().keys())


def pprint(*args, **kwargs):
    try:
        stack_tuple = traceback.extract_stack(limit=2)[0]
        print('[{}][{}]'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), stack_tuple[1]),
              end=' ')
    except:
        pass

    print(*args, **kwargs)


class TransporterSingletonException(Exception):

    def __init__(self, *args, **kwargs):  # real signature unknown
        pass


class TransporterSingleton:
    __instance = None

    MAX_GRANULAR_PLUNGER = 50000
    MAX_GRANULAR_TUBE = 70000
    MAX_SOLID_PLUNGER = 35000
    MAX_SOLID_TUBE = 70000
    MAX_LIQUID_PLUNGER = 50000
    MAX_LINEAR = 50000
    MAX_CENTER = 50000

    @staticmethod
    def get_instance():
        if TransporterSingleton.__instance is None:
            TransporterSingleton()
        return TransporterSingleton.__instance

    def __init__(self, ip='192.168.1.45'):
        if TransporterSingleton.__instance is not None:
            raise TransporterSingletonException("This class is singleton")
        else:
            TransporterSingleton.__instance = self
            self._ip = ip
            self.comm = ArduinoUdp(self._ip)
            self.busy = False
            self.claim_id = None

    from app.models import IngredientItem, Coordinates

    def handle_item(self, item: IngredientItem, requester):
        claim_id = self.claim_transporter()
        coordinate = item.ingredient_id.coordinate_id
        ingredient = item.ingredient_id
        print(f'MOVING TO {ingredient.coordinate_y}, {ingredient.coordinate_y}')
        self.move_to_coordinate(ingredient.coordinate_x, ingredient.coordinate_y, claim_id)
        from app.models import Coordinates
        dispense: Coordinates = Coordinates.objects.get(name=requester)
        self.move_to_coordinate(dispense.linear, dispense.center, claim_id)

        home: Coordinates = Coordinates.objects.get(name='HOME')

        self.move_to_coordinate(home.linear, home.center, claim_id)

        # """moving toward positions and sucking things up"""
        # if coordinate.type == Coordinates.SOLID:
        #     transporter.move_solid_tube(Ts.MAX_SOLID_TUBE, claim_id)
        #     transporter.move_solid_plunger(Ts.MAX_SOLID_PLUNGER, claim_id)
        #     transporter.on_solid_vacuum(claim_id)
        #     time.sleep(30)
        #     transporter.move_solid_plunger(item.quantity, claim_id)
        #     transporter.remove_solid_excess(claim_id)
        #
        # elif coordinate.type == Coordinates.LIQUID:
        #     transporter.move_granular_tube(Ts.MAX_GRANULAR_TUBE, claim_id)
        #     transporter.move_liquid_plunger(Ts.MAX_LIQUID_PLUNGER, claim_id)
        #     time.sleep(30)
        #     transporter.move_liquid_plunger(item.quantity, claim_id)
        #
        # elif coordinate.type == Coordinates.GRANULAR:
        #     transporter.move_granular_tube(Ts.MAX_GRANULAR_TUBE, claim_id)
        #     transporter.move_granular_plunger(Ts.MAX_GRANULAR_PLUNGER, claim_id)
        #     transporter.on_granular_vacuum(claim_id)
        #     time.sleep(30)
        #     transporter.move_granular_plunger(item.quantity, claim_id)
        # else:
        #     print('ingredient is LOL type')
        # transporter.move_granular_tube(0, claim_id)
        # transporter.move_solid_tube(0, claim_id)

        """moving toward positions and sucking things up"""

    def on_granular_blower(self, claim_id):
        ret = self.comm.send(self.__convert(TTConf.CODE.TOGGLE_GRANULAR_BLOWER, args1=1))
        return ret[0]

    def off_granular_blower(self, claim_id):
        ret = self.comm.send(self.__convert(TTConf.CODE.TOGGLE_GRANULAR_BLOWER, args1=0))
        return ret[0]

    def on_granular_vacuum(self, claim_id):
        ret = self.comm.send(self.__convert(TTConf.CODE.TOGGLE_GRANULAR_VACUUM, args1=1))
        return ret[0]

    def off_granular_vacuum(self, claim_id):
        ret = self.comm.send(self.__convert(TTConf.CODE.TOGGLE_GRANULAR_VACUUM, args1=0))
        return ret[0]

    def on_solid_blower(self, claim_id):
        ret = self.comm.send(self.__convert(TTConf.CODE.TOGGLE_SOLID_BLOWER, args1=1))
        return ret[0]

    def off_solid_blower(self, claim_id):
        ret = self.comm.send(self.__convert(TTConf.CODE.TOGGLE_SOLID_BLOWER, args1=0))
        return ret[0]

    def on_solid_vacuum(self, claim_id):
        ret = self.comm.send(self.__convert(TTConf.CODE.TOGGLE_SOLID_VACUUM, args1=1))
        return ret[0]

    def off_solid_vacuum(self, claim_id):
        ret = self.comm.send(self.__convert(TTConf.CODE.TOGGLE_SOLID_VACUUM, args1=0))
        return ret[0]

    def move_solid_tube(self, position, claim_id):
        if position > self.MAX_GRANULAR_TUBE or position < 0:
            print(f'invalid position : {position} is more than maximum position')
            position = self.MAX_GRANULAR_TUBE
        ret = self.comm.send(self.__convert(TTConf.CODE.MOVE_SOLID_TUBE, args1=position))
        return ret[0]

    def move_solid_plunger(self, position, claim_id):
        if position > self.MAX_SOLID_PLUNGER or position < 0:
            print(f'invalid position : {position} is more than maximum position')
            position = self.MAX_SOLID_PLUNGER
        ret = self.comm.send(self.__convert(TTConf.CODE.MOVE_SOLID_PLUNGER, args1=position))
        print(ret)
        return ret[0]

    def remove_solid_excess(self, claim_id):
        ret = self.comm.send(self.__convert(TTConf.CODE.MOVE_SOLID_PLUNGER, args1=-1))
        print(ret)
        return ret[0]

    def move_liquid_plunger(self, position, claim_id):
        if position > self.MAX_LIQUID_PLUNGER or position < 0:
            print(f'invalid position : {position} is more than maximum position')
            position = self.MAX_LIQUID_PLUNGER
        ret = self.comm.send(self.__convert(TTConf.CODE.MOVE_LIQUID_PLUNGER, args1=position))
        print(ret)
        return ret[0]

    def move_granular_tube(self, position, claim_id):
        if position > self.MAX_GRANULAR_TUBE or position < 0:
            print(f'invalid position : {position} is more than maximum position')
            position = self.MAX_GRANULAR_TUBE
        ret = self.comm.send(self.__convert(TTConf.CODE.MOVE_GRANULAR_TUBE, args1=position))
        print(ret)
        return ret[0]

    def move_granular_plunger(self, position, claim_id):
        if position > self.MAX_GRANULAR_PLUNGER or position < 0:
            print(f'invalid position : {position} is more than maximum position')
            position = self.MAX_GRANULAR_PLUNGER
        ret = self.comm.send(self.__convert(TTConf.CODE.MOVE_GRANULAR_PLUNGER,
                                            args1=position))
        print(ret)
        return ret[0]

    def move_to_coordinate(self, linear, center, claim_id):
        # self.move_granular_tube(0, claim_id)
        # self.move_solid_tube(0, claim_id)
        # self.off_granular_vacuum(claim_id)
        # self.off_granular_blower(claim_id)
        # self.off_solid_blower(claim_id)
        # self.off_solid_vacuum(claim_id)
        ret = self.comm.send(self.__convert(TTConf.CODE.MOVE_TO_COORDINATE,
                                            args1=linear,
                                            args2=center))
        print(ret)
        return ret[0]

    def claim_transporter(self):
        self.busy = True
        import uuid
        self.claim_id = uuid.uuid4()
        return self.claim_id

    def release_transporter(self, claim_id):
        self.busy = False

    def is_busy(self):
        return self.busy

    def can_use(self, claim_id):
        if self.claim_id != claim_id:
            return False
        else:
            if self.is_busy():
                return False
            else:
                return True

    @staticmethod
    def __convert(instruction, position=0, args1=0, args2=0):
        ret = obj_to_json_string(UpdPacket(instruction['code'],
                                           position=position,
                                           args1=args1,
                                           args2=args2))
        return ret
