REQUEST_PERMISSION = 'request_permission'
GRANT_PERMISSION = 'grant_permission'
MESSAGE = 'message'
CAMERA = 'camera'
MODULE_CONTROLS = 'module_controls'


class CamOperation:
    ACTION = 'ACTION'
    START_CAMERA = 'START_CAMERA'
    CAMERA_STARTED = 'CAMERA_STARTED'
    DATA = 'DATA'


class ModuleControls:
    EMPTY = 'NONE'
    RAISE = 'RAISE'
    PLATE = 'PLATE'
    DEGREE_45 = '45'
    STOP_HORIZONTAL = 'STOP_HORIZONTAL'
    ROTATE_HORIZONTAL = 'ROTATE_HORIZONTAL'
    START_FAN = 'START_FAN'
    STOP_FAN = 'STOP_FAN'
    ON_LED = 'ON_LED'
    STOP_LED = 'STOP_LED'
    CHANGE_TEMPERATURE = 'CHANGE_TEMPERATURE'


CAMERA_DATA = {
    "message": {
        "handler_type": CAMERA,
        "data": {
            "type": CamOperation.ACTION,
        }
    }
}

MESSAGE_DATA = {
    "message": {
        "handler_type": MESSAGE,
        "data": {}
    }
}

GRANT_PERMISSION_DATA = {
    "message": {
        "handler_type": GRANT_PERMISSION,
        "data": {}
    }
}

REQUEST_PERMISSION_DATA = {
    "message": {
        "handler_type": REQUEST_PERMISSION,
        "data": {}
    }
}

MODULE_CONTROLS_DATA = {
    "message": {
        "handler_type": MODULE_CONTROLS,
        "data": {
            'module_id': 0,
            'instruction': ModuleControls.EMPTY
        }
    }
}
