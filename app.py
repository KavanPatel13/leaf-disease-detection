from pathlib import Path
from uuid import uuid4
import pickle
import urllib.request

import cv2
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename


app = Flask(__name__)

MODEL_DIR = Path("model")
UPLOAD_DIR = Path("static") / "uploads"
MODEL_PATH = MODEL_DIR / "knn_model.pkl"
# MODEL_URL = "https://huggingface.co/Kavan13/leaf-disease-model/resolve/main/knn_model.pkl"
MODEL_URL = "https://huggingface.co/Kavan13/leaf-disease-model-v2/resolve/main/knn_model.pkl"

NOT_APPLE_LEAF_MESSAGE = "It is not an appropriate image. Please upload an apple leaf image."
NO_DISEASE_MESSAGE = "No disease detected on this apple leaf."
INVALID_IMAGE_MESSAGE = "Invalid image file. Please upload a valid apple leaf image."

MODEL_DIR.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

if not MODEL_PATH.exists():
    print("Downloading model from HuggingFace...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)

# with MODEL_PATH.open("rb") as model_file:
#     saved_model = pickle.load(model_file)

# if isinstance(saved_model, dict):
#     model = saved_model["model"]
#     label_encoder = saved_model.get("label_encoder")
# else:
#     model = saved_model
#     label_encoder = None
model = None
label_encoder = None

def load_model_once():
    global model, label_encoder

    if model is None:
        print("Loading model once at startup...")

        with MODEL_PATH.open("rb") as f:
            saved_model = pickle.load(f)

        if isinstance(saved_model, dict):
            model = saved_model["model"]
            label_encoder = saved_model.get("label_encoder")
        else:
            model = saved_model
            label_encoder = None

disease_info = {
    "Black_rot": "Black rot is a fungal disease that causes dark lesions on apple leaves and fruit.",
    "Cedar_rust": "Cedar rust creates orange spots on leaves caused by fungal infection.",
    "Scab": "Apple scab causes dark scabby spots on leaves and fruit.",
    "Healthy": "This apple leaf looks healthy. No disease was detected.",
    "Not_Apple_Leaf": NOT_APPLE_LEAF_MESSAGE,
}

about_context = {
    "disease_classes": ["Apple Scab", "Cedar Rust", "Black Rot"],
    "workflow_steps": [
        "Image preprocessing with resize to 128x128 and normalization",
        "Feature extraction by flattening the processed image",
        "Train-test split using an 80-20 ratio",
        "KNN model training for multi-class disease classification",
        "GridSearchCV optimization to improve model selection",
    ],
    "team_members": [
        {
            "name": "Ruchit Solanki",
            "role": "Frontend, Data collection",
            "icon": "fa-laptop-code",
        },
        {
            "name": "Kavan Patel",
            "role": "Model training & evaluation",
            "icon": "fa-brain",
        },
        {
            "name": "Mann Shah",
            "role": "Testing & documentation",
            "icon": "fa-file-lines",
        },
    ],
}


def predict_disease(img_path):
    load_model_once()  
    img = cv2.imread(img_path)

    if img is None:
        return "Invalid", INVALID_IMAGE_MESSAGE, "error"

    img = cv2.resize(img, (64, 64))
    img = img / 255.0
    img = img.flatten().reshape(1, -1)

    prediction = model.predict(img)[0]

    if label_encoder is not None:
        prediction = label_encoder.inverse_transform([prediction])[0]

    prediction = str(prediction)

    if prediction == "Not_Apple_Leaf":
        return "Not an Apple Leaf", NOT_APPLE_LEAF_MESSAGE, "warning"

    if prediction == "Healthy":
        return "No Disease Detected", NO_DISEASE_MESSAGE, "success"

    return prediction, disease_info.get(prediction, "Disease detected."), "disease"


@app.route("/")
def home():
    return render_template("home.html", active_page="home")


@app.route("/predict", methods=["GET", "POST"])
def predict_page():
    context = {
        "active_page": "predict",
        "result": None,
        "description": None,
        "image": None,
        "status": None,
    }

    if request.method == "POST":
        file = request.files.get("leaf")

        if not file or not file.filename:
            context.update(
                {
                    "result": "Invalid Image",
                    "description": INVALID_IMAGE_MESSAGE,
                    "status": "error",
                }
            )
            return render_template("index.html", **context)

        filename = secure_filename(file.filename)

        if not filename:
            context.update(
                {
                    "result": "Invalid Image",
                    "description": INVALID_IMAGE_MESSAGE,
                    "status": "error",
                }
            )
            return render_template("index.html", **context)

        unique_filename = f"{uuid4().hex}_{filename}"
        saved_path = UPLOAD_DIR / unique_filename
        file.save(saved_path)

        result, description, status = predict_disease(str(saved_path))
        context.update(
            {
                "result": result,
                "description": description,
                "image": f"/static/uploads/{unique_filename}",
                "status": status,
            }
        )

    return render_template("index.html", **context)


@app.route("/about")
def about():
    return render_template("about.html", active_page="about", **about_context)


if __name__ == "__main__":
    app.run(debug=True)
