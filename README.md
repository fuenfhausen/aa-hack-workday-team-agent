# AA Regional HRIS WorkDay Team Agent

This repository contains a Microsoft Foundry hosted agent built with Microsoft Agent Framework for the American Airlines Regional HRIS WorkDay support team.

Primary knowledge sources:

- Legacy SharePoint documentation exported into a document index
- Spreadsheet-driven integration inventory normalized into structured records

Architecture details are in `docs/agent-architecture.md`.

## What Is Included

- Foundry-compatible hosted agent entrypoint
- Local tools for document retrieval and integration lookup
- Sample data for SharePoint content and integration records
- Ingestion scripts for normalizing spreadsheet and document exports
- Foundry deployment metadata and containerization files
- VS Code debug configuration for `agentdev` and Agent Inspector

## Project Layout

```text
.
├── .foundry/agent-metadata.yaml
├── .vscode/
├── agent.yaml
├── data/
├── docs/
├── scripts/
├── src/aa_workday_agent/
└── tests/
```

## Prerequisites

- Python 3.12 recommended for preview SDK compatibility
- A Foundry project endpoint
- A deployed model in that Foundry project
- Azure credentials available locally

## Environment Setup

Copy `.env.template` to `.env` and set the values for your Foundry project.

Required variables:

- `FOUNDRY_PROJECT_ENDPOINT`
- `FOUNDRY_MODEL_DEPLOYMENT_NAME`

Optional variables:

- `AGENT_NAME`
- `SHAREPOINT_DOCS_PATH`
- `INTEGRATIONS_PATH`
- `KNOWLEDGE_GAP_LOG_PATH`

## Install

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Run Locally

```powershell
.venv\Scripts\python.exe src\aa_workday_agent\app.py
```

For the preferred local debugging workflow, use the VS Code launch configuration backed by `agentdev`.

## Example Workflows

- Ask which integrations support payroll processing
- Ask for documents related to onboarding or recruiting
- Ask for both the integration facts and the supporting runbook
- Record missing knowledge through the feedback tool when the agent cannot answer confidently

## Ingestion Scripts

Normalize a CSV export of the integration spreadsheet:

```powershell
.venv\Scripts\python.exe scripts\normalize_integrations.py --input integrations.csv --output data\sample\integrations.json
```

Build a document index from exported markdown or text files:

```powershell
.venv\Scripts\python.exe scripts\build_doc_index.py --input-dir exported-docs --output data\sample\sharepoint-documents.json
```

## Notes

- Dependency versions are pinned to preview versions that match the current Microsoft Agent Framework guidance.
- The included sample data is intentionally small and should be replaced with real SharePoint and spreadsheet exports.