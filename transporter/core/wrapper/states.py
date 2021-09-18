#  Copyright (c) 2021.
#  Volume Research & Development sdn. bhd.
#  Author : Timothy Lampung
#  Email : timothylampung@gmail.com
#  Contacts : +601165315133


import json
import queue

LOCK = True
RELEASE = False


class TransporterState:
    RUNNING = 'RUNNING'
    IDLE = 'IDLE'
    ERROR = 'ERROR'
    BUSY = 'BUSY'
    AVAILABLE = 'AVAILABLE'

    def __init__(self, module_name: str = None):
        self.module_status = self.BUSY
        self.module_name = module_name
        self.current_process = ''
        self.lock_count = 0
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
