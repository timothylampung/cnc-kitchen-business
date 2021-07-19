import time
from math import floor
import threading
import queue
from timeit import default_timer as timer

from app.models import Task, Module, Instruction
from business import settings
from stir_fry.api.ingredient_parser import ingredient_parser
from stir_fry.core.handler.cook_handler import CookHandler
from stir_fry.core.handler.mix_food_handler import MixFoodHandler
from stir_fry.core.handler.pick_ingredient_handler import PickIngredientHandler
from stir_fry.core.handler.portion_food_handler import PortionFoodHandler
from stir_fry.core.handler.set_to_temperature_handler import SetToTemperatureHandler
from stir_fry.core.wrapper.states import ModuleState

BY_PASS_ARM = getattr(settings, "BY_PASS_ARM", False)
_timer_sentinel = object()

MESSAGE_HANDLER = 'message'
REQUEST_PERMISSION = 'request_permission'
GRANT_PERMISSION = 'grant_permission'


def _timer(module_name: str, time_stopper: queue.Queue, etc, state):
    module_state: ModuleState = state
    sentinel = None
    start = timer()
    while sentinel != _timer_sentinel:
        time_lapse = float("%.2f" % (timer() - start))
        module_state.time_lapse = floor(time_lapse)
        if etc is not None and etc > 0:
            percentage = time_lapse / float(etc)
            if percentage >= 1:
                module_state.completion_percentage = 1
            else:
                module_state.completion_percentage = percentage
        try:
            sentinel = time_stopper.get(block=False)
            time.sleep(1)
        except Exception as e:
            str(e)
            pass


class RecipeHandler:
    def __init__(self, task: Task):
        self.task = task
        self.module = task.module_id
        from business.machine_settings import MODULES
        self._sdk = MODULES[self.module.type][self.module.name]['sdk']
        self._state: ModuleState = MODULES[self.module.type][self.module.name]['state']
        self._wrapper = self._sdk.wrapper

    def handle(self):
        while self.module.status == Module.BUSY:
            pass
        print(f'Running task {self.module.name}')
        self.module.status = Module.BUSY
        self.module.save()
        instructions = Instruction.objects.filter(recipe_id=self.task.recipe_id)
        recipe = self.task.recipe_id
        main_start = timer()
        all_ingredients = []

        if BY_PASS_ARM:
            all_ingredients = ingredient_parser(instructions)
            self._sdk.wrapper.state_factory.update_state(self.module.name, REQUEST_PERMISSION,
                                                         all_ingredients=all_ingredients,
                                                         current_process='BEFORE START, CHECK INGREDIENTS')
            self._state.clear_que()
            self._state.put_lock_queue()
            while self._state.is_process_locked():
                self._state.induction_status = ModuleState.IDLE
                self._state.temperature = self._sdk.wrapper.get_temperature()
        self._state.current_process = 'START'
        print('arm is not bypassed')
        time_stopper = queue.Queue()
        t = threading.Thread(target=_timer, args=(self.module.name, time_stopper, recipe.etc, self._state),
                             name=f'Timer for {self.module.name}')
        t.start()
        cook = CookHandler(self._sdk, self._state)
        set_to_temperature = SetToTemperatureHandler(self._sdk, self._state)
        pick_ingredient = PickIngredientHandler(self._sdk, self._state)
        portion_food = PortionFoodHandler(self._sdk, self._state)
        mix_food = MixFoodHandler(self._sdk, self._state)

        cook.set_next(pick_ingredient) \
            .set_next(set_to_temperature) \
            .set_next(portion_food) \
            .set_next(mix_food)
        print('handlers ready')

        from stir_fry.core.handler.handler import Handler

        def handle(handler: Handler):
            index = 0
            for instruction in instructions:
                if index == len(instructions):
                    break
                ins: Instruction = instructions[index]

                if self.task.recipe_id.etc is None:
                    percentage = ((index + 1) / len(instructions))
                    self._state.completion_percentage = percentage
                self._wrapper.set_vertical_0()
                self._wrapper.start_cooling_fan()
                self._wrapper.rotate_horizontal()
                handler.handle(ins, self.task)
                index = index + 1

        handle(cook)
        self._wrapper.set_vertical_0()
        self._wrapper.stop_cooling_fan()
        self._wrapper.stop_horizontal()
        self.module.status = Module.AVAILABLE
        self.module.save()

        # handle_instruction(instruction, self._sdk, self._wrapper, _manual_ingredients=all_ingredients)
