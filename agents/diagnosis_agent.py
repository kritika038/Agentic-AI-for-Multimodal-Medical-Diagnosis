
# import numpy as np
# import cv2
# import joblib

# class DiagnosisAgent:

#     def __init__(self):
#         self.model = joblib.load("models/xray_model.pkl")

#     def analyze_xray(self, image):

#         img = np.array(image.convert("L"))
#         img = cv2.resize(img,(64,64))
#         img = img.flatten().reshape(1,-1)

#         score = self.model.decision_function(img)[0]
#         prediction = self.model.predict(img)[0]

#         confidence = min(abs(score) * 10,100)

#         if confidence < 15:
#             prediction = 0

#         pneumonia = bool(prediction)

#         return pneumonia, confidence
import numpy as np
import cv2
import joblib

class DiagnosisAgent:

    def __init__(self):
        self.model = joblib.load("models/xray_model.pkl")

    def analyze_xray(self,image):

        img = np.array(image.convert("L"))
        img = cv2.resize(img,(64,64))
        img = img.flatten().reshape(1,-1)

        score = self.model.decision_function(img)[0]
        pred = self.model.predict(img)[0]

        confidence = min(abs(score) * 10, 100)

        if confidence < 15:
            pred = 0

        pneumonia = bool(pred)

        return pneumonia, round(float(confidence), 2)
