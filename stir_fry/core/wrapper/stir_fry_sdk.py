#  Copyright (c) 2021.
#  Volume Research & Development sdn. bhd.
#  Author : Timothy Lampung
#  Email : timothylampung@gmail.com
#  Contacts : +601165315133

import time

from app.models import IngredientItem
from stir_fry.core.wrapper.stir_fry_wrapper import StirFryWrapper
from timeit import default_timer as timer
from transporter.core.wrapper.transporter_wrappers import TransporterSingleton


class StirFrySDK:

    def __init__(self, ip, module_name):
        self.ip = ip
        self.module_name = module_name
        self.wrapper = StirFryWrapper(self.ip, module_name)
        self.transporter: TransporterSingleton = TransporterSingleton.get_instance()

    def cook(self, target_temperature, duration, need_flip):
        """
        :param target_temperature: target temperature on cooking,
                                    when it reaches the temperature,
                                    induction will stop
        :param duration: duration for cooking
        :param need_flip: vertical action to flip the foods
        :return: void
        """
        self.wrapper.rotate_horizontal()
        start = timer()
        time_lapse = 0

        while time_lapse <= duration:
            if self.wrapper.get_temperature() > target_temperature:
                if need_flip:
                    self.wrapper.set_vertical_0()
                    self.wrapper.set_vertical_45()
                self.wrapper.off_induction()
                start_wait = timer()
                wait_lapse = 0
                while wait_lapse < 5:
                    wait_lapse = float("%.2f" % (timer() - start_wait))
            else:
                self.wrapper.on_induction()
            time_lapse = float("%.2f" % (timer() - start))
            time.sleep(1)

        self.wrapper.off_induction()

    def set_to_temperature(self, target_temperature):
        """
        :param target_temperature: Target temperature to reach before the induction stops
        :return: void
        """
        self.wrapper.rotate_horizontal()
        temp = self.wrapper.get_temperature()
        start = timer()
        while temp < target_temperature - 10 or temp > target_temperature + 10:
            time_lapse = float("%.2f" % (timer() - start))
            if temp < target_temperature - 10:
                self.wrapper.on_induction()
            elif temp > target_temperature + 10:
                self.wrapper.off_induction()
            temp = self.wrapper.get_temperature()
            if time_lapse > 45:
                print(f'Set temperature is taking longer than usual, '
                      f'stopped due to timeout {45} seconds')
                break
            time.sleep(1)

        self.wrapper.off_induction()

    def pump_oil(self, volume):
        """
        :param volume: Volume of oil to be pump into the wok
        :return: void
        """
        self.wrapper.open_oil_valve()
        start = timer()
        time_lapse = 0
        while time_lapse < volume / 3:
            time_lapse = float("%.2f" % (timer() - start))
        self.wrapper.close_oil_valve()
        self.wrapper.set_vertical_45()
        start = timer()
        time_lapse = 0
        while time_lapse < 3:
            time_lapse = float("%.2f" % (timer() - start))

    def pump_water(self, volume):
        """
        :param volume: Volume of water to be pump into the wok
        :return: void
        """
        self.wrapper.open_water_valve()
        start = timer()
        time_lapse = 0
        while time_lapse < volume / 3:
            time_lapse = float("%.2f" % (timer() - start))
        self.wrapper.close_water_valve()
        self.wrapper.set_vertical_45()
        start = timer()
        time_lapse = 0
        while time_lapse < 3:
            time_lapse = float("%.2f" % (timer() - start))

    def pick_ingredients(self, item: IngredientItem, requester):
        self.transporter.handle_item(item, f'{item.ingredient_id.type}_{requester}')
        # handle_item(item, f'{item.ingredient_id.type}_{requester}')

    def portion_food_proximity(self):
        """
        :return: void
        """
        self.wrapper.rotate_horizontal()
        time.sleep(5)
        self.wrapper.shake_horizontal()
        # while self.wrapper.is_plate_present():
        #     print('waiting for plate', end='\r')
        #

        self.wrapper.set_vertical_plating()
        time.sleep(10)
        self.wrapper.stop_horizontal()
        time.sleep(45)
        self.wrapper.set_vertical_0()

    def portion_food_manual(self):
        """
        :return: void
        """
        self.wrapper.rotate_horizontal()
        time.sleep(5)
        self.wrapper.shake_horizontal()
        self.wrapper.set_vertical_plating()
        time.sleep(10)
        self.wrapper.stop_horizontal()

    def mix_food(self, duration):
        self.wrapper.rotate_horizontal()
        self.wrapper.set_vertical_45()
        time.sleep(duration)
        self.wrapper.stop_horizontal()

    def read_thermal_data(self):
        return self.wrapper.get_thermal_data()[0]
