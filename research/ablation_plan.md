# Research Ablation Plan

## Core Comparisons

1. Image-only baseline:
   - `DiagnosisAgent` only.
2. Image + severity:
   - `DiagnosisAgent` + `SeverityAgent`.
3. Image + tabular:
   - `DiagnosisAgent` + `RiskAgent`.
4. Full multimodal:
   - diagnosis + localization + severity + tabular + fusion.
5. Full multimodal + uncertainty:
   - full system with `UncertaintyAgent` and escalation policy.

## Target Questions

- How much does tabular context change triage decisions?
- Does explicit uncertainty reduce unsafe automation?
- Does localization improve interpretability without hurting throughput?
- Which modality contributes the largest gain in balanced accuracy?

## Reporting Template

- Dataset split
- Metrics: accuracy, precision, recall, F1, balanced accuracy
- Escalation metrics: uncertainty rate, urgent triage rate
- Error analysis by class
- Failure cases with heatmap overlays
