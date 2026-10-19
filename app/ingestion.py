from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence


def validate_round(record: Dict[str, Any]) -> Dict[str, Any]:
    required = ["round_id", "mine_count", "bet_amount", "target_clicks", "actual_clicks"]
    missing = [key for key in required if key not in record]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")
    if record["mine_count"] < 1 or record["mine_count"] >= 25:
        raise ValueError("mine_count must be between 1 and 24")
    if record["bet_amount"] <= 0:
        raise ValueError("bet_amount must be > 0")
    if record["target_clicks"] < 1:
        raise ValueError("target_clicks must be >= 1")
    if record["actual_clicks"] < 0:
        raise ValueError("actual_clicks must be >= 0")
    return record


def _read_csv_rows(path: str | Path) -> List[Dict[str, Any]]:
    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    return rows


def parse_log_file(path: str | Path) -> List[Dict[str, Any]]:
    file_path = Path(path)
    suffix = file_path.suffix.lower()
    if suffix == ".json":
        with open(file_path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
        if isinstance(payload, dict):
            payload = payload.get("rounds", [])
        if not isinstance(payload, list):
            raise ValueError("JSON log must be a list of rounds or contain a rounds list")
        return [validate_round(item) for item in payload]
    if suffix == ".csv":
        return [validate_round(item) for item in _read_csv_rows(file_path)]
    raise ValueError(f"Unsupported log type: {suffix}")


def parse_manual_round(record: Dict[str, Any]) -> Dict[str, Any]:
    return validate_round(record)
