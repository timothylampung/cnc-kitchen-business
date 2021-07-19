import os
import queue
import threading

from PyQt5.QtWidgets import QWidget
from rest_framework import generics, mixins
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from business.settings import BASE_DIR
from app.api.serializers import ModuleSerializer
from app.models import Module, Recipe
from computer_vision.predictor_camera import PredictorCamera
from computer_vision.trainer_camera import TrainerCamera


def about_to_quit_handler(window: QWidget):
    window.destroy()


def stream(url, module: Module, path, recipe: Recipe):
    from PyQt5.QtWidgets import QApplication
    app = QApplication([])
    camera = PredictorCamera(module, path, recipe)
    camera.show()
    app.aboutToQuit.connect(lambda: about_to_quit_handler(camera))
    app.exec_()


@permission_classes((AllowAny,))
class CameraAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    sentinel = queue.Queue()

    def get(self, request, *args, **kwargs):
        print("RST CALLED")
        module_id = self.kwargs['module_id']
        module = Module.objects.get(pk=module_id)
        recipe = None
        path = os.path.join(BASE_DIR, 'computer_vision\\images\\{}'.format(module.document_code))
        try:
            recipe_id = request.GET.get('recipe_id')
            recipe = Recipe.objects.get(pk=recipe_id)
            path = os.path.join(BASE_DIR,
                                'computer_vision\\images\\{}\\{}'.format(module.document_code, recipe.document_code))
        finally:
            pass
        os.makedirs(path, exist_ok=True)
        t = threading.Thread(target=stream, args=(module.wok_camera, module, path, recipe))
        t.start()

        return Response(data="camera opened")

    def delete(self, request, *args, **kwargs):
        module_id = self.kwargs['module_id']
        module = Module.objects.get(pk=module_id)
        self.sentinel.put(module.document_code)
        return Response(data="camera closed")
