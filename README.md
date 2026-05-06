# Ops Inbox Agent

Ops Inbox Agent is an AI-assisted operations workflow app for turning messy inbound messages into a structured review queue. The finished project will classify messages, detect urgency, extract useful details, suggest replies, and export follow-up tasks.

This repository is being built step by step as a production-minded portfolio project. It uses only free tools and runs without paid API keys.

## Current Status

Phase 3: classification engine.

The app currently includes realistic sample inbox records, a typed data loader, deterministic classification, priority detection, owner routing, tests, and a Streamlit review queue preview.

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

If pip tries to compile packages on Windows and mentions Visual Studio or `vswhere.exe`, recreate the virtual environment and install again. The project keeps dependencies minimal so pip can use compatible prebuilt wheels for your Python version.

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
feature/setup-run-commands
feature/classification-engine
```
