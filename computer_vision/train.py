from pathlib import Path
import os.path
import pandas as pd
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from sklearn.model_selection import train_test_split
import tensorflow as tf

from app.models import Module, Recipe
from business.settings import BASE_DIR


class ImageTrainer(QThread):
    done = pyqtSignal(str, int)
    progress = pyqtSignal(int)

    def __init__(self, image_dir, group_count, module: Module, recipe: Recipe, parent=None):
        super(ImageTrainer, self).__init__(parent=parent)
        self.image_dir = image_dir
        self.group_count = group_count
        self.module = module
        self.recipe = recipe

    def run(self):
        image_dir = Path(f'{self.image_dir}')

        filepaths = list(image_dir.glob(r'**/*.jpg'))
        labels = list(map(lambda x: os.path.split(os.path.split(x)[0])[1], filepaths))
        filepaths = pd.Series(filepaths, name='Filepath').astype(str)
        labels = pd.Series(labels, name='Label')
        images = pd.concat([filepaths, labels], axis=1)

        category_samples = []

        for category in images['Label'].unique():
            category_slice = images.query("Label == @category")
            category_samples.append(category_slice.sample(50, random_state=1))
        image_df = pd.concat(category_samples, axis=0).sample(frac=1.0, random_state=1).reset_index(drop=True)

        print(image_df)
        print(image_df['Label'].value_counts())

        """TEST TRAIN SPLIT"""

        train_df, test_df = train_test_split(image_df, train_size=0.7, shuffle=True, random_state=1)
        self.progress.emit(5)

        """GENERATING GENERATORS"""

        train_generator = tf.keras.preprocessing.image.ImageDataGenerator(
            preprocessing_function=tf.keras.applications.mobilenet_v2.preprocess_input,
            validation_split=0.2
        )
        self.progress.emit(15)

        test_generator = tf.keras.preprocessing.image.ImageDataGenerator(
            preprocessing_function=tf.keras.applications.mobilenet_v2.preprocess_input
        )
        self.progress.emit(20)

        train_images = train_generator.flow_from_dataframe(
            dataframe=train_df,
            x_col='Filepath',
            y_col='Label',
            target_size=(550, 550),
            color_mode='rgb',
            class_mode='categorical',
            batch_size=10,
            shuffle=True,
            seed=42,
            subset='training'
        )
        self.progress.emit(30)

        val_images = train_generator.flow_from_dataframe(
            dataframe=train_df,
            x_col='Filepath',
            y_col='Label',
            target_size=(550, 550),
            color_mode='rgb',
            class_mode='categorical',
            batch_size=10,
            shuffle=True,
            seed=42,
            subset='validation'
        )
        self.progress.emit(35)

        test_images = test_generator.flow_from_dataframe(
            dataframe=test_df,
            x_col='Filepath',
            y_col='Label',
            target_size=(550, 550),
            color_mode='rgb',
            class_mode='categorical',
            batch_size=10,
            shuffle=False
        )

        self.progress.emit(40)

        """MODELING"""

        pretrained_model = tf.keras.applications.MobileNetV2(
            input_shape=(550, 550, 3),
            include_top=False,
            weights='imagenet',
            pooling='avg'
        )
        self.progress.emit(60)

        pretrained_model.trainable = False

        inputs = pretrained_model.input

        x = tf.keras.layers.Dense(128, activation='relu')(pretrained_model.output)
        x = tf.keras.layers.Dense(128, activation='relu')(x)
        self.progress.emit(70)

        outputs = tf.keras.layers.Dense(self.group_count, activation='softmax')(x)

        model = tf.keras.Model(inputs, outputs)

        print(model.summary())

        """Training"""

        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        self.progress.emit(80)

        history = model.fit(
            train_images,
            workers=1,
            validation_data=val_images,
            epochs=100,
            steps_per_epoch=9,
            callbacks=[
                tf.keras.callbacks.EarlyStopping(
                    monitor='val_loss',
                    patience=3,
                    restore_best_weights=True
                )
            ]
        )
        self.progress.emit(85)

        """RESULTS"""
        path = os.path.join(BASE_DIR,
                            'computer_vision\\modules\\{}\\{}'.format(self.module.document_code,
                                                                      self.recipe.document_code))
        os.makedirs(path, exist_ok=True)
        results = model.evaluate(test_images, verbose=0)
        self.progress.emit(100)
        print("Test Accuracy: {:.2f}%".format(results[1] * 100))
        model.save(f'{path}/model')
        self.recipe.cv_model_path = f'{path}/model'
        self.recipe.save()
        self.done.emit("Test Accuracy: {:.2f}%".format(results[1] * 100), self.group_count, )
