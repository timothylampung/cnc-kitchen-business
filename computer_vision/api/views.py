import os
import queue
import subprocess
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from business.settings import BASE_DIR
from app.api.serializers import ModuleSerializer
from app.models import Module, Recipe, Setting


@permission_classes((AllowAny,))
class CameraAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    sentinel = queue.Queue()

    def get(self, request, *args, **kwargs):
        module_id = self.kwargs['module_id']
        module = Module.objects.get(pk=module_id)
        recipe = None
        path = os.path.join(BASE_DIR, 'computer_vision\\images\\{}'.format(module.document_code))
        model_path = os.path.join(BASE_DIR, 'computer_vision\\modules\\{}'.format(module.document_code))
        camera_type = request.GET.get('camera_type')
        try:
            recipe_id = request.GET.get('recipe_id')
            recipe = Recipe.objects.get(pk=recipe_id)
            path = os.path.join(BASE_DIR,
                                'computer_vision\\images\\{}\\{}'.format(module.document_code, recipe.document_code))
            model_path = os.path.join(BASE_DIR,
                                      'computer_vision\\modules\\{}\\{}'.format(module.document_code, recipe.id))
        finally:
            pass
        os.makedirs(path, exist_ok=True)
        os.makedirs(model_path, exist_ok=True)
        # t = threading.Thread(target=stream, args=(module.wok_camera, module, path, recipe))
        # t.start()
        image_per_cv: Setting = Setting.objects.get(key='COUNT_OF_IMAGE_PER_CV')
        camera_settings: Setting = Setting.objects.get(key='CAMERA_APP_SCRIPT')
        train_ = f'cmd /k "cd /d {camera_settings.string_value}\\venv\\Scripts & activate & cd ' \
                 f'/d {camera_settings.string_value} & python main.py {module_id} {recipe_id} {image_per_cv.int_value} {path} ' \
                 f'{model_path} TRAIN"'
        print(train_)
        subprocess.Popen(train_)
        return Response(data="camera opened")

    def delete(self, request, *args, **kwargs):
        module_id = self.kwargs['module_id']
        module = Module.objects.get(pk=module_id)
        self.sentinel.put(module.document_code)
        return Response(data="camera closed")
