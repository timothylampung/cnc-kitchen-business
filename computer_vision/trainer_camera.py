from queue import Queue
import matplotlib as mpl
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import cv2
import qimage2ndarray
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QListWidget, \
    QListWidgetItem, \
    QInputDialog, QHBoxLayout, QProgressBar
from PyQt5 import QtCore
from keras import Model

from app.models import Module, Recipe, CookState, Setting
from computer_vision.train import ImageTrainer
from rtc_channels.data import CAMERA_DATA, CamOperation, CAMERA
from stir_fry.core.wrapper.stir_fry_sdk import StirFrySDK
from utils.utils import count_directories

mpl.use('tkagg')


class TrainerCamera(QWidget):

    def __init__(self, module: Module, path, recipe: Recipe):
        super().__init__()
        self.module = module
        self.path = path
        self.recipe = recipe

        self.setWindowTitle(module.name)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.list_widget = QListWidget()
        self.cv_result = QLabel()
        self.progress = QProgressBar()
        self.cv_progress = QProgressBar()
        self.label = QLabel('No Camera Feed')
        self.snap = QPushButton("CAPTURE COOK STATE")
        self.snap.clicked.connect(lambda: self.take_50_at_background())
        self.main_layout = QHBoxLayout()
        self.layout = QVBoxLayout()
        self.layout2 = QVBoxLayout()
        self.setFixedWidth(800)
        self.cap = cv2.VideoCapture(module.wok_camera)
        self.queue = Queue()
        self.counter = {'count': 0}
        from business.machine_settings import MODULES
        self.sdk: StirFrySDK = MODULES[module.type][module.name]['sdk']
        self.image_per_cv = Setting.objects.get(key='COUNT_OF_IMAGE_PER_CV')
        self.list_widget.itemClicked.connect(self.show_dialog)
        self.timer = QTimer()

        self.timer.timeout.connect(lambda: self.display_frame(self.queue, self.capture_images))
        self.timer.start(120)
        self.layout.addWidget(self.snap)
        self.layout.addWidget(self.progress)
        self.layout.addWidget(self.label)
        self.train = QPushButton("TRAIN")
        self.train.clicked.connect(lambda: self.train_images())
        self.layout2.addWidget(self.list_widget)
        self.layout2.addWidget(self.train)
        self.layout2.addWidget(self.cv_progress)
        self.layout2.addWidget(self.cv_result)
        self.main_layout.addLayout(self.layout)
        self.main_layout.addLayout(self.layout2)
        self.list_widget.show()
        self.setLayout(self.main_layout)
        self.populate_data()

        channel_layer = get_channel_layer()

        data = CAMERA_DATA.copy()
        data["message"]["data"]["type"] = CamOperation.CAMERA_STARTED

        async_to_sync(channel_layer.group_send)(
            module.name, {
                'type': CAMERA,
                'message': data["message"]["data"]
            }
        )

    def display_frame(self, q: Queue, on_snap):
        ret, frame = self.cap.read()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = qimage2ndarray.array2qimage(frame)
            self.label.setPixmap(QPixmap.fromImage(image).copy(300, 100, 550, 550))
            try:
                name = q.get_nowait()
                if isinstance(name, int):
                    on_snap(image, name)
            except:
                pass

    def populate_data(self):
        states = self.recipe.cook_states_of_recipe.all()
        self.list_widget.clear()
        for state in states:
            item = QListWidgetItem()
            item.setData(QtCore.Qt.UserRole, state)
            item.setText(state.state_label)
            self.list_widget.addItem(item)

    def take_50_at_background(self):
        for i in range(self.image_per_cv.int_value):
            self.queue.put(i)
        self.counter['count'] = self.counter['count'] + 1
        print('take images')

    def capture_images(self, image, c):
        copy = QPixmap.fromImage(image).copy(300, 100, 550, 550)
        import os
        class_name = f"STATE_{self.counter['count']}"
        class_path = f'{self.path}\\{class_name}\\'
        os.makedirs(class_path, exist_ok=True)
        copy.save(f"{class_path}\\frame{c}.jpg")
        self.update_progress(c)

        if c == self.image_per_cv.int_value - 1:
            print('Trying to add to list')
            cook_state, created = CookState.objects.get_or_create(state_label=f"STATE_{self.counter['count']}",
                                                                  recipe_id=self.recipe)
            print(cook_state)

            if created:
                cook_state.recipe_id = self.recipe
                cook_state.state_name = f"STATE {self.counter['count']}"
                cook_state.state_label = f"STATE_{self.counter['count']}"
                cook_state.save()

            self.populate_data()

    def show_dialog(self, state_name: QListWidgetItem):
        text, ok = QInputDialog.getText(self, f'{state_name.text()}', 'Specify state name', )
        if ok:
            state = state_name.data(QtCore.Qt.UserRole)
            if isinstance(state, CookState):
                state.state_name = text
                state.save()
                cook_states = self.recipe.cook_states_of_recipe.all()
                self.list_widget.clear()
                for s in cook_states:
                    l_item = QListWidgetItem()
                    l_item.setData(QtCore.Qt.UserRole, s)
                    l_item.setText(state.state_label)
                    self.list_widget.addItem(l_item)

    def update_progress(self, snap_number):
        if snap_number == 0 or snap_number == self.image_per_cv.int_value - 1:
            self.snap.setEnabled(True)
        else:
            self.snap.setEnabled(False)

        c = ((snap_number + 1) / 50) * 100
        self.progress.setValue(c)
        print(c)
        print(snap_number)

    def on_cv_result(self, result, number_of_class):
        self.cv_result.setText(result)
        self.recipe.number_of_class = number_of_class
        self.recipe.save()
        self.train.setEnabled(True)

    def on_cv_progress(self, result):
        if 0 < result < 100:
            self.train.setEnabled(False)
        else:
            self.train.setEnabled(True)
        self.cv_progress.setValue(result)

    def train_images(self):
        print(f'Folders in directory {count_directories(self.path)}')
        trainer = ImageTrainer(self.path, count_directories(self.path), self.module, self.recipe, parent=self)

        def started():
            print('STARTED')

        trainer.started.connect(started)
        trainer.finished.connect(started)

        trainer.progress.connect(self.on_cv_progress)
        trainer.done.connect(self.on_cv_result)
        self.train.setEnabled(False)
        trainer.start()

    def about_to_quit_handler(self):
        self.module.camera_opened = False
        self.module.save()
        self.timer.stop()
        self.progress.close()
        self.cap.release()
        self.close()
        print("about_to_quit_handler")
