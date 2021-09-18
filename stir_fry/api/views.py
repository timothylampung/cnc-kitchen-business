from rest_framework import mixins, generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from app.api.serializers import TaskViewSerializer
from app.api.views import CustomPaginationClass
from app.models import Module, Task, Setting
from stir_fry.api.task_runner import _sentinel_stop_worker


@permission_classes((AllowAny,))
class TaskExecutionView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Module.objects.all()
    serializer_class = TaskViewSerializer
    pagination_class = CustomPaginationClass

    def __init__(self):
        super().__init__()

    def get_queryset(self):
        qs = Module.objects.all()
        query = self.request.GET.get('query')
        if query is not None and query != '':
            qs = qs.filter(task_name__icontains=query)
        return qs

    def post(self, request, *args, **kwargs):
        module_id = self.request.GET.get('module_id')
        tasks = Task.objects.filter(module_id=module_id)

        def run(recipes):
            for task in recipes:
                from stir_fry.api.recipe_handler import RecipeHandler

                path = task.recipe_id.cv_images_path
                if task.recipe_id.cv_model_path is None:
                    pass
                else:
                    image_per_cv: Setting = Setting.objects.get(key='COUNT_OF_IMAGE_PER_CV')
                    camera_settings: Setting = Setting.objects.get(key='CAMERA_APP_SCRIPT')
                    import subprocess
                    subprocess.Popen(
                        f'cmd /k "cd /d {camera_settings.string_value}\\venv\\Scripts & activate & cd '
                        f'/d {camera_settings.string_value} & python main.py {task.module_id.id} {task.recipe_id.id} '
                        f'{image_per_cv.int_value} {path} {task.recipe_id.cv_model_path} PREDICT"')
                recipe_handler = RecipeHandler(task)
                recipe_handler.handle()
        import threading
        t = threading.Thread(target=run, args=(tasks,), daemon=True)
        t.start()

        return Response("task runner started")

    def put(self, request, *args, **kwargs):
        task_id = self.request.GET.get('task_id')
        task = Task.objects.get(pk=task_id)
        self.tasks_queue.put(task)
        return Response("task added to queue")

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.tasks_queue.put(_sentinel_stop_worker)
        return self.destroy(request, *args, **kwargs)
