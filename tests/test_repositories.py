from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from aa_workday_agent.repositories import DocumentRepository, IntegrationRepository


class RepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.document_repository = DocumentRepository(ROOT / "data/sample/sharepoint-documents.json")
        self.integration_repository = IntegrationRepository(ROOT / "data/sample/integrations.json")

    def test_document_search_returns_payroll_design(self) -> None:
        results = self.document_repository.search("payroll vendor design")
        self.assertTrue(results)
        self.assertEqual(results[0].title, "Payroll Vendor Integration Design")

    def test_integration_search_returns_worker_data(self) -> None:
        results = self.integration_repository.search("worker outbound identity hub")
        self.assertTrue(results)
        self.assertEqual(results[0].integration_name, "Worker Data Outbound")

    def test_integrations_by_owner_filters_records(self) -> None:
        results = self.integration_repository.by_owner("Payroll")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].integration_name, "Payroll Vendor Export")


if __name__ == "__main__":
    unittest.main()