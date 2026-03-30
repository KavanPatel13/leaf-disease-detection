import os
import pickle

import cv2
import numpy as np
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder


DATASET_PATH = "dataset"
MODEL_PATH = "model/knn_model.pkl"
IMAGE_SIZE = (64, 64)
PCA_COMPONENTS = 150
VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
CLASSES = ["Black_rot", "Cedar_rust", "Scab", "Healthy", "Not_Apple_Leaf"]

data = []
labels = []

for label in CLASSES:
    folder = os.path.join(DATASET_PATH, label)

    if not os.path.exists(folder):
        continue

    for img_name in os.listdir(folder):
        image_path = os.path.join(folder, img_name)

        if os.path.splitext(img_name)[1].lower() not in VALID_EXTENSIONS:
            continue

        image = cv2.imread(image_path)

        if image is None:
            continue

        image = cv2.resize(image, IMAGE_SIZE)
        image = image.astype("float32") / 255.0

        data.append(image.flatten())
        labels.append(label)

X = np.array(data, dtype="float32")
y_text = np.array(labels)

label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y_text)
class_names = [str(label) for label in label_encoder.classes_]

print("Classes used:", class_names)
print("Total samples:", len(X))

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))
print(f"Applying PCA with {PCA_COMPONENTS} components...")

pca = PCA(n_components=PCA_COMPONENTS, svd_solver="randomized", random_state=42)
X_train_pca = pca.fit_transform(X_train)
X_test_pca = pca.transform(X_test)

print(f"Explained variance retained: {pca.explained_variance_ratio_.sum() * 100:.2f}%")
print("Reduced feature size:", X_train_pca.shape[1])

base_knn = KNeighborsClassifier(n_neighbors=3, weights="distance", metric="manhattan")
base_knn.fit(X_train_pca, y_train)

base_predictions = base_knn.predict(X_test_pca)
base_accuracy = accuracy_score(y_test, base_predictions)
print(f"Initial PCA + KNN Accuracy: {base_accuracy * 100:.2f} %")

# param_grid = {
#     "n_neighbors": [3, 5, 7, 9],
#     "weights": ["uniform", "distance"],
#     "metric": ["euclidean", "manhattan"],
# }

# print("Starting GridSearchCV for PCA + KNN...")

# grid_search = GridSearchCV(
#     KNeighborsClassifier(),
#     param_grid,
#     cv=5,
#     scoring="accuracy",
#     verbose=2,
#     n_jobs=2,
# )
# grid_search.fit(X_train_pca, y_train)

# best_knn = grid_search.best_estimator_
# best_predictions = best_knn.predict(X_test_pca)
# best_accuracy = accuracy_score(y_test, best_predictions)

# print("GridSearch Completed")
# print("Best Parameters:", grid_search.best_params_)
# print(f"Best Cross-Validation Accuracy: {grid_search.best_score_ * 100:.2f} %")
# print(f"Test Accuracy with Best Parameters: {best_accuracy * 100:.2f} %")
print("Confusion Matrix:")
print(confusion_matrix(y_test, base_predictions))
print("Classification Report:")
print(classification_report(y_test, base_predictions, target_names=class_names))

os.makedirs("model", exist_ok=True)

with open(MODEL_PATH, "wb") as model_file:
    pickle.dump(
        {
            "model": base_knn,
            "label_encoder": label_encoder,
            "pca": pca,
            "image_size": IMAGE_SIZE,
            "class_names": class_names,
            "pipeline_type": "pca_knn",
        },
        model_file,
    )

print("PCA + KNN model saved successfully!")
