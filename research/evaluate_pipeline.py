import argparse
import json
import os
import sys
from collections import Counter

from PIL import Image

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from agents.case_orchestrator import HealthcareOrchestrator
from healthcare_types import ClinicalFeatures, PatientCase


def _default_case(sample_id):
    return PatientCase(
        patient_id=sample_id,
        timestamp="2026-03-12T00:00:00",
        clinical_features=ClinicalFeatures(
            glucose=110,
            blood_pressure=80,
            skin_thickness=20,
            insulin=85,
            bmi=24.0,
            diabetes_pedigree=0.4,
            age=40,
        ),
        notes="evaluation sample",
    )


def evaluate_folder(dataset_root, limit_per_class):
    orchestrator = HealthcareOrchestrator()
    results = []

    for label_name in ["NORMAL", "PNEUMONIA"]:
        label_dir = os.path.join(dataset_root, label_name)
        if not os.path.isdir(label_dir):
            continue

        image_names = sorted(os.listdir(label_dir))[:limit_per_class]
        for image_name in image_names:
            image_path = os.path.join(label_dir, image_name)
            image = Image.open(image_path)
            result = orchestrator.run_case(_default_case(image_name), image)
            predicted = int(result.pneumonia_detected)
            actual = 1 if label_name == "PNEUMONIA" else 0
            results.append(
                {
                    "image_name": image_name,
                    "actual_label": actual,
                    "predicted_label": predicted,
                    "pneumonia_confidence": result.pneumonia_confidence,
                    "severity_level": result.severity_level,
                    "multimodal_score": result.multimodal_score,
                    "uncertainty_band": result.uncertainty_band,
                    "triage_level": result.triage_level,
                }
            )

    return results


def summarize(results):
    tp = sum(1 for row in results if row["actual_label"] == 1 and row["predicted_label"] == 1)
    tn = sum(1 for row in results if row["actual_label"] == 0 and row["predicted_label"] == 0)
    fp = sum(1 for row in results if row["actual_label"] == 0 and row["predicted_label"] == 1)
    fn = sum(1 for row in results if row["actual_label"] == 1 and row["predicted_label"] == 0)
    total = max(len(results), 1)

    accuracy = (tp + tn) / total
    precision = tp / max(tp + fp, 1)
    recall = tp / max(tp + fn, 1)
    f1 = 0.0 if (precision + recall) == 0 else 2 * precision * recall / (precision + recall)
    sensitivity = recall
    specificity = tn / max(tn + fp, 1)
    balanced_accuracy = (sensitivity + specificity) / 2

    triage_distribution = Counter(row["triage_level"] for row in results)
    uncertainty_distribution = Counter(row["uncertainty_band"] for row in results)

    return {
        "num_samples": len(results),
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "balanced_accuracy": round(balanced_accuracy, 4),
        "triage_distribution": dict(triage_distribution),
        "uncertainty_distribution": dict(uncertainty_distribution),
        "confusion_matrix": {"tp": tp, "tn": tn, "fp": fp, "fn": fn},
    }


def main():
    parser = argparse.ArgumentParser(description="Evaluate the multimodal agentic pipeline.")
    parser.add_argument("--dataset-root", default="chest_xray/val")
    parser.add_argument("--limit-per-class", type=int, default=8)
    parser.add_argument("--output", default="research/evaluation_summary.json")
    args = parser.parse_args()

    results = evaluate_folder(args.dataset_root, args.limit_per_class)
    summary = summarize(results)

    payload = {"summary": summary, "samples": results}
    with open(args.output, "w") as file:
        json.dump(payload, file, indent=4)

    print(json.dumps(summary, indent=4))


if __name__ == "__main__":
    main()
