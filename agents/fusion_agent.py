from healthcare_types import ClinicalFeatures


class FusionAgent:

    def _clinical_risk_modifier(self, clinical_features: ClinicalFeatures) -> float:
        modifier = 0.0

        if clinical_features.age >= 60:
            modifier += 6.0
        elif clinical_features.age >= 45:
            modifier += 3.0

        if clinical_features.bmi >= 30:
            modifier += 4.0

        if clinical_features.glucose >= 180:
            modifier += 6.0
        elif clinical_features.glucose >= 126:
            modifier += 3.0

        return modifier

    def fuse(
        self,
        pneumonia_confidence,
        severity_score,
        diabetes_risk_score,
        warnings,
        clinical_features,
    ):
        clinical_modifier = self._clinical_risk_modifier(clinical_features)
        warning_penalty = min(len(warnings) * 8.0, 20.0)

        multimodal_score = (
            (0.50 * float(pneumonia_confidence))
            + (0.25 * float(severity_score))
            + (0.20 * float(diabetes_risk_score))
            + clinical_modifier
            - warning_penalty
        )
        multimodal_score = max(0.0, min(100.0, multimodal_score))

        if multimodal_score >= 75:
            band = "Critical"
        elif multimodal_score >= 55:
            band = "High"
        elif multimodal_score >= 35:
            band = "Moderate"
        else:
            band = "Low"

        return round(multimodal_score, 2), band
