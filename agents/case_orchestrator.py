from typing import List

from healthcare_types import AgentEvidence, DiagnosticResult, PatientCase
from utils.explainability import generate_heatmap
from agents.diagnosis_agent import DiagnosisAgent
from agents.doctor_agent import DoctorAgent
from agents.fusion_agent import FusionAgent
from agents.intake_agent import IntakeAgent
from agents.localization_agent import LocalizationAgent
from agents.report_agent import ReportAgent
from agents.risk_agent import RiskAgent
from agents.severity_agent import SeverityAgent
from agents.uncertainty_agent import UncertaintyAgent


class HealthcareOrchestrator:

    def __init__(self):
        self.intake_agent = IntakeAgent()
        self.diagnosis_agent = DiagnosisAgent()
        self.localization_agent = LocalizationAgent()
        self.severity_agent = SeverityAgent()
        self.risk_agent = RiskAgent()
        self.fusion_agent = FusionAgent()
        self.uncertainty_agent = UncertaintyAgent()
        self.report_agent = ReportAgent()
        self.doctor_agent = DoctorAgent()

    def run_case(self, patient_case: PatientCase, image) -> DiagnosticResult:
        valid_case, warnings = self.intake_agent.validate_case(patient_case, image)
        evidence_chain: List[AgentEvidence] = [
            AgentEvidence(
                agent_name="IntakeAgent",
                summary="Validated multimodal inputs before downstream analysis.",
                confidence=1.0 if valid_case else 0.4,
                findings={"warnings": warnings, "image_available": image is not None},
            )
        ]

        pneumonia_detected = False
        pneumonia_confidence = 0.0
        infection_location = "Not assessed"
        severity_score = 0.0
        severity_level = "Unavailable"
        explainability = None

        if image is not None:
            pneumonia_detected, pneumonia_confidence = self.diagnosis_agent.analyze_xray(image)
            evidence_chain.append(
                AgentEvidence(
                    agent_name="DiagnosisAgent",
                    summary="Estimated pneumonia likelihood from the chest X-ray classifier.",
                    confidence=pneumonia_confidence / 100.0,
                    findings={"pneumonia_detected": pneumonia_detected},
                )
            )

            severity_score, severity_level = self.severity_agent.assess(image, pneumonia_confidence)
            evidence_chain.append(
                AgentEvidence(
                    agent_name="SeverityAgent",
                    summary="Estimated radiographic severity from opacity burden and classifier confidence.",
                    confidence=max(pneumonia_confidence / 100.0, 0.3),
                    findings={
                        "severity_score": severity_score,
                        "severity_level": severity_level,
                    },
                )
            )

            if pneumonia_detected:
                infection_location = self.localization_agent.locate_infection(image)
                evidence_chain.append(
                    AgentEvidence(
                        agent_name="LocalizationAgent",
                        summary="Localized the dominant suspicious region on the X-ray.",
                        confidence=0.65,
                        findings={"infection_location": infection_location},
                    )
                )

            heatmap = generate_heatmap(image)
            explainability = {
                "heatmap": heatmap,
                "note": "Color overlay is a heuristic explainability map, not a validated saliency method.",
            }

        diabetes_risk_detected, diabetes_risk_score = self.risk_agent.predict_diabetes_risk(
            patient_case.clinical_features
        )
        evidence_chain.append(
            AgentEvidence(
                agent_name="RiskAgent",
                summary="Estimated metabolic risk from tabular clinical features.",
                confidence=max(diabetes_risk_score / 100.0, 0.35),
                findings={
                    "diabetes_risk_detected": diabetes_risk_detected,
                    "diabetes_risk_score": diabetes_risk_score,
                },
            )
        )

        multimodal_score, multimodal_band = self.fusion_agent.fuse(
            pneumonia_confidence=pneumonia_confidence,
            severity_score=severity_score,
            diabetes_risk_score=diabetes_risk_score,
            warnings=warnings,
            clinical_features=patient_case.clinical_features,
        )
        evidence_chain.append(
            AgentEvidence(
                agent_name="FusionAgent",
                summary="Aggregated imaging and tabular evidence into a multimodal severity score.",
                confidence=max(multimodal_score / 100.0, 0.35),
                findings={
                    "multimodal_score": multimodal_score,
                    "multimodal_band": multimodal_band,
                },
            )
        )

        uncertainty_score, uncertainty_band = self.uncertainty_agent.estimate(
            pneumonia_confidence=pneumonia_confidence,
            diabetes_risk_score=diabetes_risk_score,
            multimodal_score=multimodal_score,
            warnings=warnings,
            pneumonia_detected=pneumonia_detected,
            severity_level=severity_level,
        )
        evidence_chain.append(
            AgentEvidence(
                agent_name="UncertaintyAgent",
                summary="Estimated decision uncertainty to support safe escalation.",
                confidence=max(1.0 - (uncertainty_score / 100.0), 0.2),
                findings={
                    "uncertainty_score": uncertainty_score,
                    "uncertainty_band": uncertainty_band,
                },
            )
        )

        triage_level = self.doctor_agent.triage(
            pneumonia_detected=pneumonia_detected,
            pneumonia_confidence=pneumonia_confidence,
            diabetes_risk_detected=diabetes_risk_detected,
            diabetes_risk_score=diabetes_risk_score,
            severity_level=severity_level,
            multimodal_score=multimodal_score,
            uncertainty_band=uncertainty_band,
            warnings=warnings,
        )
        doctor_advice = self.doctor_agent.advice(
            pneumonia_detected=pneumonia_detected,
            diabetes_risk_detected=diabetes_risk_detected,
            severity_level=severity_level,
            triage_level=triage_level,
            uncertainty_band=uncertainty_band,
            warnings=warnings,
        )
        report = self.report_agent.generate_report(
            patient_case=patient_case,
            pneumonia_detected=pneumonia_detected,
            pneumonia_confidence=pneumonia_confidence,
            infection_location=infection_location,
            severity_score=severity_score,
            severity_level=severity_level,
            diabetes_risk_detected=diabetes_risk_detected,
            diabetes_risk_score=diabetes_risk_score,
            multimodal_score=multimodal_score,
            uncertainty_band=uncertainty_band,
            triage_level=triage_level,
            warnings=warnings,
        )

        return DiagnosticResult(
            case_summary={
                "patient_id": patient_case.patient_id,
                "timestamp": patient_case.timestamp,
                "notes": patient_case.notes,
            },
            pneumonia_detected=pneumonia_detected,
            pneumonia_confidence=pneumonia_confidence,
            diabetes_risk_detected=diabetes_risk_detected,
            diabetes_risk_score=diabetes_risk_score,
            infection_location=infection_location,
            severity_score=severity_score,
            severity_level=severity_level,
            multimodal_score=multimodal_score,
            uncertainty_score=uncertainty_score,
            uncertainty_band=uncertainty_band,
            triage_level=triage_level,
            doctor_advice=doctor_advice,
            report=report,
            evidence_chain=evidence_chain,
            warnings=warnings,
            explainability=explainability,
        )
