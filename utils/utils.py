#  Copyright (c) 2021.
#  Volume Research & Development sdn. bhd.
#  Author : Timothy Lampung
#  Email : timothylampung@gmail.com
#  Contacts : 01165315133

import json
import platform  # For getting the operating system name
import subprocess  # For executing a shell command


def obj_to_json_string(obj):
    dumps = json.dumps(obj.__dict__)
    return dumps


def count_directories(path):
    import os
    count1 = 0
    for root, dirs, files in os.walk(path):
        count1 += len(dirs)
    return count1


def ping(ip):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', ip]
    return subprocess.call(command) == 0
