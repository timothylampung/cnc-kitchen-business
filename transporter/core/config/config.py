#  Copyright (c) 2021.
#  Volume Research & Development sdn. bhd.
#  Author : Timothy Lampung
#  Email : timothylampung@gmail.com
#  Contacts : 01165315133


class TTConf(object):

    def __init__(self):
        pass

    class CODE:
        MOVE_SOLID_TUBE = {
            'code': 10,
            'name': 'MOVE_SOLID_TUBE'
        }
        MOVE_SOLID_PLUNGER = {
            'code': 11,
            'name': 'MOVE_SOLID_PLUNGER'
        }
        MOVE_LIQUID_PLUNGER = {
            'code': 12,
            'name': 'MOVE_LIQUID_PLUNGER'
        }
        MOVE_GRANULAR_TUBE = {
            'code': 13,
            'name': 'MOVE_GRANULAR_TUBE'
        }
        MOVE_GRANULAR_PLUNGER = {
            'code': 14,
            'name': 'MOVE_GRANULAR_PLUNGER'
        }
        TOGGLE_GRANULAR_VACUUM = {
            'code': 15,
            'name': 'TOGGLE_GRANULAR_VACUUM'
        }
        TOGGLE_GRANULAR_BLOWER = {
            'code': 16,
            'name': 'TOGGLE_GRANULAR_BLOWER'
        }
        TOGGLE_SOLID_VACUUM = {
            'code': 17,
            'name': 'TOGGLE_SOLID_VACUUM'
        }
        TOGGLE_SOLID_BLOWER = {
            'code': 18,
            'name': 'TOGGLE_SOLID_BLOWER'
        }
        MOVE_TO_COORDINATE = {
            'code': 30,
            'name': 'MOVE_TO_COORDINATE'
        }
        RESET = {
            'code': 31,
            'name': 'RESET'
        }

        ArduinoRequestTimeOut = 180
