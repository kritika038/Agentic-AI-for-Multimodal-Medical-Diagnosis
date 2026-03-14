# import joblib
# import numpy as np

# class RiskAgent:

#     def __init__(self):
#         self.model = joblib.load("models/diabetes_model.pkl")

#     def predict_diabetes(self,data):

#         data = np.array(data).reshape(1,-1)

#         result = self.model.predict(data)[0]

#         return bool(result)
import joblib
import numpy as np
import pandas as pd

from healthcare_types import ClinicalFeatures

class RiskAgent:

    def __init__(self):
        self.model = joblib.load("models/diabetes_model.pkl")

    def _to_feature_list(self, data):
        if isinstance(data, ClinicalFeatures):
            return [
                0.0,
                data.glucose,
                data.blood_pressure,
                data.skin_thickness,
                data.insulin,
                data.bmi,
                data.diabetes_pedigree,
                data.age,
            ]

        return data

    def _to_model_input(self, data):
        values = self._to_feature_list(data)

        if hasattr(self.model, "feature_names_in_"):
            return pd.DataFrame([values], columns=list(self.model.feature_names_in_))

        return np.array(values, dtype=float).reshape(1, -1)

    def predict_diabetes(self, data):
        features = self._to_model_input(data)
        result = self.model.predict(features)[0]
        return bool(result)

    def predict_diabetes_risk(self, data):
        features = self._to_model_input(data)
        result = bool(self.model.predict(features)[0])

        if hasattr(self.model, "predict_proba"):
            score = float(self.model.predict_proba(features)[0][1] * 100.0)
        else:
            score = 75.0 if result else 25.0

        return result, round(score, 2)
