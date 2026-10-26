"""OPTIONAL: train a real CNN. Owner: Fariha
Only run this if you have time + a dataset (e.g. PlantVillage from Kaggle).

1. pip install tensorflow
2. Put images in ml/dataset/<class_id>/*.jpg  (folder names must match ids in
   backend/data/diseases.json, e.g. ml/dataset/rice_blast/, ml/dataset/healthy_leaf/)
3. python train_model.py
It creates ml/model.keras and ml/class_names.json, and predict.py will use them.
"""
import json, os
from tensorflow import keras

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "dataset")
SIZE = (128, 128)

train = keras.utils.image_dataset_from_directory(
    DATA, validation_split=0.2, subset="training", seed=42, image_size=SIZE, batch_size=32)
val = keras.utils.image_dataset_from_directory(
    DATA, validation_split=0.2, subset="validation", seed=42, image_size=SIZE, batch_size=32)
classes = train.class_names

model = keras.Sequential([
    keras.layers.Input(shape=SIZE + (3,)),
    keras.layers.Rescaling(1 / 255),
    keras.layers.Conv2D(16, 3, activation="relu"), keras.layers.MaxPooling2D(),
    keras.layers.Conv2D(32, 3, activation="relu"), keras.layers.MaxPooling2D(),
    keras.layers.Conv2D(64, 3, activation="relu"), keras.layers.MaxPooling2D(),
    keras.layers.Flatten(),
    keras.layers.Dense(128, activation="relu"),
    keras.layers.Dense(len(classes), activation="softmax"),
])
model.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy"])
model.fit(train, validation_data=val, epochs=5)

model.save(os.path.join(HERE, "model.keras"))
json.dump(classes, open(os.path.join(HERE, "class_names.json"), "w"))
print("Saved model. Classes:", classes)
