from typing import List, Tuple

from healthcare_types import ClinicalFeatures, PatientCase
from utils.xray_validator import is_xray


class IntakeAgent:

    def validate_case(self, patient_case: PatientCase, image) -> Tuple[bool, List[str]]:
        warnings: List[str] = []
        features: ClinicalFeatures = patient_case.clinical_features

        if image is None:
            warnings.append("No chest X-ray was provided.")
        elif not is_xray(image):
            warnings.append("Uploaded image does not strongly resemble a chest X-ray.")

        if features.age <= 0:
            warnings.append("Patient age should be greater than zero.")

        if features.glucose <= 0:
            warnings.append("Glucose value is missing or unrealistic.")

        if features.bmi <= 0:
            warnings.append("BMI value is missing or unrealistic.")

        if features.blood_pressure <= 0:
            warnings.append("Blood pressure value is missing or unrealistic.")

        return len(warnings) == 0, warnings
