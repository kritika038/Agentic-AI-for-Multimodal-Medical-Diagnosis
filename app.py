import datetime
import json
import os
import uuid

import streamlit as st
from PIL import Image

from agents.case_orchestrator import HealthcareOrchestrator
from healthcare_types import ClinicalFeatures, PatientCase


DB_PATH = "database/patient_history.json"
orchestrator = HealthcareOrchestrator()
PAGES = ["Overview", "Imaging", "Clinical Data", "Results"]


def save_record(result):
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w") as file:
            json.dump([], file)

    with open(DB_PATH, "r") as file:
        data = json.load(file)

    clean_record = {
        "timestamp": result.case_summary["timestamp"],
        "patient_id": result.case_summary["patient_id"],
        "pneumonia_detected": result.pneumonia_detected,
        "pneumonia_confidence": result.pneumonia_confidence,
        "infection_location": result.infection_location,
        "severity_score": result.severity_score,
        "severity_level": result.severity_level,
        "diabetes_risk_detected": result.diabetes_risk_detected,
        "diabetes_risk_score": result.diabetes_risk_score,
        "multimodal_score": result.multimodal_score,
        "uncertainty_score": result.uncertainty_score,
        "uncertainty_band": result.uncertainty_band,
        "triage_level": result.triage_level,
        "warnings": result.warnings,
    }

    data.append(clean_record)

    with open(DB_PATH, "w") as file:
        json.dump(data, file, indent=4)


