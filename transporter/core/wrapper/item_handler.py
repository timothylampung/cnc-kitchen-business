#  Copyright (c) 2021.
#  Volume Research & Development sdn. bhd.
#  Author : Timothy Lampung
#  Email : timothylampung@gmail.com
#  Contacts : +601165315133

from app.models import IngredientItem, Coordinates


def handle_item(item: IngredientItem, requester):
    from transporter.core.wrapper.transporter_wrappers import TransporterSingleton as Ts
    transporter: Ts = Ts.get_instance()
    claim_id = transporter.claim_transporter()
    coordinate = item.ingredient_id.coordinate_id
    ingredient = item.ingredient_id
    transporter.move_to_coordinate(ingredient.coordinate_x, ingredient.coordinate_y, claim_id)
    dispense: Coordinates = Coordinates.objects.get(name=requester)
    transporter.move_to_coordinate(dispense.linear, dispense.center, claim_id)
    # """moving toward positions and sucking things up"""
    # if coordinate.type == Coordinates.SOLID:
    #     transporter.move_solid_tube(Ts.MAX_SOLID_TUBE, claim_id)
    #     transporter.move_solid_plunger(Ts.MAX_SOLID_PLUNGER, claim_id)
    #     transporter.on_solid_vacuum(claim_id)
    #     time.sleep(30)
    #     transporter.move_solid_plunger(item.quantity, claim_id)
    #     transporter.remove_solid_excess(claim_id)
    #
    # elif coordinate.type == Coordinates.LIQUID:
    #     transporter.move_granular_tube(Ts.MAX_GRANULAR_TUBE, claim_id)
    #     transporter.move_liquid_plunger(Ts.MAX_LIQUID_PLUNGER, claim_id)
    #     time.sleep(30)
    #     transporter.move_liquid_plunger(item.quantity, claim_id)
    #
    # elif coordinate.type == Coordinates.GRANULAR:
    #     transporter.move_granular_tube(Ts.MAX_GRANULAR_TUBE, claim_id)
    #     transporter.move_granular_plunger(Ts.MAX_GRANULAR_PLUNGER, claim_id)
    #     transporter.on_granular_vacuum(claim_id)
    #     time.sleep(30)
    #     transporter.move_granular_plunger(item.quantity, claim_id)
    # else:
    #     print('ingredient is LOL type')
    # transporter.move_granular_tube(0, claim_id)
    # transporter.move_solid_tube(0, claim_id)

    """moving toward positions and sucking things up"""
