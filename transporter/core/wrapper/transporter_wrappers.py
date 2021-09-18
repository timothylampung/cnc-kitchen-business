#  Copyright (c) 2021.
#  Volume Research & Development sdn. bhd.
#  Author : Timothy Lampung
#  Email : timothylampung@gmail.com
#  Contacts : +601165315133

import time
import traceback
from comm.arduino.arduino_udp import ArduinoUdp, UpdPacket
from transporter.core.config.config import TTConf
from transporter.core.wrapper.states import TransporterState
from utils.utils import obj_to_json_string

locals_keys = list(locals().keys())


def pprint(*args, **kwargs):
    try:
        stack_tuple = traceback.extract_stack(limit=2)[0]
        print('[{}][{}]'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), stack_tuple[1]),
              end=' ')
    except Exception:
        pass


class TransporterSingletonException(Exception):

    def __init__(self, *args, **kwargs):  # real signature unknown
        pass


class TransporterSingleton:
    __instance = None

    MAX_GRANULAR_PLUNGER = 35000
    MAX_GRANULAR_TUBE = 80000
    MAX_SOLID_PLUNGER = 35000
    MAX_SOLID_TUBE = 50000
    MAX_LIQUID_PLUNGER = 50000
    MAX_LINEAR = 50000
    MAX_CENTER = 50000

    @staticmethod
    def get_instance():
        if TransporterSingleton.__instance is None:
            TransporterSingleton()
        return TransporterSingleton.__instance

    def __init__(self):
        if TransporterSingleton.__instance is not None:
            raise TransporterSingletonException("This class is singleton")
        else:
            TransporterSingleton.__instance = self
            self.comm = None
            self.busy = False
            self.claim_id = None
            self.state = TransporterState()

    def connect(self, ip):
        if self.comm is None:
            self.comm = ArduinoUdp(ip)
        else:
            pass

    def test_coordinate(self, coordinate, requester):
        from app.models import Coordinates

        if isinstance(coordinate, Coordinates) and isinstance(requester, Coordinates):
            print('testing')
            while self.busy:
                pass

            print('running')
            self.busy = True
            claim_id = self.claim_transporter()
            self.move_to_coordinate(coordinate.linear, coordinate.center, claim_id)
            # for i in range(2):
            #     print(i)
            #     time.sleep(1)
            #
            # # move effectors
            # if coordinate.type == Coordinates.LIQUID:
            #     self.move_liquid_plunger(0, claim_id)
            #     # self.move_granular_tube(TransporterSingleton.MAX_GRANULAR_TUBE, claim_id)
            #     # self.move_liquid_plunger(self.MAX_LIQUID_PLUNGER, claim_id)
            #     self.move_granular_tube(0, claim_id)
            #
            # #     @todo: TIMOTHY remove excess according to volume
            # elif coordinate.type == Coordinates.GRANULAR:
            #     self.on_granular_vacuum(claim_id)
            #     # self.move_granular_tube(TransporterSingleton.MAX_GRANULAR_TUBE, claim_id)
            #     # self.move_granular_plunger(TransporterSingleton.MAX_GRANULAR_PLUNGER, claim_id)
            #     time.sleep(4)
            #     self.off_granular_vacuum(claim_id)
            #     self.move_granular_tube(0, claim_id)
            #
            # #     @todo: TIMOTHY remove excess according to volume
            # elif coordinate.type == Coordinates.SOLID:
            #     # self.move_solid_plunger(TransporterSingleton.MAX_SOLID_PLUNGER, claim_id)
            #     self.on_solid_vacuum(claim_id)
            #     # self.move_solid_tube(TransporterSingleton.MAX_SOLID_TUBE, claim_id)
            #     time.sleep(4)
            #     self.off_solid_vacuum(claim_id)
            #     self.on_solid_blower(claim_id)
            #     self.remove_solid_excess(claim_id)
            #     self.off_solid_blower(claim_id)
            #     self.move_solid_tube(0, claim_id)

            #     @todo: TIMOTHY remove excess according to volume
            # move to dispense
            from app.models import Coordinates
            self.move_to_coordinate(requester.linear, requester.center, claim_id)

            # # dispense
            # if coordinate.type == Coordinates.LIQUID:
            #     self.move_granular_tube(TransporterSingleton.MAX_GRANULAR_TUBE, claim_id)
            #     self.move_liquid_plunger(0, claim_id)
            #     self.move_granular_tube(0, claim_id)
            #
            # elif coordinate.type == Coordinates.GRANULAR:
            #     self.on_granular_blower(claim_id)
            #     self.move_granular_tube(TransporterSingleton.MAX_GRANULAR_TUBE, claim_id)
            #     self.move_granular_plunger(0, claim_id)
            #     self.move_granular_tube(0, claim_id)
            #     self.off_granular_blower(claim_id)
            #
            #
            # elif coordinate.type == Coordinates.SOLID:
            #     self.move_solid_tube(TransporterSingleton.MAX_SOLID_TUBE, claim_id)
            #     self.on_solid_blower(claim_id)
            #     self.move_solid_plunger(1, claim_id)
            #     self.off_solid_blower(claim_id)
            #     self.move_solid_tube(0, claim_id)
            #     self.move_solid_plunger(0, claim_id)

            home: Coordinates = Coordinates.objects.get(name='HOME')
            self.move_to_coordinate(home.linear, home.center, claim_id)

            self.busy = False

    def handle_item(self, item, requester):
        from app.models import IngredientItem, Coordinates as C
        if isinstance(item, IngredientItem):

            while self.busy:
                pass

            self.busy = True
            claim_id = self.claim_transporter()
            coordinate = item.ingredient_id.coordinate_id
            ingredient = item.ingredient_id
            self.move_to_coordinate(ingredient.coordinate_x, ingredient.coordinate_y, claim_id)

            # move effectors
            if coordinate.type == C.LIQUID:
                self.move_liquid_plunger(0, self.claim_id)
                self.move_liquid_plunger(self.MAX_LIQUID_PLUNGER, self.claim_id)
            #     @todo: TIMOTHY remove excess according to volume
            elif coordinate.type == C.GRANULAR:
                self.move_granular_tube(self.MAX_GRANULAR_TUBE, self.claim_id)
                self.move_granular_plunger(self.MAX_GRANULAR_PLUNGER, self.claim_id)
                self.on_granular_vacuum(self.claim_id)
            #     @todo: TIMOTHY remove excess according to volume
            elif coordinate.type == C.SOLID:
                self.move_solid_tube(self.MAX_SOLID_TUBE, self.claim_id)
                self.move_solid_plunger(self.MAX_SOLID_PLUNGER, self.claim_id)
                self.on_solid_vacuum(self.claim_id)
            #     @todo: TIMOTHY remove excess according to volume
            # move to dispense
            from app.models import Coordinates
            dispense: Coordinates = Coordinates.objects.get(name=requester)
            self.move_to_coordinate(dispense.linear, dispense.center, claim_id)
            # dispense
            if coordinate.type == C.LIQUID:
                pass
            elif coordinate.type == C.GRANULAR:
                self.move_granular_tube(self.MAX_GRANULAR_TUBE, self.claim_id)

            elif coordinate.type == C.SOLID:
                pass

            home: Coordinates = Coordinates.objects.get(name='HOME')

            self.move_to_coordinate(home.linear, home.center, claim_id)

            # move effectors
            if coordinate.type == C.LIQUID:
                pass
            elif coordinate.type == C.GRANULAR:
                self.move_granular_tube(self.MAX_GRANULAR_TUBE, self.claim_id)
            elif coordinate.type == C.SOLID:
                pass
            self.busy = False

    def on_granular_blower(self, claim_id):
        ret = self.comm.send(self.__convert(TTConf.CODE.GRANULAR_ESC, args1=30, args2=0))
        return ret[0]

    def off_granular_blower(self, claim_id):
        ret = self.comm.send(self.__convert(TTConf.CODE.GRANULAR_ESC, args1=0, args2=0))
        return ret[0]

    def on_granular_vacuum(self, claim_id):
        ret = self.comm.send(self.__convert(TTConf.CODE.GRANULAR_ESC, args1=255, args2=1))
        return ret[0]

    def off_granular_vacuum(self, claim_id):
        ret = self.comm.send(self.__convert(TTConf.CODE.GRANULAR_ESC, args1=0, args2=1))
        return ret[0]

    def on_solid_blower(self, claim_id):
        ret = self.comm.send(self.__convert(TTConf.CODE.SOLID_ESC, args1=30, args2=1))
        return ret[0]

    def off_solid_blower(self, claim_id):
        ret = self.comm.send(self.__convert(TTConf.CODE.SOLID_ESC, args1=0, args2=0))
        return ret[0]

    def on_solid_vacuum(self, claim_id):
        ret = self.comm.send(self.__convert(TTConf.CODE.SOLID_ESC, args1=255, args2=0))
        return ret[0]

    def off_solid_vacuum(self, claim_id):
        ret = self.comm.send(self.__convert(TTConf.CODE.SOLID_ESC, args1=0, args2=0))
        return ret[0]

    def move_solid_tube(self, position, claim_id):
        if position > self.MAX_GRANULAR_TUBE or position < 0:
            position = self.MAX_GRANULAR_TUBE
        ret = self.comm.send(self.__convert(TTConf.CODE.MOVE_SOLID_TUBE, args1=position))
        return ret[0]

    def move_solid_plunger(self, position, claim_id):
        if position > self.MAX_SOLID_PLUNGER or position < 0:
            position = self.MAX_SOLID_PLUNGER
        ret = self.comm.send(self.__convert(TTConf.CODE.MOVE_SOLID_PLUNGER, args1=position))
        return ret[0]

    def remove_solid_excess(self, claim_id):
        ret = self.comm.send(self.__convert(TTConf.CODE.MOVE_SOLID_PLUNGER, args1=-1))
        return ret[0]

    def move_liquid_plunger(self, position, claim_id):
        if position > self.MAX_LIQUID_PLUNGER or position < 0:
            position = self.MAX_LIQUID_PLUNGER
        ret = self.comm.send(self.__convert(TTConf.CODE.MOVE_LIQUID_PLUNGER, args1=position))
        return ret[0]

    def move_granular_tube(self, position, claim_id):
        if position > self.MAX_GRANULAR_TUBE or position < 0:
            position = self.MAX_GRANULAR_TUBE
        ret = self.comm.send(self.__convert(TTConf.CODE.MOVE_GRANULAR_TUBE, args1=position))
        return ret[0]

    def move_granular_plunger(self, position, claim_id):
        if position > self.MAX_GRANULAR_PLUNGER or position < 0:
            position = self.MAX_GRANULAR_PLUNGER
        ret = self.comm.send(self.__convert(TTConf.CODE.MOVE_GRANULAR_PLUNGER,
                                            args1=position))
        return ret[0]

    def move_to_coordinate(self, linear, center, claim_id):
        ret = self.comm.send(self.__convert(TTConf.CODE.MOVE_TO_COORDINATE,
                                            args1=linear,
                                            args2=center))
        return ret[0]

    def claim_transporter(self):
        import uuid
        self.claim_id = uuid.uuid4()
        return self.claim_id

    def release_transporter(self, claim_id):
        self.busy = False
        self.claim_id = None

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
