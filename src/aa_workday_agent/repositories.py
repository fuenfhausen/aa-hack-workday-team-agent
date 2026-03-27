from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from aa_workday_agent.models import DocumentRecord, IntegrationRecord, SearchResult


def _tokenize(text: str) -> set[str]:
    return {token.strip(".,:;()[]{}\"'").lower() for token in text.split() if token.strip()}


class DocumentRepository:
    def __init__(self, path: Path) -> None:
        self._path = path
        self._documents = [DocumentRecord(**item) for item in json.loads(path.read_text(encoding="utf-8"))]

    def search(self, query: str, functional_area: str | None = None, max_results: int = 5) -> list[SearchResult]:
        query_tokens = _tokenize(query)
        results: list[SearchResult] = []
        for document in self._documents:
            if functional_area and functional_area.lower() != document.functional_area.lower():
                continue
            haystack = " ".join(
                [
                    document.title,
                    document.page_type,
                    document.functional_area,
                    document.owner,
                    " ".join(document.integration_names),
                    document.content,
                ]
            )
            score = len(query_tokens & _tokenize(haystack))
            if score == 0:
                continue
            results.append(
                SearchResult(
                    score=score,
                    title=document.title,
                    citation=document.url,
                    summary=document.content,
                )
            )
        return sorted(results, key=lambda item: item.score, reverse=True)[:max_results]

    def list_sources(self) -> list[dict[str, str]]:
        return [
            {
                "title": document.title,
                "url": document.url,
                "last_modified": document.last_modified,
                "functional_area": document.functional_area,
            }
            for document in self._documents
        ]


class IntegrationRepository:
    def __init__(self, path: Path) -> None:
        self._path = path
        self._records = [IntegrationRecord(**item) for item in json.loads(path.read_text(encoding="utf-8"))]

    def search(self, query: str, max_results: int = 5) -> list[IntegrationRecord]:
        query_tokens = _tokenize(query)
        scored: list[tuple[int, IntegrationRecord]] = []
        for record in self._records:
            haystack = " ".join(str(value) for value in asdict(record).values())
            score = len(query_tokens & _tokenize(haystack))
            if score == 0:
                continue
            scored.append((score, record))
        return [record for _, record in sorted(scored, key=lambda item: item[0], reverse=True)[:max_results]]

    def by_owner(self, owner_team: str) -> list[IntegrationRecord]:
        owner = owner_team.lower()
        return [record for record in self._records if owner in record.owner_team.lower()]

    def by_domain(self, domain: str) -> list[IntegrationRecord]:
        needle = domain.lower()
        return [record for record in self._records if needle in record.domain.lower()]

    def all_records(self) -> list[IntegrationRecord]:
        return list(self._records)