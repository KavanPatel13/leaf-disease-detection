# ==============================
# Imports
# ==============================
from flask import Flask, render_template, request
import pickle
import cv2
import numpy as np
import os
import urllib.request
from werkzeug.utils import secure_filename


# ==============================
# Flask app
# ==============================
app = Flask(__name__)


# ==============================
# Model download from HuggingFace
# ==============================

MODEL_PATH = "model/knn_model.pkl"
MODEL_URL = "https://huggingface.co/Kavan13/leaf-disease-model/resolve/main/knn_model.pkl"

# Create folders if not exist
os.makedirs("model", exist_ok=True)
os.makedirs("static/uploads", exist_ok=True)

# Download model only if missing
if not os.path.exists(MODEL_PATH):
    print("Downloading model from HuggingFace...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)


# ==============================
# Load model
# ==============================
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)


# ==============================
# Disease descriptions
# ==============================
disease_info = {
    "Black_rot": "Black rot is a fungal disease that causes dark lesions on apple leaves and fruit.",
    "Cedar_rust": "Cedar rust creates orange spots on leaves caused by fungal infection.",
    "Scab": "Apple scab causes dark scabby spots on leaves and fruit."
}


# ==============================
# Prediction function
# ==============================
def predict_disease(img_path):

    img = cv2.imread(img_path)
    img = cv2.resize(img, (128,128))
    img = img / 255.0

    img = img.flatten().reshape(1,-1)

    prediction = model.predict(img)

    return prediction[0]


# ==============================
# Main Route
# ==============================
@app.route("/", methods=["GET","POST"])
def index():

    result = ""
    description = ""
    image_path = ""

    if request.method == "POST":

        file = request.files["leaf"]

        filename = secure_filename(file.filename)
        image_path = os.path.join("static/uploads", filename)
        file.save(image_path)

        result = predict_disease(image_path)
        description = disease_info.get(result, "Unknown disease")

    return render_template(
        "index.html",
        result=result,
        description=description,
        image=image_path
    )


# ==============================
# Local run (NOT used on Render)
# ==============================
# Render uses: gunicorn app:app
# This block only runs when you start locally with:
# python app.py

# if __name__ == "__main__":
#     app.run(debug=True)