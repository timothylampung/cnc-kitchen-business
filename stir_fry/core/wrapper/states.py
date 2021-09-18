#  Copyright (c) 2021.
#  Volume Research & Development sdn. bhd.
#  Author : Timothy Lampung
#  Email : timothylampung@gmail.com
#  Contacts : +601165315133


import json
import queue

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

LOCK = True
RELEASE = False


class ModuleState:
    RUNNING = 'RUNNING'
    IDLE = 'IDLE'
    ERROR = 'ERROR'
    BUSY = 'BUSY'
    AVAILABLE = 'AVAILABLE'

    def __init__(self, module_name: str = None, by_pass_arm=False):
        self.module_status = ModuleState.BUSY
        self.module_name = module_name
        self.horizontal_status = self.IDLE
        self.vertical_status = self.IDLE
        self.induction_status = self.IDLE
        self.oil_pump_status = self.IDLE
        self.water_pump_status = self.IDLE
        self.fan_status = self.IDLE
        self.time_lapse = 0
        self.temperature = 36.0
        self.is_plate_ready = False
        self.current_process = ''
        self.done_pick_up = False
        self.ingredients = None
        self.all_ingredients = None
        self.completion_percentage = 0
        self.lock_count = 0
        self.by_pass_arm = by_pass_arm
        self.handler_type = 'message'  # request_permission, grant_permission
        self.__release_que = queue.Queue()

    def put_release_que(self):
        self.lock_count = self.lock_count - 1
        self.__release_que.put_nowait(RELEASE)

    def put_lock_queue(self):
        self.lock_count = self.lock_count + 1
        self.__release_que.put_nowait(LOCK)

    def is_process_locked(self):
        get = LOCK
        try:
            get = self.__release_que.get(block=True)
            return get
        except:
            return get

    # def clear_que(self):
    #     self.__release_que.queue.clear()

    def clear_que(self):
        '''
        Clears all items from the queue.
        '''
        self.lock_count = 0
        with self.__release_que.mutex:
            unfinished = self.__release_que.unfinished_tasks - len(self.__release_que.queue)
            if unfinished <= 0:
                if unfinished < 0:
                    raise ValueError('task_done() called too many times')
                self.__release_que.all_tasks_done.notify_all()
            self.unfinished_tasks = unfinished
            self.__release_que.queue.clear()
            self.__release_que.not_full.notify_all()

    def __str__(self):
        return json.dumps(self.__dict__)

    def event_trigger(self):
        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'{self.module_name}_STATES', {
                    'type': 'state',
                    'message': {
                        'module_name': self.module_name,
                        'horizontal_status': self.horizontal_status,
                        'vertical_status': self.vertical_status,
                        'induction_status': self.induction_status,
                        'oil_pump_status': self.oil_pump_status,
                        'water_pump_status': self.water_pump_status,
                        'fan_status': self.fan_status,
                        'time_lapse': self.time_lapse,
                        'temperature': self.temperature,
                        'is_plate_ready': self.is_plate_ready,
                        'current_process': self.current_process,
                        'by_pass_arm': self.by_pass_arm,
                        'done_pick_up': self.done_pick_up,
                        'ingredients': self.ingredients,
                        'all_ingredients': self.all_ingredients,
                        'completion_percentage': self.completion_percentage,
                        'lock_count': self.lock_count,
                        'handler_type': self.handler_type
                    }
                }
            )
        except Exception as e:
            raise Exception('Failed to connect to redis. Please make sure that docker or redis is running')
