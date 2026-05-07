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
python -m pip install -r requirements-dev.txt
```

Run tests:

```powershell
python -m unittest discover -s tests
```

Run the app:

```powershell
python -m streamlit run app.py
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

## Phase 3 Verification

Switch to the classification branch:

```powershell
git checkout feature/classification-engine
```

Install dependencies if needed:

```powershell
python -m pip install -r requirements-dev.txt
```

Run all tests:

```powershell
python -m unittest discover -s tests
```

Start the app:

```powershell
python -m streamlit run app.py
```

Open the local URL shown by Streamlit. The review queue should show sample inbox items with category, priority, owner, confidence, and matched signal terms.

## Phase 4 Verification

Switch to the entity extraction branch:

```powershell
git checkout feature/entity-extraction
```

Run all tests:

```powershell
python -m unittest discover -s tests
```

Start the app:

```powershell
python -m streamlit run app.py
```

Open the local URL shown by Streamlit. Each review queue item should now show extracted details such as sender email, phone number, invoice number, dollar amount, date, time, or operational ID when present.

## Phase 5 Verification

Switch to the urgency routing branch:

```powershell
git checkout feature/urgency-routing
```

Run all tests:

```powershell
python -m unittest discover -s tests
```

Start the app:

```powershell
python -m streamlit run app.py
```

Open the local URL shown by Streamlit. Each review card should show an urgency score, SLA target, routing reason, and manager-review warning when the item needs escalation.

## Phase 6 Verification

Switch to the reply drafting branch:

```powershell
git checkout feature/reply-drafting
```

Run all tests:

```powershell
python -m unittest discover -s tests
```

Start the app:

```powershell
python -m streamlit run app.py
```

Open the local URL shown by Streamlit. Each review card should include a `Suggested reply` expander with an editable draft, tone, and next-step guidance.

## Streamlit Troubleshooting

If this command fails:

```powershell
streamlit run app.py
```

Use this command instead:

```powershell
python -m streamlit run app.py
```

If Python says Streamlit is not installed, run:

```powershell
python -m pip install -r requirements-dev.txt
```

Then try again:

```powershell
python -m streamlit run app.py
```

## Dependency Install Troubleshooting

If pip fails while installing `pandas` and mentions Visual Studio, Meson, or `vswhere.exe`, the environment is trying to compile a package from source. Use a clean virtual environment and reinstall:

```powershell
deactivate
Remove-Item -Recurse -Force .\.venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests
python -m streamlit run app.py
```

Check your Python version:

```powershell
python --version
```

Python 3.11 or 3.12 is recommended for the smoothest Windows setup.
