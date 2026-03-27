from __future__ import annotations

import json
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated

from aa_workday_agent.repositories import DocumentRepository, IntegrationRepository


class ToolContext:
    def __init__(
        self,
        document_repository: DocumentRepository,
        integration_repository: IntegrationRepository,
        knowledge_gap_log_path: Path,
    ) -> None:
        self.document_repository = document_repository
        self.integration_repository = integration_repository
        self.knowledge_gap_log_path = knowledge_gap_log_path


_CONTEXT: ToolContext | None = None


def configure_tools(context: ToolContext) -> None:
    global _CONTEXT
    _CONTEXT = context


def _require_context() -> ToolContext:
    if _CONTEXT is None:
        raise RuntimeError("Tool context has not been configured")
    return _CONTEXT


def search_sharepoint_docs(
    query: Annotated[str, "What documents or runbooks to search for."],
    functional_area: Annotated[str | None, "Optional functional area filter like Payroll or Recruiting."] = None,
    max_results: Annotated[int, "Maximum number of documents to return."] = 5,
) -> str:
    context = _require_context()
    results = context.document_repository.search(query=query, functional_area=functional_area, max_results=max_results)
    if not results:
        return "No SharePoint documents matched that query. Use the knowledge gap tool if the topic should exist."

    lines = []
    for result in results:
        lines.append(
            f"- {result.title} | citation: {result.citation} | relevance: {result.score} | summary: {result.summary}"
        )
    return "\n".join(lines)


def find_integration(
    query: Annotated[str, "Integration name, downstream system, or domain to search for."],
    max_results: Annotated[int, "Maximum number of integrations to return."] = 5,
) -> str:
    context = _require_context()
    records = context.integration_repository.search(query=query, max_results=max_results)
    if not records:
        return "No integrations matched that query."

    lines = []
    for record in records:
        lines.append(
            "- "
            f"{record.integration_name} | source: {record.source_system} | target: {record.target_system} | "
            f"protocol: {record.protocol} | frequency: {record.frequency} | owner: {record.owner_team} | "
            f"contact: {record.support_contact} | citation: spreadsheet {record.row_id}"
        )
    return "\n".join(lines)


def list_integrations_by_owner(
    owner_team: Annotated[str, "Owner team or support team name."],
) -> str:
    context = _require_context()
    records = context.integration_repository.by_owner(owner_team)
    if not records:
        return f"No integrations were found for owner team '{owner_team}'."
    return "\n".join(
        f"- {record.integration_name} | target: {record.target_system} | citation: spreadsheet {record.row_id}"
        for record in records
    )


def list_integrations_by_domain(
    domain: Annotated[str, "Business domain such as Payroll, Recruiting, or Worker Data."],
) -> str:
    context = _require_context()
    records = context.integration_repository.by_domain(domain)
    if not records:
        return f"No integrations were found for domain '{domain}'."
    return "\n".join(
        f"- {record.integration_name} | owner: {record.owner_team} | target: {record.target_system} | citation: spreadsheet {record.row_id}"
        for record in records
    )


def list_sharepoint_sources() -> str:
    context = _require_context()
    return json.dumps(context.document_repository.list_sources(), indent=2)


def report_knowledge_gap(
    question: Annotated[str, "The user question that could not be answered well."],
    context_note: Annotated[str | None, "Optional context explaining what was missing or conflicting."] = None,
) -> str:
    context = _require_context()
    context.knowledge_gap_log_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "timestamp": datetime.now(UTC).isoformat(),
        "question": question,
        "context": context_note or "",
    }
    with context.knowledge_gap_log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload) + "\n")
    return "Knowledge gap recorded for follow-up."


def create_toolset() -> list[object]:
    return [
        search_sharepoint_docs,
        find_integration,
        list_integrations_by_owner,
        list_integrations_by_domain,
        list_sharepoint_sources,
        report_knowledge_gap,
    ]