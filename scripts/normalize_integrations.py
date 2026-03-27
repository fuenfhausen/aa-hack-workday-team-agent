from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


EXPECTED_COLUMNS = {
    "integration_name",
    "source_system",
    "target_system",
    "direction",
    "protocol",
    "frequency",
    "owner_team",
    "support_contact",
    "environment_coverage",
    "criticality",
    "last_updated",
    "row_id",
    "domain",
}


def normalize_row(row: dict[str, str]) -> dict[str, object]:
    missing = EXPECTED_COLUMNS - row.keys()
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    environments = [item.strip() for item in row["environment_coverage"].split(",") if item.strip()]
    return {
        "integration_name": row["integration_name"].strip(),
        "source_system": row["source_system"].strip(),
        "target_system": row["target_system"].strip(),
        "direction": row["direction"].strip(),
        "protocol": row["protocol"].strip(),
        "frequency": row["frequency"].strip(),
        "owner_team": row["owner_team"].strip(),
        "support_contact": row["support_contact"].strip(),
        "environment_coverage": environments,
        "criticality": row["criticality"].strip(),
        "last_updated": row["last_updated"].strip(),
        "row_id": row["row_id"].strip(),
        "domain": row["domain"].strip(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize a Workday integration spreadsheet CSV export.")
    parser.add_argument("--input", required=True, help="Path to the input CSV file.")
    parser.add_argument("--output", required=True, help="Path to the output JSON file.")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    with input_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = [normalize_row(row) for row in reader]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(rows, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()