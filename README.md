# Ops Inbox Agent

Ops Inbox Agent is an AI-assisted operations workflow app for turning messy inbound messages into a structured review queue. The finished project will classify messages, detect urgency, extract useful details, suggest replies, and export follow-up tasks.

This repository is being built step by step as a production-minded portfolio project. It uses only free tools and runs without paid API keys.

## Current Status

Phase 2: sample inbox data.

The app currently includes the clean project structure, realistic sample inbox records, a typed data loader, configuration, smoke tests, and a placeholder Streamlit entrypoint. Classification and workflow features start in the next phase.

## Tech Stack

- Python
- Streamlit
- SQLite
- pytest
- Optional local LLM support planned for a later phase

## Run Locally

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements-dev.txt
```

Run the app:

```powershell
python -m streamlit run app.py
```

Run tests:

```powershell
python -m unittest discover -s tests
```

If PowerShell says `streamlit` is not recognized, use `python -m streamlit run app.py`. If Python says `No module named streamlit`, install the dependencies again with `python -m pip install -r requirements-dev.txt` while the virtual environment is active.

## Folder Structure

```text
app.py
data/
  sample_inbox.json
src/
  ops_inbox/
    core/
    data/
    services/
    ui/
tests/
data/
docs/
```

## Development Workflow

Work is organized by feature branches. Each branch should add one meaningful capability, be tested, then merge back to `main`.

Completed branches:

```text
feature/project-scaffold
feature/sample-inbox-data
```
