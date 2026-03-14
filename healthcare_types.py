from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ClinicalFeatures:
    glucose: float
    blood_pressure: float
    skin_thickness: float
    insulin: float
    bmi: float
    diabetes_pedigree: float
    age: int


@dataclass
class PatientCase:
    patient_id: str
    timestamp: str
    clinical_features: ClinicalFeatures
    image_available: bool = True
    notes: str = ""


@dataclass
class AgentEvidence:
    agent_name: str
    summary: str
    confidence: float
    findings: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DiagnosticResult:
    case_summary: Dict[str, Any]
    pneumonia_detected: bool
    pneumonia_confidence: float
    diabetes_risk_detected: bool
    diabetes_risk_score: float
    infection_location: str
    severity_score: float
    severity_level: str
    multimodal_score: float
    uncertainty_score: float
    uncertainty_band: str
    triage_level: str
    doctor_advice: str
    report: str
    evidence_chain: List[AgentEvidence]
    warnings: List[str]
    explainability: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
