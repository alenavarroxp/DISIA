import os
import pandas as pd
import numpy as np
from datetime import datetime
from flask import Flask, jsonify
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Input, Dropout, BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.preprocessing.image import ImageDataGenerator

app = Flask(__name__)

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 5
INIT_LR = 1e-4
TRAIN_DIR = "/datasets/train"
VAL_DIR = "/datasets/val"
OUTPUT_DIR = "/compartido"


def build_model():
    base_model = EfficientNetB0(include_top=False, weights='imagenet', input_shape=(*IMG_SIZE, 3))
    base_model.trainable = False

    inputs = Input(shape=(*IMG_SIZE, 3))
    x = base_model(inputs, training=False)
    x = GlobalAveragePooling2D()(x)
    x = BatchNormalization()(x)
    x = Dropout(0.5)(x)
    x = Dense(256, activation='relu')(x)
    x = BatchNormalization()(x)
    x = Dropout(0.3)(x)

    output_transitable = Dense(1, activation='sigmoid', name='transitable')(x)
    output_inundado = Dense(1, activation='sigmoid', name='inundado')(x)

    model = Model(inputs=inputs, outputs=[output_transitable, output_inundado])
    return model


def compile_model(model):
    model.compile(
        optimizer=Adam(learning_rate=INIT_LR),
        loss={"transitable": "binary_crossentropy", "inundado": "binary_crossentropy"},
        metrics=["accuracy"]
    )
    return model


def get_data_generators():
    datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

    train_gen = datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='multi_output',  # handled as two outputs
        subset='training'
    )

    val_gen = datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='multi_output',
        subset='validation'
    )
    return train_gen, val_gen


@app.route('/train', methods=['GET'])
def train():
    try:
        model = build_model()
        model = compile_model(model)

        train_gen, val_gen = get_data_generators()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_path = os.path.join(OUTPUT_DIR, f"entrenado_effnet_{timestamp}.keras")

        checkpoint = ModelCheckpoint(model_path, save_best_only=True, monitor="val_loss", mode="min")

        model.fit(
            train_gen,
            validation_data=val_gen,
            epochs=EPOCHS,
            callbacks=[checkpoint],
            verbose=1
        )

        return jsonify({"mensaje": f"Entrenamiento finalizado. Modelo guardado en {model_path}"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
