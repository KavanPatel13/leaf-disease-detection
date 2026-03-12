
# app.py
# Add your Flask or FastAPI app code here
# from flask import Flask, render_template, request
# import pickle
# import cv2
# import numpy as np
# import os
# import gdown

# app = Flask(__name__)
# MODEL_PATH = "model/knn_model.pkl"
# MODEL_URL = "https://drive.google.com/uc?id=19eWEElmqKyZA2No5I3Y4FoUlZWs1iSwz"

# os.makedirs("model", exist_ok=True)
# os.makedirs("static/uploads", exist_ok=True)
# if not os.path.exists(MODEL_PATH):
#     print("Downloading model...")
#     gdown.download(MODEL_URL, MODEL_PATH, quiet=False)

# with open(MODEL_PATH, "rb") as f:
#     model = pickle.load(f)
import os
import pickle
import gdown

MODEL_PATH = "model/knn_model.pkl"
MODEL_URL = "https://drive.google.com/uc?id=1nUhIEAFvdERRVQMGoghwndXIsryreO6v"
# create model folder
os.makedirs("model", exist_ok=True)

# download model if missing
if not os.path.exists(MODEL_PATH):
    print("Downloading model...")
    gdown.download(MODEL_URL, MODEL_PATH, quiet=False)

# now load model
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)


# model = pickle.load(open("model/knn_model.pkl","rb"))
# with open("model/knn_model.pkl","rb") as f:
#     model = pickle.load(f)

disease_info = {

"Black_rot":
"Black rot is a fungal disease that causes dark lesions on apple leaves and fruit.",

"Cedar_rust":
"Cedar rust creates orange spots on leaves caused by fungal infection.",

"Scab":
"Apple scab causes dark scabby spots on leaves and fruit."
}

def predict_disease(img_path):

    img = cv2.imread(img_path)
    img = cv2.resize(img,(128,128))
    img = img/255.0

    img = img.flatten().reshape(1,-1)

    prediction = model.predict(img)

    return prediction[0]

@app.route("/",methods=["GET","POST"])

def index():

    result=""
    description=""
    image_path=""

    if request.method=="POST":

        file=request.files["leaf"]

        # image_path="static/uploads/"+file.filename
        from werkzeug.utils import secure_filename
        filename = secure_filename(file.filename)
        image_path = os.path.join("static/uploads", filename)
        file.save(image_path)

        result=predict_disease(image_path)

        description=disease_info[result]

    return render_template("index.html",
                           result=result,
                           description=description,
                           image=image_path)

if __name__=="__main__":
    app.run(debug=True)
