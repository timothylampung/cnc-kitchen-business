#  Copyright (c) 2021.
#  Volume Research & Development sdn. bhd.
#  Author : Timothy Lampung
#  Email : timothylampung@gmail.com
#  Contacts : 01165315133

import json
import socket
from stir_fry.core.config.config import SFConf
import platform  # For getting the operating system name
import subprocess  # For executing a shell command


class UpdPacket:
    def __init__(self, function=SFConf.CODE.OFF_INDUCTION_HEATER, position=0, args1=0, args2=0):
        self.function = function
        self.position = position
        self.args1 = args1
        self.args2 = args2


class UdpSetUp:
    GET_PORT = 8888
    GET_UDP_TIMEOUT = 180


class ArduinoUdp:
    ONLINE = True
    OFFLINE = False

    def __init__(self, ip, port=8888):
        self.ip = ip
        self.busy = False
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.settimeout(300)
        self.addr = (ip, port)

    def ping(self):
        """
        Returns True if host (str) responds to a ping request.
        Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
        """
        # Option for the number of packets as a function of
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', self.ip]
        return subprocess.call(command) == 0

    def recv(self):
        try:
            data, server = self.client_socket.recvfrom(1024)
            loads = json.loads(data.decode('utf-8'))
            self.busy = False
            return loads, server
        except (socket.timeout, json.decoder.JSONDecodeError) as e:
            self.busy = False
            raise Exception(f'Arduino UDP 6 1 {e}')

    def send(self, message):
        # if not self.ping():
        #     raise Exception(f'ping failed {self.ip}')

        while self.busy:
            pass
        self.busy = True
        self.client_socket.sendto(message.encode(), self.addr)
        recv = self.recv()
        return recv
