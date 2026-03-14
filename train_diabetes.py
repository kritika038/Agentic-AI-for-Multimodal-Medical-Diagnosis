import pandas as pd
import pickle
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


print("Loading diabetes dataset...")

data = pd.read_csv("dataset/diabetes/diabetes.csv")

X = data.drop("Outcome", axis=1)
y = data["Outcome"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training Random Forest model...")

model = RandomForestClassifier()
model.fit(X_train, y_train)

pred = model.predict(X_test)

acc = accuracy_score(y_test, pred)

print("Accuracy:", acc)

# ensure models folder exists
if not os.path.exists("models"):
    os.mkdir("models")

with open("models/diabetes_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved at models/diabetes_model.pkl")