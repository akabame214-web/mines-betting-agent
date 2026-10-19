from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.config import CONFIG
from app.payouts import expected_net_return, payout_lookup
from app.probability import probability_table, survival_probability


def make_recommendation(
    mine_count: int,
    target_clicks: int,
    current_bankroll: float,
    stake: float,
    payout_model: Optional[Dict[str, Dict[int, float]]] = None,
    warnings: Optional[List[str]] = None,
) -> Dict[str, Any]:
    warnings = warnings or []
    p_survive = survival_probability(mine_count, target_clicks)
    p_loss = 1.0 - p_survive
    multiplier = payout_lookup(payout_model or CONFIG.payout_model, mine_count, target_clicks)
    ev = expected_net_return(stake, multiplier, p_survive)
    action = "NO BET"
    reasons = ["Probability and bankroll risk were evaluated before recommending a next action."]
    reject_reasons = []

    if current_bankroll <= 0:
        reason = "Bankroll is depleted; no further wagers are allowed."
        reject_reasons.append(reason)
        action = "NO BET"
    elif multiplier is None:
        action = "NO BET"
        reject_reasons.append("Payout multiplier is unknown; live betting is disabled until a verified schedule is provided.")
        reasons.append("The engine can calculate exact survival probabilities, but no verified gross payout model is configured.")
    elif stake <= 0:
        action = "NO BET"
        reject_reasons.append("Stake must be positive.")
    elif ev is not None and ev <= 0:
        action = "NO BET"
        reject_reasons.append("The configured payout schedule produces a non-positive expected net return for this strategy.")
        reasons.append("No positive theoretical edge is available under the current multipliers.")
    else:
        action = "CONTINUE WITH FLAT STAKE"
        reasons.append("The tactic is mathematically admissible and preserves bankroll while respecting risk limits.")

    return {
        "action": action,
        "mine_count": mine_count,
        "target_clicks": target_clicks,
        "survival_probability": round(p_survive, 6),
        "loss_probability": round(p_loss, 6),
        "gross_multiplier": multiplier,
        "expected_net_return": round(ev, 6) if ev is not None else None,
        "proposed_stake": stake,
        "estimated_loss_if_fail": round(stake, 6),
        "current_bankroll": current_bankroll,
        "remaining_daily_loss_limit": max(0.0, current_bankroll * 0.05),
        "assumptions": [
            "Board is standard 5x5 with 25 tiles.",
            "The game uses independent, fair random placement.",
            "Historical patterns are not used to predict future mine placement.",
        ],
        "warnings": warnings,
        "reasons": reasons,
        "reject_reasons": reject_reasons,
        "confidence": 0.75 if multiplier is not None else 0.55,
    }


def build_probability_dashboard(mine_count: int, target_clicks: int, max_clicks: int = 5) -> list:
    return probability_table(mine_count, max_clicks=max_clicks)
