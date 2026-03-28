import os
import cv2
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC, SVC
import pickle

dataset_path = "dataset"

data = []
labels = []

# classes = ["Black_rot", "Cedar_rust", "Scab", "Healthy"]
classes = ["Black_rot", "Cedar_rust", "Scab", "Healthy", "Not_Apple_Leaf"]

for label in classes:
    folder = os.path.join(dataset_path, label)

    if not os.path.exists(folder):
        continue

    for img in os.listdir(folder):
        path = os.path.join(folder, img)

        if os.path.splitext(img)[1].lower() not in [".jpg", ".jpeg", ".png", ".bmp", ".webp"]:
            continue

        image = cv2.imread(path)

        if image is None:
            continue

        # âœ… Reduced size (less memory, faster)
        image = cv2.resize(image, (96, 96))

        # âœ… Convert to float32 (IMPORTANT)
        image = image.astype("float32") / 255.0

        data.append(image.flatten())
        labels.append(label)

# âœ… Force float32 array (IMPORTANT)
X = np.array(data, dtype="float32")
y_text = np.array(labels)

label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y_text)

print("Classes used:", list(label_encoder.classes_))
print("Total samples:", len(X))

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))

# âœ… Base model
# knn = SVC(kernel='rbf', C=1, gamma='scale')
# knn = LinearSVC(C=1)
knn = KNeighborsClassifier(n_neighbors=3, weights="distance", metric="manhattan")
knn.fit(X_train, y_train)

# accuracy = knn.score(X_test, y_test)
y_pred = knn.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Initial Model Accuracy:", accuracy * 100, "%")

# âœ… Grid parameters (same as yours)
# param_grid = {
#     "n_neighbors": [3, 5, 7, 9],
#     "weights": ["uniform", "distance"],
#     "metric": ["euclidean", "manhattan"]
# }
# param_grid = {
#     "C": [0.1, 1, 10],
#     "loss": ["hinge", "squared_hinge"]
# }
# print("Starting GridSearch... This may take time â³")

# FIX: limited jobs (avoid memory crash)
# grid_search = GridSearchCV(
#     knn,
#     param_grid,
#     cv=5,
#     scoring="accuracy",
#     verbose=2,
#     n_jobs=2   # âš ï¸ IMPORTANT (was -1)
# )

# grid_search.fit(X_train, y_train)

# print("GridSearch Completed âœ…")
# print("Best Parameters:", grid_search.best_params_)
# print("Best Cross-Validation Accuracy:", grid_search.best_score_ * 100, "%")

# # âœ… Best model evaluation
# best_knn = grid_search.best_estimator_
# grid_pre = best_knn.predict(X_test)

# print("Test Accuracy with Best Parameters:", accuracy_score(y_test, grid_pre) * 100, "%")
# print("Confusion Matrix:\n", confusion_matrix(y_test, grid_pre))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

print(
    "Classification Report:\n",
    classification_report(
        label_encoder.inverse_transform(y_test),
        label_encoder.inverse_transform(y_pred),
    ),
)
# print(
#     "Classification Report:\n",
#     classification_report(
#         label_encoder.inverse_transform(y_test),
#         label_encoder.inverse_transform(grid_pre),
#     ),
# )

#  Save model
os.makedirs("model", exist_ok=True)

# with open("model/knn_model.pkl", "wb") as f:
#     pickle.dump(
#         {
#             "model": best_knn,
#             "label_encoder": label_encoder,
#         },
#         f,
#     )
with open("model/knn_model.pkl", "wb") as f:
    pickle.dump(
        {
            "model": knn,
            "label_encoder": label_encoder,
        },
        f,
    )

print("Model saved successfully!")
