from app.models import Instruction, Task
from stir_fry.core.handler.handler import AbstractHandler
from stir_fry.core.wrapper.states import ModuleState
from stir_fry.core.wrapper.stir_fry_sdk import StirFrySDK


class MixFoodHandler(AbstractHandler):

    def __init__(self, sdk: StirFrySDK, state: ModuleState):
        self._sdk = sdk
        self._wrapper = self._sdk.wrapper
        self._state = state

    def handle(self, instruction: Instruction, task: Task) -> str:
        if instruction.name == Instruction.COOK:
            print(f'------- MIXING FOOD ------ {instruction.name}')
            self._sdk.mix_food(instruction.duration)
            return "MIX FOOD"
        else:
            return super().handle(instruction, task)
