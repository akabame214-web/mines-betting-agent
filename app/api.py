from __future__ import annotations

import sqlite3
from typing import Any, Dict, List, Optional

from app.config import CONFIG
from app.decision_engine import make_recommendation
from app.ingestion import parse_log_file
from app.storage import ensure_db, insert_round, load_rounds


def health_check() -> Dict[str, Any]:
    return {"status": "ok", "message": "Acebet Mines AI Agent is running", "live_mode_enabled": CONFIG.live_mode_enabled}


def import_logs(db_path: str, file_path: str) -> Dict[str, Any]:
    records = parse_log_file(file_path)
    conn = ensure_db(db_path)
    imported = 0
    for record in records:
        insert_round(conn, record)
        imported += 1
    conn.close()
    return {"status": "ok", "imported": imported}


def fetch_rounds(db_path: str) -> List[Dict[str, Any]]:
    conn = ensure_db(db_path)
    rounds = load_rounds(conn)
    conn.close()
    return rounds


def fetch_recommendation(db_path: str, mine_count: Optional[int] = None, target_clicks: Optional[int] = None) -> Dict[str, Any]:
    mine_count = mine_count if mine_count is not None else CONFIG.default_mine_count
    target_clicks = target_clicks if target_clicks is not None else CONFIG.default_target_clicks
    recommendation = make_recommendation(
        mine_count=mine_count,
        target_clicks=target_clicks,
        current_bankroll=CONFIG.default_bankroll,
        stake=CONFIG.default_wager,
        payout_model=CONFIG.payout_model,
        warnings=["No verified Acebet live API integration exists in this build."],
    )
    return recommendation
