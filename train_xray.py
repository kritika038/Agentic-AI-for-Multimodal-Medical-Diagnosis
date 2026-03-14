import os
import cv2
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# dataset location
dataset_path = "dataset/pneumonia/train"

categories = ["NORMAL", "PNEUMONIA"]

data = []
labels = []

img_size = 64

print("Loading images...")

for category in categories:
    path = os.path.join(dataset_path, category)
    label = categories.index(category)

    for img in os.listdir(path)[:500]:   # limit images for faster training
        try:
            img_path = os.path.join(path, img)

            image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            image = cv2.resize(image, (img_size, img_size))

            data.append(image.flatten())
            labels.append(label)

        except Exception as e:
            pass

data = np.array(data)
labels = np.array(labels)

print("Dataset loaded:", data.shape)

# split data
X_train, X_test, y_train, y_test = train_test_split(
    data,
    labels,
    test_size=0.2,
    random_state=42
)

print("Training SVM model...")

model = SVC(kernel="linear")
model.fit(X_train, y_train)

# prediction
pred = model.predict(X_test)

acc = accuracy_score(y_test, pred)

print("Accuracy:", acc)

# create models folder if it does not exist
if not os.path.exists("models"):
    os.mkdir("models")

# save model
with open("models/xray_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved successfully at models/xray_model.pkl") 