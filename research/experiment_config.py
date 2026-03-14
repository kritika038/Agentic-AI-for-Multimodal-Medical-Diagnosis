EXPERIMENT_CONFIG = {
    "project_name": "agentic_multimodal_healthcare",
    "modalities": ["imaging", "tabular", "symbolic"],
    "agents": [
        "IntakeAgent",
        "DiagnosisAgent",
        "LocalizationAgent",
        "SeverityAgent",
        "RiskAgent",
        "FusionAgent",
        "UncertaintyAgent",
        "DoctorAgent",
        "ReportAgent",
    ],
    "research_tracks": {
        "baseline": "classical_ml_imaging_plus_tabular",
        "improved_imaging": "densenet_or_vit_classifier",
        "improved_localization": "weakly_supervised_cam_or_segmentation_model",
        "improved_tabular": "calibrated_gradient_boosting_or_tabnet",
        "improved_fusion": "learned_gating_or_attention_fusion",
    },
    "primary_metrics": [
        "accuracy",
        "precision",
        "recall",
        "f1",
        "balanced_accuracy",
    ],
    "secondary_metrics": [
        "uncertainty_escalation_rate",
        "triage_priority_rate",
        "modality_ablation_drop",
    ],
}
