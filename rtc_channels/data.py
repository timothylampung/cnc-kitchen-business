
REQUEST_PERMISSION = 'request_permission'
GRANT_PERMISSION = 'grant_permission'
MESSAGE = 'message'
CAMERA = 'camera'


class CamOperation:
    ACTION = 'ACTION'
    START_CAMERA = 'START_CAMERA'
    CAMERA_STARTED = 'CAMERA_STARTED'
    DATA = 'DATA'


CAMERA_DATA = {
    "message": {
        "handler_type": CAMERA,
        "data": {
            "type": CamOperation.ACTION
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

