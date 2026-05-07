# Development Log

This log records real work from the start of the project. It does not invent prior history.

## 2026-05-06

- Created the isolated project repository folder.
- Connected the project to the GitHub repository.
- Started the `feature/project-scaffold` branch.
- Added the initial Streamlit/Python project scaffold.
- Added smoke tests for metadata and folder structure.
- Started the `feature/sample-inbox-data` branch.
- Added realistic inbound messages across support, billing, sales, scheduling, vendor, account management, and complaint workflows.
- Added a typed sample inbox loader.
- Added validation tests for dataset coverage, required fields, preview formatting, and datetime parsing.
- Updated setup instructions after local Streamlit installation exposed a Windows dependency issue.
- Started the `feature/classification-engine` branch.
- Added deterministic message classification, priority detection, owner routing, confidence scoring, and reasoning terms.
- Updated the Streamlit scaffold into a review queue preview backed by sample data.
- Added tests that compare predicted labels against expected sample-data labels.
- Started the `feature/entity-extraction` branch.
- Added extraction for email addresses, phone numbers, money amounts, invoice IDs, operational IDs, dates, and times.
- Displayed extracted details in the Streamlit review queue.
- Added tests for sample-data extraction behavior and formatted entity output.
- Started the `feature/urgency-routing` branch.
- Added urgency scoring, SLA targets, manager-review flags, and routing reasons.
- Updated the Streamlit review queue with urgency progress indicators and manager review warnings.
- Added tests for critical support, complaints, vendor messages, and billing payment-run urgency.
