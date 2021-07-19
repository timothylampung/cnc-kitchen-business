import queue
import threading

from app.models import Task
from stir_fry.api.recipe_handler import RecipeHandler

MESSAGE_HANDLER = 'message'
REQUEST_PERMISSION = 'request_permission'
GRANT_PERMISSION = 'grant_permission'

_sentinel_stop_worker = '*(sdj23nAsd8Y$#@sdfsjhd3(*W!Q'


class StirFryTaskRunner(threading.Thread):
    def __init__(self, q: queue.Queue, *args, **kwargs):
        self.queue = q
        super().__init__(*args, **kwargs)

    def run(self, *args, **kwargs):
        while True:
            try:
                task = self.queue.get_nowait()
                if isinstance(task, str):
                    if task == _sentinel_stop_worker:
                        break
                elif isinstance(task, Task):
                    recipe_handler = RecipeHandler(task)
                    recipe_handler.handle()
                    print(task.__str__())
            except Exception as e:
                pass
