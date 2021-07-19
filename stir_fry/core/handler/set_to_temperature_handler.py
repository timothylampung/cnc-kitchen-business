from app.models import Instruction, Task
from stir_fry.core.handler.handler import AbstractHandler
from stir_fry.core.wrapper.states import ModuleState
from stir_fry.core.wrapper.stir_fry_sdk import StirFrySDK


class SetToTemperatureHandler(AbstractHandler):

    def __init__(self, sdk: StirFrySDK, state: ModuleState):
        self._sdk = sdk
        self._wrapper = self._sdk.wrapper
        self._state = state

    def handle(self, instruction: Instruction, task: Task) -> str:
        if instruction.name == Instruction.SET_TO_TEMPERATURE:
            print(f'------- SET TO TEMPERATURE ------ {instruction.name}')
            self._sdk.set_to_temperature(instruction.target_temperature)
            return "SET TO TEMPERATURE"
        else:
            return super().handle(instruction, task)
