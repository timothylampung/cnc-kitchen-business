#  Copyright (c) 2021.
#  Volume Research & Development sdn. bhd.
#  Author : Timothy Lampung
#  Email : timothylampung@gmail.com
#  Contacts : 01165315133
import threading
import time

from comm.arduino.arduino_udp import ArduinoUdp, UpdPacket
from stir_fry.core.config.codes import ArduinoResponseCode as ARC
from stir_fry.core.wrapper.states import ModuleState
from utils.utils import obj_to_json_string
from stir_fry.core.config.config import SFConf


class StirFryWrapper:

    def __init__(self, ip, module_name, state: ModuleState):
        self._has_error = False
        self._has_warn = False
        self._state_is_ready = False
        self._error_code = 0
        self._warn_code = 0
        self._cmd_num = 0
        self._debug = False
        self._current_state = None
        self._ip = ip
        self.state = state
        self.comm = ArduinoUdp(self._ip)
        self.module_name = module_name
        self.is_far = False

    def get_states(self):
        self._current_state = SFConf.CODE.GET_TEMPERATURE['name']
        ret = self.comm.send(self.__convert(SFConf.CODE.GET_TEMPERATURE))
        return ret

    def get_temperature(self):
        self._current_state = SFConf.CODE.GET_TEMPERATURE['name']
        temp = self.comm.send(self.__convert(SFConf.CODE.GET_TEMPERATURE))
        t = 400
        try:
            t = temp[0]["average_temps"]
            self.state.temperature = t
            self.state.event_trigger()
            """update the states factory"""
            return t
        except Exception as e:
            self.state.temperature = t
            self.state.event_trigger()
            return t

    def set_vertical_0(self):
        self._current_state = SFConf.CODE.ZERO_VERTICAL['name']
        self.state.vertical_status = ModuleState.RUNNING
        self.state.event_trigger()
        """update the states factory"""
        ret = self.comm.send(self.__convert(SFConf.CODE.ZERO_VERTICAL))
        if ret[0]['function'] != ARC.PING_VERTICAL_SUCCESS:
            self._has_error = True
            raise RuntimeError()
        self.state.vertical_status = ModuleState.AVAILABLE
        self.state.event_trigger()
        """update the states factory"""
        self.is_far = False
        return ret

    def set_vertical_45(self):

        """update the states factory"""""
        self.is_far = True
        self._current_state = SFConf.CODE.VERTICAL_HOLD_45['name']
        self.state.vertical_status = ModuleState.BUSY
        self.state.event_trigger()
        ret = self.comm.send(self.__convert(SFConf.CODE.VERTICAL_HOLD_45))
        if ret[0]['function'] != ARC.PING_VERTICAL_SUCCESS:
            self._has_error = True
            raise RuntimeError()
        self.state.vertical_status = ModuleState.AVAILABLE
        self.state.event_trigger()

        """update the states factory"""""

        return ret

    def set_vertical_plating(self):

        self.is_far = True
        self._current_state = SFConf.CODE.PLATE_VERTICAL['name']
        self.state.vertical_status = ModuleState.BUSY
        self.state.event_trigger()
        """update the states factory"""""
        ret = self.comm.send(self.__convert(SFConf.CODE.PLATE_VERTICAL))

        if ret[0]['function'] != ARC.PING_VERTICAL_SUCCESS:
            self._has_error = True
            raise RuntimeError()

        """update the states factory"""""
        self.state.vertical_status = ModuleState.AVAILABLE
        self.state.event_trigger()

        return ret

    def set_vertical_picking(self):

        self._current_state = SFConf.CODE.VERTICAL_FOR_PICKING['name']
        self.state.vertical_status = ModuleState.BUSY
        self.state.event_trigger()

        """update the states factory"""""
        ret = self.comm.send(self.__convert(SFConf.CODE.VERTICAL_FOR_PICKING))

        if ret[0]['function'] != ARC.PING_VERTICAL_SUCCESS:
            self._has_error = True
            raise RuntimeError()

        """update the states factory"""""
        self.state.vertical_status = ModuleState.AVAILABLE
        self.state.event_trigger()

        return ret

    def set_vertical_washing(self):

        self._current_state = SFConf.CODE.VERTICAL_FOR_WASHING['name']
        self.state.vertical_status = ModuleState.BUSY
        self.state.event_trigger()

        """update the states factory"""""
        ret = self.comm.send(self.__convert(SFConf.CODE.VERTICAL_FOR_WASHING))

        if ret[0]['function'] != ARC.PING_VERTICAL_SUCCESS:
            self._has_error = True
            raise RuntimeError()

        """update the states factory"""""
        self.state.vertical_status = ModuleState.AVAILABLE
        self.state.event_trigger()

        return ret

    def rotate_horizontal(self):

        """update the states factory"""""
        self.state.horizontal_status = ModuleState.BUSY

        self.state.event_trigger()
        self._current_state = SFConf.CODE.ROTATE_HORIZONTAL_MOTOR['name']
        ret = self.comm.send(self.__convert(SFConf.CODE.ROTATE_HORIZONTAL_MOTOR))

        if ret[0]['function'] != ARC.PING_HORIZONTAL_SUCCESS:
            self._has_error = True
            raise RuntimeError()
        return ret

    def shake_horizontal(self):

        """update the states factory"""""
        self.state.horizontal_status = ModuleState.BUSY
        self.state.event_trigger()
        self._current_state = SFConf.CODE.SHAKE_HORIZONTAL['name']
        ret = self.comm.send(self.__convert(SFConf.CODE.SHAKE_HORIZONTAL))

        if ret[0]['function'] != ARC.PING_HORIZONTAL_SUCCESS:
            self._has_error = True
            raise RuntimeError()
        return ret

    def stop_horizontal(self):
        self.state.horizontal_status = ModuleState.AVAILABLE
        self.state.event_trigger()
        self._current_state = SFConf.CODE.STOP_HORIZONTAL_MOTOR['name']
        ret = self.comm.send(self.__convert(SFConf.CODE.STOP_HORIZONTAL_MOTOR))

        if ret[0]['function'] != ARC.PING_HORIZONTAL_SUCCESS:
            self._has_error = True
            raise RuntimeError()

        """update the states factory"""""

        return ret

    def open_oil_valve(self):
        self.state.oil_pump_status = ModuleState.RUNNING
        self.state.event_trigger()
        self._current_state = SFConf.CODE.OPEN_OIL_VALVE['name']
        ret = self.comm.send(self.__convert(SFConf.CODE.OPEN_OIL_VALVE))
        if ret[0]['function'] != ARC.OPEN_OIL_VALVE_SUCCESS:
            self._has_error = True
            raise RuntimeError()

        """update the states factory"""""

        return ret

    def close_oil_valve(self):

        self.state.oil_pump_status = ModuleState.IDLE
        self.state.event_trigger()
        self._current_state = SFConf.CODE.OPEN_OIL_VALVE['name']
        ret = self.comm.send(self.__convert(SFConf.CODE.CLOSE_OIL_VALVE))

        if ret[0]['function'] != ARC.CLOSE_OIL_VALVE_SUCCESS:
            self._has_error = True
            raise RuntimeError()

        """update the states factory"""""

        return ret

    def start_board_fan(self):
        self.state.water_pump_status = ModuleState.RUNNING
        self.state.event_trigger()
        self._current_state = SFConf.CODE.OPEN_WATER_VALVE['name']
        ret = self.comm.send(self.__convert(SFConf.CODE.OPEN_WATER_VALVE))

        if ret[0]['function'] != ARC.OPEN_WATER_VALVE_SUCCESS:
            self._has_error = True
            raise RuntimeError()

        """update the states factory"""""

        return ret

    def stop_board_fan(self):
        self._current_state = SFConf.CODE.OPEN_WATER_VALVE['name']
        self.state.event_trigger()
        ret = self.comm.send(self.__convert(SFConf.CODE.CLOSE_WATER_VALVE))

        if ret[0]['function'] != ARC.CLOSE_WATER_VALVE_SUCCESS:
            self._has_error = True
            raise RuntimeError()

        """update the states factory"""""
        self.state.water_pump_status = ModuleState.IDLE

        return ret

    def start_cooling_fan(self):
        self.state.fan_status = ModuleState.RUNNING
        self.state.event_trigger()
        self._current_state = SFConf.CODE.START_COOLING_FAN['name']
        ret = self.comm.send(self.__convert(SFConf.CODE.START_COOLING_FAN))

        if ret[0]['function'] != ARC.START_COOLING_FAN_SUCCESS:
            self._has_error = True
            raise RuntimeError()

        """update the states factory"""""
        return ret

    def stop_cooling_fan(self):
        self._current_state = SFConf.CODE.STOP_COOLING_FAN['name']
        ret = self.comm.send(self.__convert(SFConf.CODE.STOP_COOLING_FAN))

        if ret[0]['function'] != ARC.STOP_COOLING_FAN_SUCCESS:
            self._has_error = True
            raise RuntimeError()

        """update the states factory"""""

        self.state.fan_status = ModuleState.IDLE
        self.state.event_trigger()
        return ret

    def on_induction(self):
        self.state.induction_status = ModuleState.RUNNING
        self.state.event_trigger()
        self._current_state = SFConf.CODE.ON_INDUCTION_HEATER['name']
        ret = self.comm.send(self.__convert(SFConf.CODE.ON_INDUCTION_HEATER))

        if ret[0]['function'] != ARC.START_INDUCTION_SUCCESS:
            self._has_error = True
            raise RuntimeError()

        """update the states factory"""""

        return ret

    def get_thermal_data(self):
        self._current_state = SFConf.CODE.READ_THERMAL_DATA['name']
        ret = self.comm.send(self.__convert(SFConf.CODE.READ_THERMAL_DATA))

        if ret[0]['function'] != ARC.READ_THERMAL_DATA:
            self._has_error = True
            raise RuntimeError()
        """update the states factory"""""

        return ret

    def off_induction(self):
        self._current_state = SFConf.CODE.OFF_INDUCTION_HEATER['name']
        ret = self.comm.send(self.__convert(SFConf.CODE.OFF_INDUCTION_HEATER))

        if ret[0]['function'] != ARC.STOP_INDUCTION_SUCCESS:
            self._has_error = True
            raise RuntimeError()

        """update the states factory"""""
        self.state.induction_status = ModuleState.IDLE
        self.state.event_trigger()
        return ret

    def is_plate_present(self):
        self.state.is_plate_ready = False
        self.state.event_trigger()
        self._current_state = SFConf.CODE.GET_PROXIMITY['name']
        ret = self.comm.send(self.__convert(SFConf.CODE.GET_PROXIMITY))

        if ret[0]['function'] != ARC.GET_PROXIMITY_SUCCESS:
            self._has_error = True
            raise RuntimeError()

        self.state.is_plate_ready = True
        self.state.event_trigger()
        return ret[0]['analog_status'] > 900

    def on_light(self):
        self._current_state = SFConf.CODE.OPEN_OIL_VALVE['name']
        ret = self.comm.send(self.__convert(SFConf.CODE.OPEN_OIL_VALVE))

        if ret[0]['function'] != ARC.OPEN_OIL_VALVE_SUCCESS:
            self._has_error = True
            raise RuntimeError()

        return ret

    def off_light(self):
        self._current_state = SFConf.CODE.CLOSE_OIL_VALVE['name']
        ret = self.comm.send(self.__convert(SFConf.CODE.CLOSE_OIL_VALVE))

        if ret[0]['function'] != ARC.CLOSE_OIL_VALVE_SUCCESS:
            self._has_error = True
            raise RuntimeError()

        return ret

    # version 2
    def update_time(self, target_time):
        """
        :param target_time: target time must be in long
        :return: json
        """
        self._current_state = SFConf.CODE.UPDATE_TIME['name']
        ret = self.comm.send(self.__convert(SFConf.CODE.UPDATE_TIME, 0, args1=target_time))

        if ret[0]['function'] != ARC.UPDATE_TIME:
            self._has_error = True
            raise RuntimeError()

        return ret

    def start_process(self):
        self._current_state = SFConf.CODE.START_PROCESS['name']
        ret = self.comm.send(self.__convert(SFConf.CODE.START_PROCESS))

        if ret[0]['function'] != ARC.START_PROCESS:
            self._has_error = True
            raise RuntimeError()

        return ret

    def stop_process(self):
        self._current_state = SFConf.CODE.STOP_PROCESS['name']
        ret = self.comm.send(self.__convert(SFConf.CODE.STOP_PROCESS))

        if ret[0]['function'] != ARC.STOP_PROCESS:
            self._has_error = True
            raise RuntimeError()

        return ret

    def update_temperature(self, target_temperature):
        self._current_state = SFConf.CODE.UPDATE_TEMPERATURE['name']
        ret = self.comm.send(self.__convert(SFConf.CODE.UPDATE_TEMPERATURE))

        if ret[0]['function'] != ARC.UPDATE_TEMPERATURE:
            self._has_error = True
            raise RuntimeError()

        return ret

    def pause_timer(self):
        self._current_state = SFConf.CODE.PAUSE_TIMER['name']
        ret = self.comm.send(self.__convert(SFConf.CODE.PAUSE_TIMER))

        if ret[0]['function'] != ARC.PAUSE_TIMER:
            self._has_error = True
            raise RuntimeError()

        return ret

    def unpause_timer(self):
        self._current_state = SFConf.CODE.UNPAUSE_TIMER['name']
        ret = self.comm.send(self.__convert(SFConf.CODE.UNPAUSE_TIMER))

        if ret[0]['function'] != ARC.UNPAUSE_TIMER:
            self._has_error = True
            raise RuntimeError()

        return ret

    def enable_flip(self):
        self._current_state = SFConf.CODE.ENABLE_FLIP['name']
        ret = self.comm.send(self.__convert(SFConf.CODE.ENABLE_FLIP))

        if ret[0]['function'] != ARC.ENABLE_FLIP:
            self._has_error = True
            raise RuntimeError()

        return ret

    def disable_flip(self):
        self._current_state = SFConf.CODE.DISABLE_FLIP['name']
        ret = self.comm.send(self.__convert(SFConf.CODE.DISABLE_FLIP))

        if ret[0]['function'] != ARC.DISABLE_FLIP:
            self._has_error = True
            raise RuntimeError()

        return ret

    @property
    def state_is_ready(self):
        return self._state_is_ready

    def set_debug(self, debug):
        self._debug = debug

    @staticmethod
    def __convert(instruction, position=0, args1=0, args2=0):
        return obj_to_json_string(UpdPacket(instruction['code'], position=position, args1=args1, args2=args2))

    def clean_error(self):
        self._has_error = False


if __name__ == '__main__':
    wrapper = StirFryWrapper('192.168.1.168', module_name='MODULE_1')
