# Agentic AI-Based Multimodal Healthcare Diagnostic System

This project is structured as a research-oriented agentic healthcare pipeline. Instead of one monolithic model, separate agents handle different subtasks and pass evidence to an orchestrator that produces the final triage decision.

## Current Agent Roles

- `IntakeAgent`: validates image quality and clinical completeness.
- `DiagnosisAgent`: screens chest X-rays for pneumonia.
- `LocalizationAgent`: estimates the dominant suspicious lung region.
- `SeverityAgent`: scores opacity burden and maps it to a severity level.
- `RiskAgent`: predicts diabetes risk from tabular clinical variables.
- `FusionAgent`: combines imaging and clinical evidence into a multimodal severity score.
- `UncertaintyAgent`: estimates confidence breakdown and routes ambiguous cases for review.
- `DoctorAgent`: converts multimodal evidence into triage guidance.
- `ReportAgent`: produces a structured research-style report.
- `HealthcareOrchestrator`: coordinates all agents and stores the evidence chain.

## Multimodal Design

The system combines:

- Imaging modality: chest X-ray classification and localization.
- Tabular modality: diabetes-risk estimation from structured clinical values.
- Symbolic reasoning layer: warnings, evidence aggregation, and triage rules.

This is a stronger research foundation because it demonstrates:

- modular agent specialization,
- multimodal data fusion,
- uncertainty-aware escalation,
- explainability output,
- triage policy design,
- auditability through an evidence chain.

## Research Assets Added

- [research/experiment_config.py](/Users/kritikabansal/Desktop/Healthcare_MultiTask_AI/research/experiment_config.py): reproducible experiment metadata.
- [research/evaluate_pipeline.py](/Users/kritikabansal/Desktop/Healthcare_MultiTask_AI/research/evaluate_pipeline.py): pipeline-level evaluation script.
- [research/ablation_plan.md](/Users/kritikabansal/Desktop/Healthcare_MultiTask_AI/research/ablation_plan.md): ablation roadmap for thesis or paper reporting.

## What Still Makes It Baseline

The project architecture is now closer to a research system, but the underlying predictive models are still classical baselines. For a strong final-year or paper-style result, replace:

- `models/xray_model.pkl` with a pretrained chest X-ray backbone plus calibration,
- `LocalizationAgent` with CAM or segmentation-based localization,
- `models/diabetes_model.pkl` with a tuned calibrated ensemble,
- heuristic fusion with learned multimodal fusion.

## Recommended Research Upgrades

To make this stronger for publication-style evaluation or a final-year project, replace the baseline models with stronger task-specific models:

- X-ray diagnosis: DenseNet121, EfficientNet, ConvNeXt, or a vision transformer fine-tuned on chest radiographs.
- Localization: U-Net, nnU-Net, YOLOv8-seg, or weakly supervised CAM/Grad-CAM localization.
- Severity scoring: ordinal regression or a multi-label opacity scoring model.
- Tabular risk modeling: XGBoost, CatBoost, TabNet, or a calibrated ensemble.
- Report generation: LLM-backed summarizer constrained by structured evidence.
- Orchestration: uncertainty-aware routing, conflict detection, and human-in-the-loop escalation.

## Suggested Research Questions

- Does multimodal fusion improve triage quality over image-only diagnosis?
- How much does localization evidence improve clinician trust?
- Can uncertainty-aware orchestration reduce false positive escalations?
- Which agent contributes most to final triage quality?

## How To Run

Use Streamlit:

```bash
streamlit run app.py
```

Or with the project virtualenv:

```bash
./venv/bin/streamlit run app.py
```

Run evaluation:

```bash
./venv/bin/python research/evaluate_pipeline.py --dataset-root chest_xray/val --limit-per-class 8
```

## GitHub And Streamlit Deployment

This project can be deployed on Streamlit Community Cloud using the GitHub repo as the source.

Required files already expected by deployment:

- `app.py` as the Streamlit entrypoint
- `requirements.txt` for Python packages
- `runtime.txt` for the Python version
- `.streamlit/config.toml` for app theme/server defaults

Recommended deployment flow:

```bash
git init
git add .
git commit -m "Initial Streamlit deployment setup"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

Then in Streamlit Community Cloud:

1. Sign in with GitHub.
2. Click `New app`.
3. Select your repository and branch `main`.
4. Set the main file path to `app.py`.
5. Deploy.

If the app later needs secrets, add them in the Streamlit Cloud app settings instead of committing them to the repository.

## Important Note

This repository is for education and research prototyping. It is not a medical device and must not be used as a standalone diagnostic system.
