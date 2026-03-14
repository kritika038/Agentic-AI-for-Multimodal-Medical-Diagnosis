# Agentic AI for Multimodal Medical Diagnosis and Clinical Decision Support

## Methodology

This project follows a design-and-development research methodology for building an intelligent healthcare decision support framework that uses multimodal inputs and coordinated AI agents. The objective is to simulate a clinically relevant diagnostic workflow in which chest X-ray imaging and structured patient information are analyzed together rather than in isolation. The system is designed to support preliminary screening, multimodal reasoning, uncertainty-aware triage, and explainable reporting.

The methodology begins with multimodal data acquisition. The first input modality is chest X-ray imaging, which provides radiological evidence for pulmonary abnormality screening. The second modality is structured clinical data, including glucose, blood pressure, skin thickness, insulin, BMI, diabetes pedigree, age, and clinical notes. These inputs are collected through a staged interface so that the diagnostic workflow resembles a real clinical pathway instead of a single static form.

After data acquisition, the system performs input validation and preprocessing. The intake stage checks whether the uploaded image resembles a chest X-ray and whether the clinical variables fall within interpretable ranges. The image is then converted into grayscale and resized for downstream analysis, while the tabular values are transformed into model-ready structured features. This preprocessing stage improves compatibility across the specialized agents and ensures stable downstream execution.

The core of the methodology is the multi-agent diagnostic pipeline. The Diagnosis Agent analyzes the chest X-ray to estimate pneumonia likelihood. If suspicious findings are identified, the Localization Agent estimates the dominant affected lung region, and the Severity Agent computes a radiographic severity score from the image characteristics and model confidence. In parallel, the Risk Agent processes the structured clinical data to estimate diabetes risk. Each agent contributes a focused output and corresponding evidence, making the pipeline modular and auditable.

Once individual agent outputs are available, a Fusion Agent combines imaging evidence and structured clinical risk into a unified multimodal score. This stage is important because real medical decisions depend on combined evidence rather than one isolated prediction. After fusion, an Uncertainty Agent evaluates confidence, ambiguity, and warning signals. Cases with higher uncertainty can then be marked for clinician review, which improves safety and prevents over-reliance on automated output.

In the final stage, the Doctor Agent transforms the combined evidence into a triage recommendation, while the Report Agent produces an explainable clinical summary containing diagnostic findings, severity level, risk score, uncertainty status, and recommendations. The complete methodology therefore supports not only prediction, but also reasoning, escalation, and transparent output generation. This makes the project suitable as a research-oriented prototype in multimodal medical AI and clinical decision support.

## Flowchart

```text
Start
  |
  v
System Launch
  |
  v
Patient ID and Clinical Notes Entered
  |
  v
Chest X-ray Uploaded
  |
  v
Input Validation and Preprocessing
  |
  +-------------------------------+
  |                               |
  |  Valid Image and Data?        |
  |                               |
  +-----------+-------------------+
              |
        Yes   |   No
              |
              v
      Multimodal Agent Pipeline
              |
              v
   +---------------------------+
   |     Imaging Branch        |
   | Diagnosis Agent           |
   | Localization Agent        |
   | Severity Agent            |
   +---------------------------+
              |
              |
              v
   +---------------------------+
   |     Clinical Branch       |
   | Risk Agent                |
   | Tabular Risk Prediction   |
   +---------------------------+
              |
              v
       Fusion Agent
Combine Imaging + Clinical Evidence
              |
              v
      Uncertainty Agent
 Confidence / Escalation Check
              |
              v
         Doctor Agent
   Triage Decision Generation
              |
              v
         Report Agent
 Explainable Diagnostic Report
              |
              v
      Results Displayed in UI
              |
              v
             End
```

## Short Architecture Note

The overall architecture consists of four layers: input layer, preprocessing layer, specialized agent layer, and decision support layer. The input layer handles imaging and structured clinical values. The preprocessing layer validates and prepares both modalities. The specialized agent layer performs diagnosis, localization, severity estimation, diabetes risk prediction, multimodal fusion, and uncertainty estimation. The decision support layer generates triage advice, explainable reports, and user-facing outputs.
