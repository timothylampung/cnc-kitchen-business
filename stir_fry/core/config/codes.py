#  Copyright (c) 2021.
#  Volume Research & Development sdn. bhd.
#  Author : Timothy Lampung
#  Email : timothylampung@gmail.com
#  Contacts : 01165315133

class ArduinoResponseCode:
    DISABLE_FLIP = 'disable_flip'
    ENABLE_FLIP = 'enable_flip'
    START_PROCESS = 'start_process'
    STOP_PROCESS = 'stop_process'
    UPDATE_TEMPERATURE = 'update_temperature'
    UNPAUSE_TIMER = 'unpause_timer'
    CLOSE_OIL_VALVE_SUCCESS = 'close_oil_valve'
    OPEN_OIL_VALVE_SUCCESS = 'open_oil_valve'
    CLOSE_WATER_VALVE_SUCCESS = 'close_water_valve'
    OPEN_WATER_VALVE_SUCCESS = 'open_water_valve'
    PING_VERTICAL_SUCCESS = 'ping_vertical'
    PING_HORIZONTAL_SUCCESS = 'ping_horizontal'
    GET_LIMIT_SWITCH_SUCCESS = 'get_limit_switch_status'
    GET_LOAD_CELL_SUCCESS = 'get_load_cell_reading'
    GET_PROXIMITY_SUCCESS = 'get_proximity_switch_status'
    GET_TEMPERATURE_SUCCESS = 'get_wok_temperature'
    STOP_INDUCTION_SUCCESS = 'stop_induction_heaters'
    START_INDUCTION_SUCCESS = 'start_induction_heaters'
    START_COOLING_FAN_SUCCESS = 'start_cooling_fan'
    STOP_COOLING_FAN_SUCCESS = 'stop_cooling_fan'
    READ_THERMAL_DATA = 'READ_THERMAL_DATA'


ArduinoCodeMap = {
    100: {
        'en': {
            'title': 'Arduino Udp Timeout please check the Ethernet cable'
        }
    }
}
