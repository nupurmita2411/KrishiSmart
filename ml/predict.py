"""Disease prediction. Owner: Fariha

DUMMY MODE (default): no model needed. Picks a disease from the photo's bytes,
so the same photo always gives the same answer. Good enough for the demo.

REAL MODE: if ml/model.keras and ml/class_names.json exist (made by train_model.py)
and tensorflow is installed, the real CNN is used automatically.
"""
import hashlib, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(HERE, "model.keras")
CLASSES_PATH = os.path.join(HERE, "class_names.json")

DUMMY_CLASSES = ["rice_blast", "rice_brown_spot", "potato_early_blight",
                 "potato_late_blight", "tomato_early_blight", "tomato_leaf_mold",
                 "healthy_leaf"]

_model = None
_classes = None


def _try_load_real_model():
    global _model, _classes
    if _model is not None:
        return True
    if not (os.path.exists(MODEL_PATH) and os.path.exists(CLASSES_PATH)):
        return False
    try:
        from tensorflow import keras
        _model = keras.models.load_model(MODEL_PATH)
        _classes = json.load(open(CLASSES_PATH))
        return True
    except Exception as e:
        print("Real model not usable, using dummy:", e)
        return False


def predict(image_path):
    """Return {"disease_id": str, "confidence": float 0..1}"""
    if _try_load_real_model():
        import numpy as np
        from tensorflow.keras.preprocessing import image
        img = image.load_img(image_path, target_size=(128, 128))
        x = np.expand_dims(image.img_to_array(img), axis=0)  # model rescales inside
        probs = _model.predict(x, verbose=0)[0]
        i = int(np.argmax(probs))
        return {"disease_id": _classes[i], "confidence": float(probs[i])}

    # ---- dummy ----
    h = hashlib.md5(open(image_path, "rb").read()).digest()
    disease = DUMMY_CLASSES[h[0] % len(DUMMY_CLASSES)]
    confidence = 0.45 + (h[1] / 255) * 0.5   # 0.45 .. 0.95 (some results will say "not sure")
    return {"disease_id": disease, "confidence": confidence}
