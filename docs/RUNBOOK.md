# Runbook

## Open In VS Code

From PowerShell:

```powershell
cd "C:\Users\ushas\Documents\New project\ops-inbox-agent"
code .
```

If `code` is not available, open VS Code and select:

```text
File -> Open Folder -> C:\Users\ushas\Documents\New project\ops-inbox-agent
```

## Local Commands

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements-dev.txt
```

Run tests:

```powershell
python -m unittest discover -s tests
```

Run the app:

```powershell
streamlit run app.py
```

## Phase 2 Verification

Check the current branch:

```powershell
git branch --show-current
```

Inspect the sample data:

```powershell
Get-Content .\data\sample_inbox.json
```

Run all tests:

```powershell
python -m unittest discover -s tests
```
