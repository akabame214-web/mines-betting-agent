from __future__ import annotations

from typing import Dict, Optional


def expected_net_return(wager: float, multiplier: Optional[float], survival_probability: float) -> Optional[float]:
    if wager <= 0:
        raise ValueError("wager must be positive")
    if multiplier is None:
        return None
    if multiplier <= 0:
        raise ValueError("multiplier must be > 0")
    gross_return = survival_probability * wager * multiplier
    net_return = gross_return - wager
    return net_return


def break_even_probability(multiplier: Optional[float]) -> Optional[float]:
    if multiplier is None:
        return None
    if multiplier <= 0:
        raise ValueError("multiplier must be > 0")
    return 1.0 / multiplier


def payout_lookup(payout_model: Dict[str, Dict[int, float]], mine_count: int, target_clicks: int) -> Optional[float]:
    if not payout_model:
        return None
    model_for_mine_count = payout_model.get(str(mine_count), payout_model.get(mine_count))
    if model_for_mine_count is None:
        return None
    if target_clicks in model_for_mine_count:
        return float(model_for_mine_count[target_clicks])
    return None
