from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class DocumentRecord:
    id: str
    title: str
    url: str
    page_type: str
    functional_area: str
    last_modified: str
    owner: str
    integration_names: list[str]
    content: str


@dataclass(slots=True)
class IntegrationRecord:
    integration_name: str
    source_system: str
    target_system: str
    direction: str
    protocol: str
    frequency: str
    owner_team: str
    support_contact: str
    environment_coverage: list[str]
    criticality: str
    last_updated: str
    row_id: str
    domain: str


@dataclass(slots=True)
class SearchResult:
    score: int
    title: str
    citation: str
    summary: str