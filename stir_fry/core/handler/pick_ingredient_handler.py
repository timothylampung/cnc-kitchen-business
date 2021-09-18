from app.models import Instruction, Task, IngredientItem
from stir_fry.core.handler.handler import AbstractHandler
from transporter.core.wrapper.transporter_wrappers import TransporterSingleton


class PickIngredientHandler(AbstractHandler):

    def __init__(self, sdk: TransporterSingleton, requester_name):
        self._sdk = sdk
        self._requester_name = requester_name

    def handle(self, instruction: Instruction, task: Task) -> str:
        if instruction.name == Instruction.PICK_INGREDIENT:
            for item in IngredientItem.objects.filter(instruction_id=instruction):
                self._sdk.handle_item(item, f'{item.ingredient_id.type}_{self._requester_name}')
            return "PICK INGREDIENT"

        else:
            return super().handle(instruction, task)
