# app.py
# Add your Flask or FastAPI app code here
from flask import Flask, render_template, request, redirect, url_for, session
import pickle
import cv2
import numpy as np
import os

app = Flask(__name__)
app.secret_key = 'leaflence_secret_key'  # Needed for session

model = pickle.load(open("model/knn_model.pkl","rb"))

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
    result = ""
    description = ""
    image_path = ""

    if request.method == "POST":
        file = request.files["leaf"]
        image_path = "static/uploads/" + file.filename
        file.save(image_path)
        result = predict_disease(image_path)
        description = disease_info[result]
        # Store in session and redirect
        session['result'] = result
        session['description'] = description
        session['image'] = image_path
        return redirect(url_for('index'))

    # On GET, show result if present in session, then clear
    if 'result' in session:
        result = session.pop('result')
        description = session.pop('description')
        image_path = session.pop('image')

    return render_template("index.html",
                           result=result,
                           description=description,
                           image=image_path)

if __name__=="__main__":
    app.run(debug=True)