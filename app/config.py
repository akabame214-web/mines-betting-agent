from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import os
from typing import Any, Dict, Iterable, List


@dataclass
class AppConfig:
    app_name: str = "Acebet Mines AI Agent"
    board_rows: int = 5
    board_columns: int = 5
    total_tiles: int = 25
    default_mine_count: int = 3
    default_target_clicks: int = 2
    default_bankroll: float = 100.0
    default_wager: float = 1.0
    max_wager_fraction: float = 0.01
    max_daily_loss_fraction: float = 0.05
    max_session_loss_fraction: float = 0.03
    max_consecutive_losses: int = 8
    max_rounds_per_session: int = 1000
    live_mode_enabled: bool = False
    payout_model: Dict[str, Dict[int, float]] = field(default_factory=dict)
    simulation_seed: int = 42

    @property
    def supported_mine_counts(self) -> Iterable[int]:
        return range(1, self.total_tiles)

    @property
    def safe_tiles(self) -> int:
        return max(self.total_tiles - self.default_mine_count, 0)


def _get_env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    try:
        return int(value)
    except ValueError:
        return default


def _get_env_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    try:
        return float(value)
    except ValueError:
        return default


def _get_env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    if value.lower() in {"1", "true", "yes", "on"}:
        return True
    if value.lower() in {"0", "false", "no", "off"}:
        return False
    return default


def load_config() -> AppConfig:
    cfg = AppConfig(
        default_mine_count=_get_env_int("APP_DEFAULT_MINE_COUNT", 3),
        default_target_clicks=_get_env_int("APP_DEFAULT_TARGET_CLICKS", 2),
        default_bankroll=_get_env_float("APP_DEFAULT_BANKROLL", 100.0),
        default_wager=_get_env_float("APP_DEFAULT_WAGER", 1.0),
        max_wager_fraction=_get_env_float("APP_MAX_WAGER_FRACTION", 0.01),
        max_daily_loss_fraction=_get_env_float("APP_MAX_DAILY_LOSS_FRACTION", 0.05),
        max_session_loss_fraction=_get_env_float("APP_MAX_SESSION_LOSS_FRACTION", 0.03),
        max_consecutive_losses=_get_env_int("APP_MAX_CONSECUTIVE_LOSSES", 8),
        max_rounds_per_session=_get_env_int("APP_MAX_ROUNDS_PER_SESSION", 1000),
        live_mode_enabled=_get_env_bool("APP_LIVE_MODE_ENABLED", False),
        simulation_seed=_get_env_int("APP_SIMULATION_SEED", 42),
    )
    # Keep payout data configurable but explicitly empty by default until a verified schedule is added.
    cfg.payout_model = {}
    if cfg.default_mine_count < 1 or cfg.default_mine_count >= cfg.total_tiles:
        raise ValueError("default_mine_count must be between 1 and 24")
    if cfg.default_target_clicks < 1:
        raise ValueError("default_target_clicks must be >= 1")
    if cfg.default_bankroll <= 0:
        raise ValueError("default_bankroll must be > 0")
    if cfg.default_wager <= 0:
        raise ValueError("default_wager must be > 0")
    return cfg


CONFIG = load_config()
