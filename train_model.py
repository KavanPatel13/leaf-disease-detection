# train_model.py
# Add your model training code here
import os
import cv2
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import pickle

dataset_path = "dataset"

data = []
labels = []

classes = ["Black_rot", "Cedar_rust", "Scab"]

for label in classes:

    folder = os.path.join(dataset_path, label)

    for img in os.listdir(folder):

        path = os.path.join(folder, img)

        image = cv2.imread(path)
        image = cv2.resize(image,(128,128))

        image = image / 255.0

        data.append(image.flatten())
        labels.append(label)

X = np.array(data)
y = np.array(labels)

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)

knn = KNeighborsClassifier(n_neighbors=5)

knn.fit(X_train,y_train)

accuracy = knn.score(X_test,y_test)

print("Model Accuracy:",accuracy*100,"%")

with open("model/knn_model.pkl","wb") as f:
    pickle.dump(knn,f)