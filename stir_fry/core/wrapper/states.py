#  Copyright (c) 2021.
#  Volume Research & Development sdn. bhd.
#  Author : Timothy Lampung
#  Email : timothylampung@gmail.com
#  Contacts : +601165315133


import json
import queue

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
            print(f'WAITING FOR PERMISSION')
            get = self.__release_que.get(block=True)
            print(f'IS PROCESS BLOCKED ? : {get}')
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


class ModuleStateFactory:
    __instance = None

    @staticmethod
    def get_instance():
        if ModuleStateFactory.__instance is None:
            ModuleStateFactory()
        return ModuleStateFactory.__instance

    def __init__(self):
        if ModuleStateFactory.__instance is not None:
            raise Exception("Module State is singleton")
        else:
            self.__modules_states = []
            ModuleStateFactory.__instance = self

    def register(self, module, by_pass_arm=False):
        state = ModuleState(module.name, by_pass_arm=by_pass_arm)
        self.__modules_states.append(state)

    def get_state(self, module_name: str):
        for i in self.__modules_states:
            if isinstance(i, ModuleState):
                if i.module_name == module_name:
                    return i

    def lock(self, module_name):
        for x, i in enumerate(self.__modules_states):
            if isinstance(i, ModuleState):
                if i.module_name == module_name:
                    i.put_lock_queue()
                    break

    def release(self, module_name):
        for x, i in enumerate(self.__modules_states):
            if isinstance(i, ModuleState):
                if i.module_name == module_name:
                    i.put_release_que()
                    break

    def clear_que(self, module_name):
        for x, i in enumerate(self.__modules_states):
            if isinstance(i, ModuleState):
                if i.module_name == module_name:
                    i.clear_que()
                    break

    def is_process_locked(self, module_name):
        for x, i in enumerate(self.__modules_states):
            if isinstance(i, ModuleState):
                if i.module_name == module_name:
                    return i.is_process_locked()

    def update_state(self, module_name: str, handler_type: str, horizontal_status=None, vertical_status=None,
                     induction_status=None,
                     oil_pump_status=None, water_pump_status=None, time_lapse=0, temperature=0.0, fan_status=None,
                     current_process=None, is_plate_ready=None, done_pick_up=None, ingredients=None,
                     all_ingredients=None,
                     completion_percentage=None,
                     module_status=None,
                     status=None
                     ):

        for x, i in enumerate(self.__modules_states):
            if isinstance(i, ModuleState):
                if i.module_name == module_name:
                    if temperature != 0.0:
                        self.__modules_states[x].temperature = temperature
                    if horizontal_status is not None:
                        self.__modules_states[x].horizontal_status = horizontal_status
                    if vertical_status is not None:
                        self.__modules_states[x].vertical_status = vertical_status
                    if induction_status is not None:
                        self.__modules_states[x].induction_status = induction_status
                    if oil_pump_status is not None:
                        self.__modules_states[x].oil_pump_status = oil_pump_status
                    if water_pump_status is not None:
                        self.__modules_states[x].water_pump_status = water_pump_status
                    if time_lapse != 0:
                        self.__modules_states[x].time_lapse = time_lapse
                    if fan_status is not None:
                        self.__modules_states[x].fan_status = fan_status
                    if current_process is not None:
                        self.__modules_states[x].current_process = current_process
                    if is_plate_ready is not None:
                        self.__modules_states[x].is_plate_ready = is_plate_ready
                    if done_pick_up is not None:
                        self.__modules_states[x].done_pick_up = done_pick_up
                    if ingredients is not None:
                        self.__modules_states[x].ingredients = ingredients
                    if all_ingredients is not None:
                        self.__modules_states[x].all_ingredients = all_ingredients
                    if completion_percentage is not None:
                        self.__modules_states[x].completion_percentage = completion_percentage
                    if handler_type is not None:
                        self.__modules_states[x].handler_type = handler_type
                    if status is not None:
                        self.__modules_states[x].module_status = module_status

                    self.publish_state(module_name)
                    return self.__modules_states[x]

    def publish_state(self, module_name):
        for x, i in enumerate(self.__modules_states):
            if isinstance(i, ModuleState):
                if i.module_name == module_name:
                    from channels.layers import get_channel_layer
                    from asgiref.sync import async_to_sync
                    channel_layer = get_channel_layer()
                    ingredients = None
                    state: ModuleState = self.__modules_states[x]
                    if state.ingredients is not None:
                        tmp = state.ingredients
                        ingredients = []
                        for o in tmp:
                            ingredients.append(o.dump())
                        # ingredients = json.dumps([o.dump() for o in ingredients])

                    all_ingredients = None
                    if state.all_ingredients is not None:
                        tmp = state.all_ingredients
                        all_ingredients = []
                        for o in tmp:
                            all_ingredients.append(o.dump())

                    return i
                    async_to_sync(channel_layer.group_send)(
                        module_name, {
                            'type': 'message',
                            'message': {
                                'module_name': state.module_name,
                                'horizontal_status': state.horizontal_status,
                                'vertical_status': state.vertical_status,
                                'induction_status': state.induction_status,
                                'oil_pump_status': state.oil_pump_status,
                                'water_pump_status': state.water_pump_status,
                                'fan_status': state.fan_status,
                                'time_lapse': state.time_lapse,
                                'temperature': state.temperature,
                                'is_plate_ready': state.is_plate_ready,
                                'current_process': state.current_process,
                                'by_pass_arm': state.by_pass_arm,
                                'done_pick_up': state.done_pick_up,
                                'ingredients': ingredients,
                                'all_ingredients': all_ingredients,
                                'completion_percentage': state.completion_percentage,
                                'lock_count': state.lock_count,
                                'handler_type': state.handler_type
                            }
                        }
                    )
                    return i
