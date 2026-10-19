from __future__ import annotations

import csv
import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional


def ensure_db(path: str | Path) -> sqlite3.Connection:
    db_path = Path(path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS rounds (
            round_id TEXT PRIMARY KEY,
            timestamp TEXT,
            mine_count INTEGER,
            bet_amount REAL,
            target_clicks INTEGER,
            actual_clicks INTEGER,
            success INTEGER,
            gross_payout REAL,
            net_profit REAL,
            balance_before REAL,
            balance_after REAL,
            source TEXT,
            metadata TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    return conn


def insert_round(conn: sqlite3.Connection, record: Dict[str, Any]) -> None:
    conn.execute(
        """
        INSERT OR REPLACE INTO rounds (
            round_id, timestamp, mine_count, bet_amount, target_clicks,
            actual_clicks, success, gross_payout, net_profit,
            balance_before, balance_after, source, metadata
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            record.get("round_id"),
            record.get("timestamp"),
            record.get("mine_count"),
            record.get("bet_amount"),
            record.get("target_clicks"),
            record.get("actual_clicks"),
            int(bool(record.get("success", False))),
            record.get("gross_payout"),
            record.get("net_profit"),
            record.get("balance_before"),
            record.get("balance_after"),
            record.get("source", "manual"),
            json.dumps(record.get("metadata", {}), sort_keys=True),
        ),
    )
    conn.commit()


def load_rounds(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    rows = conn.execute(
        "SELECT round_id, timestamp, mine_count, bet_amount, target_clicks, actual_clicks, success, gross_payout, net_profit, balance_before, balance_after, source, metadata FROM rounds ORDER BY created_at"
    ).fetchall()
    outputs = []
    for row in rows:
        metadata = json.loads(row[12]) if row[12] else {}
        outputs.append(
            {
                "round_id": row[0],
                "timestamp": row[1],
                "mine_count": row[2],
                "bet_amount": row[3],
                "target_clicks": row[4],
                "actual_clicks": row[5],
                "success": bool(row[6]),
                "gross_payout": row[7],
                "net_profit": row[8],
                "balance_before": row[9],
                "balance_after": row[10],
                "source": row[11],
                "metadata": metadata,
            }
        )
    return outputs
