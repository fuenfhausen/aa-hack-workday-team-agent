from __future__ import annotations

import argparse
import json
from pathlib import Path


def build_record(path: Path) -> dict[str, object]:
    content = path.read_text(encoding="utf-8")
    title = path.stem.replace("-", " ").title()
    return {
        "id": path.stem,
        "title": title,
        "url": f"file:///{path.as_posix()}",
        "page_type": "exported-doc",
        "functional_area": "Unknown",
        "last_modified": "",
        "owner": "",
        "integration_names": [],
        "content": content,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a simple JSON document index from exported files.")
    parser.add_argument("--input-dir", required=True, help="Directory containing markdown or text exports.")
    parser.add_argument("--output", required=True, help="Path to the output JSON file.")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_path = Path(args.output)
    records = []
    for path in sorted(input_dir.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".md", ".txt"}:
            records.append(build_record(path))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(records, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()