from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class Settings:
    foundry_project_endpoint: str
    foundry_model_deployment_name: str
    agent_name: str
    sharepoint_docs_path: Path
    integrations_path: Path
    knowledge_gap_log_path: Path

    @classmethod
    def from_env(cls) -> "Settings":
        project_endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT", "")
        deployment_name = os.getenv("FOUNDRY_MODEL_DEPLOYMENT_NAME", "")
        if not project_endpoint:
            raise ValueError("FOUNDRY_PROJECT_ENDPOINT is required")
        if not deployment_name:
            raise ValueError("FOUNDRY_MODEL_DEPLOYMENT_NAME is required")

        return cls(
            foundry_project_endpoint=project_endpoint,
            foundry_model_deployment_name=deployment_name,
            agent_name=os.getenv("AGENT_NAME", "aa-workday-team-agent"),
            sharepoint_docs_path=Path(os.getenv("SHAREPOINT_DOCS_PATH", "data/sample/sharepoint-documents.json")),
            integrations_path=Path(os.getenv("INTEGRATIONS_PATH", "data/sample/integrations.json")),
            knowledge_gap_log_path=Path(os.getenv("KNOWLEDGE_GAP_LOG_PATH", "data/feedback/knowledge-gaps.jsonl")),
        )