"""Validate fictional exhibition data and create reproducible recommendation files.

Uses only Python's standard library. No network requests or API keys.
"""

import argparse
import csv
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ["id", "title", "venue", "district", "genre", "start_date", "end_date", "price_krw", "is_sample"]


def load_exhibitions(path):
    """Reject incomplete rows, duplicate IDs, invalid dates and negative prices."""
    records = []
    seen = set()
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != FIELDS:
            raise ValueError("CSV columns must match: " + ", ".join(FIELDS))
        for line, row in enumerate(reader, start=2):
            if None in row or any(not str(row.get(key) or "").strip() for key in FIELDS):
                raise ValueError(f"Line {line}: missing or extra values")
            row = {key: value.strip() for key, value in row.items()}
            if row["id"] in seen:
                raise ValueError(f"Line {line}: duplicate ID")
            seen.add(row["id"])
            start = date.fromisoformat(row["start_date"])
            end = date.fromisoformat(row["end_date"])
            price = int(row["price_krw"])
            if start > end or price < 0:
                raise ValueError(f"Line {line}: invalid date range or price")
            if row["is_sample"].lower() != "true":
                raise ValueError(f"Line {line}: this demo accepts only clearly labeled sample data")
            row["price_krw"] = price
            row["is_sample"] = True
            records.append(row)
    if not records:
        raise ValueError("CSV must contain at least one exhibition")
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=ROOT / "data/exhibitions.csv")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "results")
    parser.add_argument("--as-of", type=date.fromisoformat, default=date.today(), help="YYYY-MM-DD; inclusive exhibition dates")
    parser.add_argument("--max-price", type=int, default=10000, help="Maximum admission price in KRW")
    args = parser.parse_args()
    if args.max_price < 0:
        parser.error("--max-price must be nonnegative")
    records = load_exhibitions(args.input)
    active = [row for row in records if date.fromisoformat(row["start_date"]) <= args.as_of <= date.fromisoformat(row["end_date"])]
    recommended = sorted(
        [row for row in active if row["price_krw"] <= args.max_price],
        key=lambda row: (row["price_krw"], row["end_date"], row["id"]),
    )
    summary = {
        "notice": "Fictional sample data for coursework; not real exhibition information.",
        "as_of": args.as_of.isoformat(),
        "max_price_krw": args.max_price,
        "total_count": len(records),
        "active_count": len(active),
        "recommended_count": len(recommended),
        "recommendations": recommended,
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (args.output_dir / "recommendations.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(recommended)
    (args.output_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
