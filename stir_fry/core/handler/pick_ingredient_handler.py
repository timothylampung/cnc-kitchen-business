from app.models import Instruction, Task, IngredientItem
from stir_fry.core.handler.handler import AbstractHandler
from stir_fry.core.wrapper.states import ModuleState
from stir_fry.core.wrapper.stir_fry_sdk import StirFrySDK


class PickIngredientHandler(AbstractHandler):

    def __init__(self, sdk: StirFrySDK, state: ModuleState):
        self._sdk = sdk
        self._wrapper = self._sdk.wrapper
        self._state = state

    def handle(self, instruction: Instruction, task: Task) -> str:
        if instruction.name == Instruction.PICK_INGREDIENT:
            print(f'------- PICKING INGREDIENT ------ {instruction.name}')
            for item in IngredientItem.objects.filter(instruction_id=instruction):
                print(f'------- PICKING INGREDIENT ------ {item.ingredient_id.ingredient_name}')
                self._sdk.pick_ingredients(item, self._sdk.module_name)
            return "PICK INGREDIENT"
        else:
            return super().handle(instruction, task)
