# class DoctorAgent:

#     def advice(self,pneumonia,diabetes):

#         if pneumonia and diabetes:

#             return "Possible lung infection and diabetes risk detected. Immediate medical consultation recommended."

#         elif pneumonia:

#             return "Possible pneumonia detected. Consult a chest specialist."

#         elif diabetes:

#             return "Diabetes risk detected. Lifestyle modification and medical consultation recommended."

#         else:

#             return "No major abnormalities detected. Regular health checkups advised."
class DoctorAgent:

    def triage(
        self,
        pneumonia_detected,
        pneumonia_confidence,
        diabetes_risk_detected,
        diabetes_risk_score,
        severity_level,
        multimodal_score,
        uncertainty_band,
        warnings,
    ):
        if warnings:
            return "Needs Review"

        if uncertainty_band == "High":
            return "Needs Review"

        if pneumonia_detected and severity_level == "High":
            return "Urgent"

        if multimodal_score >= 75:
            return "Urgent"

        if pneumonia_detected and pneumonia_confidence >= 50:
            return "Priority"

        if diabetes_risk_detected and diabetes_risk_score >= 70:
            return "Priority"

        return "Routine"

    def advice(
        self,
        pneumonia_detected,
        diabetes_risk_detected,
        severity_level,
        triage_level,
        uncertainty_band,
        warnings,
    ):
        if warnings:
            return "Input quality issues were detected. Repeat imaging or verify clinical values before relying on the result."

        if uncertainty_band == "High":
            return "Model uncertainty is high. Escalate to clinician review before acting on automated recommendations."

        if pneumonia_detected and diabetes_risk_detected:
            return f"Combined pulmonary and metabolic risk detected with {triage_level.lower()} triage. Consult a physician promptly."

        if pneumonia_detected:
            return f"Pulmonary abnormality detected with {severity_level.lower()} radiographic severity. Refer to a chest specialist."

        if diabetes_risk_detected:
            return "Elevated diabetes risk detected. Confirm with laboratory evaluation and physician review."

        return "No major abnormality was flagged. Continue routine clinical follow-up."
