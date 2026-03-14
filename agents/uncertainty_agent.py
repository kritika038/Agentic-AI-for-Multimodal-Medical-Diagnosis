class UncertaintyAgent:

    def estimate(
        self,
        pneumonia_confidence,
        diabetes_risk_score,
        multimodal_score,
        warnings,
        pneumonia_detected,
        severity_level,
    ):
        uncertainty = 0.0

        uncertainty += max(0.0, 50.0 - float(pneumonia_confidence)) * 0.8
        uncertainty += abs(float(diabetes_risk_score) - 50.0) * -0.2 + 10.0
        uncertainty += len(warnings) * 12.0

        if pneumonia_detected and severity_level == "Low":
            uncertainty += 8.0

        if not pneumonia_detected and multimodal_score >= 60:
            uncertainty += 10.0

        uncertainty = max(0.0, min(100.0, uncertainty))

        if uncertainty >= 60:
            band = "High"
        elif uncertainty >= 30:
            band = "Moderate"
        else:
            band = "Low"

        return round(uncertainty, 2), band
