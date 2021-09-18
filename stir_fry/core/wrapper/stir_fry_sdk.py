#  Copyright (c) 2021.
#  Volume Research & Development sdn. bhd.
#  Author : Timothy Lampung
#  Email : timothylampung@gmail.com
#  Contacts : +601165315133

import time
from stir_fry.core.wrapper.states import ModuleState
from stir_fry.core.wrapper.stir_fry_wrapper import StirFryWrapper
from timeit import default_timer as timer


class StirFrySDK:

    def __init__(self, ip, module_name):
        self.ip = ip
        self.module_name = module_name
        self.state = ModuleState(module_name, by_pass_arm=False)
        self.wrapper = StirFryWrapper(self.ip, module_name, self.state)
        self.target_temperature = 32.0

    def change_temperature(self, target_temperature):
        """
        :param target_temperature:
        :return:
        """
        self.target_temperature = target_temperature

    def functionality_test(self, count):
        self.wrapper.rotate_horizontal()
        for i in range(count):
            self.wrapper.set_vertical_0()
            self.wrapper.set_vertical_45()
            time.sleep(3)
            self.wrapper.set_vertical_0()

        self.wrapper.set_vertical_plating()
        time.sleep(4)
        self.wrapper.set_vertical_0()
        self.wrapper.set_vertical_washing()
        time.sleep(3)
        self.wrapper.set_vertical_0()
        self.wrapper.set_vertical_45()
        self.wrapper.set_vertical_0()

    def cook(self, target_temperature, duration, need_flip):
        """
        :param target_temperature: target temperature on cooking,
                                    when it reaches the temperature,
                                    induction will stop
        :param duration: duration for cooking
        :param need_flip: vertical action to flip the foods
        :return: void
        """
        self.target_temperature = target_temperature
        self.wrapper.rotate_horizontal()
        start = timer()
        time_lapse = 0
        self.wrapper.set_vertical_0()
        self.wrapper.set_vertical_picking()

        self.wrapper.start_cooling_fan()
        self.wrapper.start_board_fan()

        while time_lapse <= duration:
            if self.wrapper.is_far:
                self.wrapper.off_induction()
            else:
                if self.wrapper.get_temperature() > self.target_temperature:
                    self.wrapper.off_induction()
                    if need_flip:
                        self.wrapper.set_vertical_0()
                        self.wrapper.set_vertical_45()
                        start_wait = timer()
                        wait_lapse = 0
                        while wait_lapse < 5:
                            wait_lapse = float("%.2f" % (timer() - start_wait))
                        self.wrapper.set_vertical_0()
                        self.wrapper.set_vertical_picking()
                elif self.wrapper.get_temperature() < self.target_temperature:
                    self.wrapper.on_induction()
            time_lapse = float("%.2f" % (timer() - start))
            time.sleep(1)

        self.wrapper.set_vertical_0()
        self.wrapper.off_induction()

    def set_to_temperature(self, target_temperature):
        """
        :param target_temperature: Target temperature to reach before the induction stops
        :return: void
        """
        self.target_temperature = target_temperature
        self.wrapper.rotate_horizontal()
        temp = self.wrapper.get_temperature()
        start = timer()
        while temp < self.target_temperature - 10 or temp > self.target_temperature + 10:
            time_lapse = float("%.2f" % (timer() - start))
            if (temp < self.target_temperature - 10) and not self.wrapper.is_far:
                self.wrapper.on_induction()
            elif (temp > self.target_temperature + 10) and not self.wrapper.is_far:
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
        self.wrapper.start_board_fan()
        start = timer()
        time_lapse = 0
        while time_lapse < volume / 3:
            time_lapse = float("%.2f" % (timer() - start))
        self.wrapper.stop_board_fan()
        self.wrapper.set_vertical_45()
        start = timer()
        time_lapse = 0
        while time_lapse < 3:
            time_lapse = float("%.2f" % (timer() - start))

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
        print('portion food')
        self.wrapper.set_vertical_0()
        self.wrapper.rotate_horizontal()
        time.sleep(5)
        self.wrapper.set_vertical_plating()
        time.sleep(10)
        self.wrapper.set_vertical_0()
        self.wrapper.stop_horizontal()

    def mix_food(self, duration):
        self.wrapper.rotate_horizontal()
        self.wrapper.set_vertical_45()
        time.sleep(duration)
        self.wrapper.stop_horizontal()

    def on_light(self):
        self.wrapper.on_light()

    def off_light(self):
        self.wrapper.off_light()

    def read_thermal_data(self):
        return self.wrapper.get_thermal_data()[0]
