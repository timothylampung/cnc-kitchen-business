from PyQt5.QtCore import QThread, pyqtSignal, QObject
import tensorflow as tf
from tensorflow import keras
import numpy as np


class ImagePredict(QThread):
    on_predict = pyqtSignal(str)

    def __init__(self, model, frame, group, parent=None):
        super(ImagePredict, self).__init__(parent=parent)
        self.frame = frame
        self.model = model
        self.group = group

    def run(self):
        img_array = keras.preprocessing.image.img_to_array(self.frame)
        img_array = tf.expand_dims(img_array, 0)  # Create a batch
        predictions = self.model.predict(img_array)
        score: tf.Tensor = tf.nn.softmax(predictions[0])
        results = np.array(score.__array__())
        print("This image most likely belongs to {} with a {:.2f} percent confidence.".format(
            self.group[results.argmax()].state_label, 100 * np.max(score)))
        self.on_predict.emit(f'STATE : {score} CONFIDENCE: {100 * np.max(score)}')
