# Ops Inbox Agent

Ops Inbox Agent is an AI-assisted operations workflow app for turning messy inbound messages into a structured review queue. The finished project will classify messages, detect urgency, extract useful details, suggest replies, and export follow-up tasks.

This repository is being built step by step as a production-minded portfolio project. It uses only free tools and runs without paid API keys.

## Current Status

Phase 1: project scaffold.

The app currently includes the clean project structure, configuration, smoke test, and placeholder Streamlit entrypoint. Feature work starts after this scaffold is approved.

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
pip install -r requirements-dev.txt
```

Run the app:

```powershell
streamlit run app.py
```

Run tests:

```powershell
python -m unittest discover -s tests
```

## Folder Structure

```text
app.py
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

First branch:

```text
feature/project-scaffold
```
