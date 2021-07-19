import matplotlib as mpl
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import cv2
import qimage2ndarray
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5 import QtCore
from tensorflow import keras

from app.models import Module, Recipe, CookState
from computer_vision.predict import ImagePredict
from rtc_channels.data import CAMERA_DATA, CamOperation, CAMERA
import tensorflow as tf
import numpy as np

mpl.use('tkagg')


class PredictorCamera(QWidget):

    def __init__(self, module: Module, path, recipe: Recipe):
        super().__init__()
        self.module = module
        self.path = path
        self.recipe = recipe

        self.setWindowTitle(module.name)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.cv_result = QLabel()
        self.label = QLabel('No Camera Feed')
        self.layout = QVBoxLayout()
        self.setFixedWidth(550)

        self.cap = cv2.VideoCapture(module.wok_camera)

        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.display_frame())
        self.timer.start(2000)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.cv_result)
        self.setLayout(self.layout)

        self.group = []
        for state in self.recipe.cook_states_of_recipe.all():
            if isinstance(state, CookState):
                self.group.append(state)

        channel_layer = get_channel_layer()

        self.model = tf.keras.models.load_model(recipe.cv_model_path)

        data = CAMERA_DATA.copy()
        data["message"]["data"]["type"] = CamOperation.CAMERA_STARTED

        async_to_sync(channel_layer.group_send)(
            module.name, {
                'type': CAMERA,
                'message': data["message"]["data"]
            }
        )

    def update_result(self, message):
        self.cv_result.setText(message)

    def display_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = qimage2ndarray.array2qimage(frame)
            copy = QPixmap.fromImage(image).copy(300, 100, 550, 550)
            frame = frame[100:650, 300:850]

            def started():
                print('STARTED')

            predictor = ImagePredict(self.model, frame, self.group, parent=self)
            predictor.on_predict.connect(self.update_result)
            predictor.started.connect(started)
            predictor.finished.connect(started)
            predictor.start()

            self.label.setPixmap(copy)
