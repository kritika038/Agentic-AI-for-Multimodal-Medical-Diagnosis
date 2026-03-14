# Agentic AI for Multimodal Medical Diagnosis

This project presents a healthcare AI workflow that combines chest X-ray analysis, diabetes risk estimation, agent-based orchestration, explainability, and triage-oriented reporting in one Streamlit application.

## Links

- GitHub Repository: `https://github.com/kritika038/Agentic-AI-for-Multimodal-Medical-Diagnosis`
- Live App: `https://agentic-ai-for-multimodal-medical-diagnosis-gph5znuag4uuswq6su.streamlit.app/`
- Website Source: `docs/index.html`

If the Streamlit app shows a sleep screen, wake it up and wait a short moment for the demo to load.

## What This Project Does

- Analyzes chest X-ray input for pneumonia-oriented screening
- Estimates diabetes risk from structured clinical measurements
- Uses multiple specialized agents for intake, diagnosis, localization, severity, fusion, uncertainty, doctor guidance, and reporting
- Produces a multimodal result with triage-focused guidance and explainability context

## Core Architecture

- `app.py`: Streamlit entrypoint and user interface
- `agents/case_orchestrator.py`: coordinates the full workflow
- `agents/diagnosis_agent.py`: image-based diagnosis logic
- `agents/localization_agent.py`: suspicious lung-region localization
- `agents/severity_agent.py`: severity estimation
- `agents/risk_agent.py`: diabetes-risk estimation from tabular inputs
- `agents/fusion_agent.py`: multimodal evidence fusion
- `agents/uncertainty_agent.py`: uncertainty handling and escalation logic
- `agents/doctor_agent.py`: triage guidance generation
- `agents/report_agent.py`: structured report generation
- `utils/explainability.py`: heatmap and explanation support
- `models/xray_model.pkl`: X-ray model artifact
- `models/diabetes_model.pkl`: diabetes-risk model artifact

## Local Run

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

## Streamlit Deployment

This repository is ready to deploy on Streamlit Community Cloud.

Settings to use:

- Repository: `kritika038/Agentic-AI-for-Multimodal-Medical-Diagnosis`
- Branch: `main`
- Main file path: `app.py`
- Python version: use the version in `runtime.txt`

## GitHub Pages Landing Page

This repo now includes a static landing page in `docs/`.

If you want to publish it with GitHub Pages:

1. Open the repository on GitHub.
2. Go to `Settings -> Pages`.
3. Under `Build and deployment`, choose:
   - `Source`: `Deploy from a branch`
   - `Branch`: `main`
   - `Folder`: `/docs`
4. Save.

The expected site URL will be:

```text
https://kritika038.github.io/Agentic-AI-for-Multimodal-Medical-Diagnosis/
```

## Important Note About Privacy

If you want both:

- a private repository
- and a GitHub Pages site

that depends on your GitHub plan.

According to GitHub Docs, GitHub Pages works:

- on public repositories with GitHub Free
- on public and private repositories with GitHub Pro, Team, Enterprise Cloud, or Enterprise Server

Source:
- https://docs.github.com/en/pages/getting-started-with-github-pages/using-submodules-with-github-pages

So if your account is on GitHub Free, you will usually need:

- either a public repo for GitHub Pages
- or a paid GitHub plan to keep the repo private and still use Pages

## How To Make The Repo Private

GitHub repo visibility must be changed in GitHub settings:

1. Open the repository on GitHub.
2. Go to `Settings`.
3. Scroll to `Danger Zone`.
4. Click `Change visibility`.
5. Choose `Make private`.

GitHub Docs:
- https://docs.github.com/articles/making-a-private-repository-public

## Disclaimer

This project is for education, research, and demonstration only. It is not a medical device and should not be used as a standalone diagnostic system.