def init_state():
    defaults = {
        "page": "Overview",
        "uploaded_image": None,
        "patient_id": "CASE-001",
        "notes": "Shortness of breath and persistent cough.",
        "glucose": 110.0,
        "blood_pressure": 80.0,
        "skin_thickness": 20.0,
        "insulin": 85.0,
        "bmi": 24.0,
        "diabetes_pedigree": 0.4,
        "age": 40,
        "result": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def go_to(page_name):
    st.session_state.page = page_name


def build_case():
    clinical_features = ClinicalFeatures(
        glucose=float(st.session_state.glucose),
        blood_pressure=float(st.session_state.blood_pressure),
        skin_thickness=float(st.session_state.skin_thickness),
        insulin=float(st.session_state.insulin),
        bmi=float(st.session_state.bmi),
        diabetes_pedigree=float(st.session_state.diabetes_pedigree),
        age=int(st.session_state.age),
    )

    return PatientCase(
        patient_id=st.session_state.patient_id or f"CASE-{uuid.uuid4().hex[:8].upper()}",
        timestamp=datetime.datetime.now().isoformat(timespec="seconds"),
        clinical_features=clinical_features,
        image_available=st.session_state.uploaded_image is not None,
        notes=st.session_state.notes.strip(),
    )


def run_analysis():
    if st.session_state.uploaded_image is None:
        st.error("Upload a chest X-ray before running the workflow.")
        return

    patient_case = build_case()
    result = orchestrator.run_case(patient_case, st.session_state.uploaded_image)
    st.session_state.result = result
    save_record(result)
    go_to("Results")
    st.rerun()


st.set_page_config(page_title="Agentic Multimodal Healthcare AI", layout="wide")
init_state()

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at top right, rgba(37, 99, 235, 0.22), transparent 28%),
            radial-gradient(circle at top left, rgba(13, 148, 136, 0.18), transparent 24%),
            linear-gradient(180deg, #08111f 0%, #0d1727 54%, #111827 100%);
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.95), rgba(17, 24, 39, 0.88));
        border-right: 1px solid rgba(148, 163, 184, 0.16);
    }
    .hero-shell {
        padding: 2rem 2.2rem;
        border-radius: 28px;
        background: linear-gradient(135deg, rgba(8, 15, 31, 0.92), rgba(19, 38, 62, 0.88));
        border: 1px solid rgba(125, 211, 252, 0.18);
        box-shadow: 0 24px 60px rgba(2, 6, 23, 0.35);
        overflow: hidden;
    }
    .eyebrow {
        display: inline-block;
        padding: 0.35rem 0.7rem;
        border-radius: 999px;
        background: rgba(45, 212, 191, 0.12);
        border: 1px solid rgba(45, 212, 191, 0.28);
        color: #99f6e4;
        font-size: 0.78rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }
    .hero-title {
        font-size: 1.75rem;
        line-height: 1.15;
        font-weight: 800;
        color: #f8fafc;
        margin: 1rem 0 0.9rem 0;
        max-width: none;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: clip;
    }
    .hero-copy {
        max-width: 44rem;
        font-size: 1.08rem;
        color: #cbd5e1;
        line-height: 1.7;
    }
    .status-strip {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.9rem;
        margin-top: 1.6rem;
    }
    .status-card, .feature-card, .timeline-card {
        padding: 1rem 1.1rem;
        border-radius: 22px;
        background: rgba(15, 23, 42, 0.68);
        border: 1px solid rgba(148, 163, 184, 0.18);
        backdrop-filter: blur(8px);
    }
    .status-label, .feature-kicker {
        font-size: 0.78rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #7dd3fc;
    }
    .status-value {
        margin-top: 0.35rem;
        font-size: 1.35rem;
        font-weight: 700;
        color: #f8fafc;
    }
    .section-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #f8fafc;
        margin: 0 0 0.8rem 0;
    }
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 1rem;
    }
    .feature-title {
        margin-top: 0.5rem;
        font-size: 1.1rem;
        font-weight: 700;
        color: #f8fafc;
    }
    .feature-text, .timeline-text {
        color: #cbd5e1;
        line-height: 1.6;
        font-size: 0.96rem;
    }
    .timeline-stack {
        display: grid;
        gap: 0.85rem;
    }
    .timeline-step {
        display: grid;
        grid-template-columns: 44px 1fr;
        gap: 0.85rem;
        align-items: start;
    }
    .timeline-number {
        width: 44px;
        height: 44px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        color: #ecfeff;
        background: linear-gradient(135deg, #0f766e, #1d4ed8);
    }
    .panel-shell {
        padding: 1.4rem;
        border-radius: 24px;
        background: rgba(10, 17, 31, 0.72);
        border: 1px solid rgba(148, 163, 184, 0.16);
    }
    .note-card {
        padding: 1rem 1.1rem;
        border-radius: 18px;
        background: linear-gradient(135deg, rgba(30, 64, 175, 0.22), rgba(8, 47, 73, 0.52));
        border: 1px solid rgba(96, 165, 250, 0.24);
        color: #dbeafe;
        margin-bottom: 0.9rem;
    }
    @media (max-width: 980px) {
        .hero-title { font-size: 1.3rem; max-width: none; white-space: normal; overflow: visible; }
        .status-strip, .feature-grid { grid-template-columns: 1fr; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.subheader("Navigation")
    selected_page = st.radio("Go to", PAGES, index=PAGES.index(st.session_state.page))
    if selected_page != st.session_state.page:
        go_to(selected_page)
        st.rerun()

    st.markdown("**Workflow**")
    st.write("1. Overview")
    st.write("2. Imaging")
    st.write("3. Clinical Data")
    st.write("4. Results")


if st.session_state.page == "Overview":
    st.markdown(
        """
        <div class="hero-shell">
            <div class="eyebrow">Clinical AI Workspace</div>
            <div class="hero-title">Agentic AI for Multimodal Medical Diagnosis and Clinical Decision Support</div>
            <div class="hero-copy">
                Screen chest X-rays, combine radiology evidence with structured metabolic risk,
                and route uncertain cases through a staged decision pipeline instead of a single black-box prediction.
            </div>
            <div class="status-strip">
                <div class="status-card">
                    <div class="status-label">Active Agents</div>
                    <div class="status-value">8 Specialized Modules</div>
                </div>
                <div class="status-card">
                    <div class="status-label">Fusion Strategy</div>
                    <div class="status-value">Imaging + Tabular + Rules</div>
                </div>
                <div class="status-card">
                    <div class="status-label">Safety Layer</div>
                    <div class="status-value">Uncertainty Escalation</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    feature_cols = st.columns([1.4, 1.1])

    with feature_cols[0]:
        st.markdown(
            """
            <div class="feature-grid">
                <div class="feature-card">
                    <div class="feature-kicker">Imaging Intelligence</div>
                    <div class="feature-title">Radiology-first screening</div>
                    <div class="feature-text">Diagnosis, localization, and severity agents work together to flag pulmonary risk instead of returning a single flat label.</div>
                </div>
                <div class="feature-card">
                    <div class="feature-kicker">Clinical Context</div>
                    <div class="feature-title">Tabular risk integration</div>
                    <div class="feature-text">Metabolic indicators are fused with imaging evidence so the final triage output reflects more than one modality.</div>
                </div>
                <div class="feature-card">
                    <div class="feature-kicker">Research Control</div>
                    <div class="feature-title">Auditable evidence chain</div>
                    <div class="feature-text">Each agent writes explicit findings, making the system suitable for ablation studies, error analysis, and explainability review.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with feature_cols[1]:
        st.markdown(
            """
            <div class="timeline-card">
                <div class="section-title">Live Workflow</div>
                <div class="timeline-stack">
                    <div class="timeline-step">
                        <div class="timeline-number">01</div>
                        <div class="timeline-text"><strong>Intake</strong><br/>Validate X-ray quality and core patient context.</div>
                    </div>
                    <div class="timeline-step">
                        <div class="timeline-number">02</div>
                        <div class="timeline-text"><strong>Screening</strong><br/>Run pneumonia detection, severity scoring, and region localization.</div>
                    </div>
                    <div class="timeline-step">
                        <div class="timeline-number">03</div>
                        <div class="timeline-text"><strong>Fusion</strong><br/>Blend radiology and diabetes-risk evidence into a multimodal score.</div>
                    </div>
                    <div class="timeline-step">
                        <div class="timeline-number">04</div>
                        <div class="timeline-text"><strong>Escalation</strong><br/>Use uncertainty-aware triage to route ambiguous cases for review.</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    st.markdown('<div class="panel-shell">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Case Setup</div>', unsafe_allow_html=True)
    st.text_input("Patient ID", key="patient_id")
    st.text_area("Clinical notes", key="notes", height=140)
    if st.button("Continue to Imaging", use_container_width=True):
        go_to("Imaging")
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


elif st.session_state.page == "Imaging":
    st.subheader("Imaging Page")
    uploaded_file = st.file_uploader("Upload chest X-ray", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        st.session_state.uploaded_image = Image.open(uploaded_file)

    if st.session_state.uploaded_image is not None:
        st.image(st.session_state.uploaded_image, caption="Uploaded chest X-ray", width=360)

    nav_cols = st.columns(2)
    if nav_cols[0].button("Back to Overview", use_container_width=True):
        go_to("Overview")
        st.rerun()
    if nav_cols[1].button("Continue to Clinical Data", use_container_width=True):
        go_to("Clinical Data")
        st.rerun()


elif st.session_state.page == "Clinical Data":
    st.subheader("Clinical Data Page")
    left, right = st.columns(2)

    with left:
        st.number_input("Glucose", min_value=0.0, step=1.0, key="glucose")
        st.number_input("Blood Pressure", min_value=0.0, step=1.0, key="blood_pressure")
        st.number_input("Skin Thickness", min_value=0.0, step=1.0, key="skin_thickness")
        st.number_input("Insulin", min_value=0.0, step=1.0, key="insulin")

    with right:
        st.number_input("BMI", min_value=0.0, step=0.1, key="bmi")
        st.number_input("Diabetes Pedigree", min_value=0.0, step=0.01, key="diabetes_pedigree")
        st.number_input("Age", min_value=0, step=1, key="age")

    nav_cols = st.columns(3)
    if nav_cols[0].button("Back to Imaging", use_container_width=True):
        go_to("Imaging")
        st.rerun()
    if nav_cols[1].button("Run Agent Workflow", use_container_width=True):
        run_analysis()
    if nav_cols[2].button("Go to Results", use_container_width=True):
        go_to("Results")
        st.rerun()


elif st.session_state.page == "Results":
    st.subheader("Results Page")

    if st.session_state.result is None:
        st.warning("No analysis has been run yet.")
        if st.button("Go to Imaging", use_container_width=True):
            go_to("Imaging")
            st.rerun()
    else:
        result = st.session_state.result

        if st.session_state.uploaded_image is not None:
            st.image(st.session_state.uploaded_image, caption="Case X-ray", width=320)

        metric_cols = st.columns(6)
        metric_cols[0].metric("Pneumonia", "Detected" if result.pneumonia_detected else "Not detected")
        metric_cols[1].metric("X-ray Confidence", f"{result.pneumonia_confidence:.2f}%")
        metric_cols[2].metric("Severity", result.severity_level, f"{result.severity_score:.2f}/100")
        metric_cols[3].metric("Diabetes Risk", "High" if result.diabetes_risk_detected else "Low")
        metric_cols[4].metric("Fusion Score", f"{result.multimodal_score:.2f}/100")
        metric_cols[5].metric("Triage", result.triage_level)

        st.caption(f"Uncertainty: {result.uncertainty_band} ({result.uncertainty_score:.2f}/100)")

        st.subheader("Integrated Report")
        st.write(result.report)

        st.subheader("Doctor Agent Advice")
        st.write(result.doctor_advice)

        st.subheader("Evidence Chain")
        for evidence in result.evidence_chain:
            with st.expander(f"{evidence.agent_name} | confidence {evidence.confidence:.2f}"):
                st.write(evidence.summary)
                st.json(evidence.findings)

        if result.warnings:
            st.subheader("Warnings")
            for warning in result.warnings:
                st.warning(warning)

        if result.explainability and result.explainability.get("heatmap") is not None:
            st.subheader("Explainability Overlay")
            st.image(
                result.explainability["heatmap"],
                caption=result.explainability["note"],
                channels="BGR",
            )

        if st.button("Run New Case", use_container_width=True):
            st.session_state.result = None
            st.session_state.uploaded_image = None
            go_to("Overview")
            st.rerun()
