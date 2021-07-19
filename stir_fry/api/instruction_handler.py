from collections import Sequence

from numpy.lib.function_base import insert

from app.models import Instruction, IngredientItem, Ingredient
from stir_fry.core.wrapper.stir_fry_sdk import StirFrySDK
from stir_fry.core.wrapper.stir_fry_wrapper import StirFryWrapper


def handle_instruction(instruction: Instruction,
                       _sdk: StirFrySDK,
                       _wrapper: StirFryWrapper,
                       _manual_ingredients,
                       bypass_arm: bool
                       ):
    if instruction.name == Instruction.COOK:
        _sdk.cook(instruction.target_temperature, instruction.duration, instruction.flip_enabled)
    elif instruction.name == Instruction.SET_TO_TEMPERATURE:
        _sdk.set_to_temperature(instruction.target_temperature)
    elif instruction.name == Instruction.PORTION_FOOD:
        # @todo more work on here TIMOTHY LAMPUNG
        _sdk.portion_food_manual()
    elif instruction.name == Instruction.MIX_FOOD:
        _sdk.mix_food(instruction.duration)
    elif instruction.name == Instruction.PICK_INGREDIENT:
        # @todo more work on here TIMOTHY LAMPUNG
        if bypass_arm:
            pass
        else:
            for item in instruction.ingredient_items_of_instruction:
                if isinstance(item, IngredientItem):
                    _sdk.pick_ingredients(item)
