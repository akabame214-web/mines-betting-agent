from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import CONFIG
from app.decision_engine import fetch_recommendation, fetch_rounds, health_check, import_logs
from app.ingestion import parse_manual_round
from app.probability import probability_table, survival_probability
from app.storage import ensure_db, insert_round

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="Acebet Mines AI Agent", version="0.1.0")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
def read_index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
def api_health() -> Dict[str, Any]:
    return health_check()


@app.get("/api/probabilities")
def probabilities(mine_count: int = 3, max_clicks: int = 5, target_clicks: int = 2) -> List[dict]:
    if mine_count < 1 or mine_count >= 25:
        raise HTTPException(status_code=400, detail="mine_count must be between 1 and 24")
    if target_clicks < 1:
        raise HTTPException(status_code=400, detail="target_clicks must be >= 1")
    table = probability_table(mine_count, max_clicks=max_clicks)
    return [{**row, "target_clicks": target_clicks} for row in table]


@app.get("/api/survival")
def api_survival(mine_count: int = 3, target_clicks: int = 2) -> Dict[str, Any]:
    return {
        "mine_count": mine_count,
        "target_clicks": target_clicks,
        "survival_probability": survival_probability(mine_count, target_clicks),
        "loss_probability": 1.0 - survival_probability(mine_count, target_clicks),
    }


@app.post("/api/import-log")
async def api_import_log(file: UploadFile = File(...)) -> Dict[str, Any]:
    path = BASE_DIR / "tmp_uploads" / file.filename
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as handle:
        handle.write(await file.read())
    result = import_logs(str(BASE_DIR / "data" / "rounds.db"), str(path))
    return result


@app.get("/api/rounds")
def api_rounds() -> List[dict]:
    return fetch_rounds(str(BASE_DIR / "data" / "rounds.db"))


@app.get("/api/recommendation")
def api_recommendation() -> Dict[str, Any]:
    return fetch_recommendation(str(BASE_DIR / "data" / "rounds.db"), CONFIG.default_mine_count, CONFIG.default_target_clicks)


@app.post("/api/manual-round")
async def manual_round(payload: dict) -> Dict[str, Any]:
    record = payload
    conn = ensure_db(BASE_DIR / "data" / "rounds.db")
    insert_round(conn, record)
    conn.close()
    return {"status": "ok", "stored": True}
