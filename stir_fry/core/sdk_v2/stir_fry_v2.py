import threading

from stir_fry.core.wrapper.states import ModuleState
from stir_fry.core.wrapper.stir_fry_sdk import StirFrySDK
from stir_fry.core.wrapper.stir_fry_wrapper import StirFryWrapper


class StirFryV2(StirFrySDK):
    def __init__(self, ip, module_name):
        super().__init__(ip, module_name)
        self.ip = ip
        self.module_name = module_name
        self.state = ModuleState(module_name, by_pass_arm=False)
        self.wrapper = StirFryWrapper(self.ip, module_name, self.state)
        self.target_temperature = 32.0
        super().state = self.state
        super().wrapper = self.wrapper
        super().target_temperature = self.target_temperature

    @staticmethod
    def update_status(_wrapper: StirFryWrapper):
        import sched, time
        s = sched.scheduler(time.time, time.sleep)

        def do_something(sc, wrp: StirFryWrapper):
            print(wrp.get_states())
            s.enter(2, 1, do_something, (sc, wrp))

        s.enter(2, 1, do_something, (s, _wrapper))

        print('HEY!')
        s.run()

    def start(self, target_temperature, duration, need_flip):
        t = threading.Thread(target=self.update_status, args=(self.wrapper,))
        t.start()
        self.wrapper.update_temperature(target_temperature)
        self.wrapper.update_time(duration)
        if need_flip:
            self.wrapper.enable_flip()
        else:
            self.wrapper.disable_flip()
        self.wrapper.start_process()
