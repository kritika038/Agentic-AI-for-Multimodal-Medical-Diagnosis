# class ReportAgent:

#     def generate_report(self,pneumonia,diabetes,confidence):

#         if pneumonia:
#             report = f"""
# Possible pneumonia indicators detected.
# Model confidence: {round(confidence,2)}%.

# Clinical evaluation recommended.
# """
#         else:
#             report = f"""
# No pneumonia indicators detected.
# Model confidence: {round(confidence,2)}%.

# Lung fields appear normal.
# """

#         if diabetes:
#             report += "\nPatient shows elevated diabetes risk."

#         else:
#             report += "\nDiabetes risk appears normal."

#         return report
class ReportAgent:

    def generate_report(
        self,
        patient_case,
        pneumonia_detected,
        pneumonia_confidence,
        infection_location,
        severity_score,
        severity_level,
        diabetes_risk_detected,
        diabetes_risk_score,
        multimodal_score,
        uncertainty_band,
        triage_level,
        warnings,
    ):
        report_lines = [
            "Multimodal Agentic Healthcare Report",
            f"Patient ID: {patient_case.patient_id}",
            f"Study Timestamp: {patient_case.timestamp}",
            "",
            "Imaging Agent Findings:",
        ]

        if pneumonia_detected:
            report_lines.extend(
                [
                    f"- Pneumonia likelihood flagged: yes ({pneumonia_confidence:.2f}% confidence)",
                    f"- Dominant suspicious region: {infection_location}",
                    f"- Severity estimate: {severity_level} ({severity_score:.2f}/100)",
                ]
            )
        else:
            report_lines.extend(
                [
                    f"- Pneumonia likelihood flagged: no ({pneumonia_confidence:.2f}% confidence)",
                    "- No focal infection region was escalated by the localization agent.",
                ]
            )

        report_lines.extend(
            [
                "",
                "Clinical Risk Agent Findings:",
                f"- Diabetes risk flagged: {'yes' if diabetes_risk_detected else 'no'} ({diabetes_risk_score:.2f}%)",
                "",
                f"Fusion Agent Score: {multimodal_score:.2f}/100",
                f"Uncertainty Band: {uncertainty_band}",
                "",
                f"Triage Recommendation: {triage_level}",
            ]
        )

        if warnings:
            report_lines.extend(["", "Data Quality Warnings:"])
            report_lines.extend([f"- {warning}" for warning in warnings])

        report_lines.extend(
            [
                "",
                "This system is intended for research and decision support, not standalone medical diagnosis.",
            ]
        )

        return "\n".join(report_lines)
