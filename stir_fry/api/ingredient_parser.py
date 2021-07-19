from collections import Sequence

from app.models import Instruction, IngredientItem


def ingredient_parser(instructions):
    all_ingredient = []
    for instruction in instructions:
        if instruction.name == Instruction.PICK_INGREDIENT:
            group = []
            for item in instruction.ingredient_items_of_instruction:
                if isinstance(item, IngredientItem):
                    item.ingredient_id.ingredient_name = f'{item.quantity} {item.ingredient_id.unit} of ' \
                                                         f'{item.ingredient_id.ingredient_name} '
                    group.append(item.ingredient_id)
            all_ingredient.append(group)
    return all_ingredient
