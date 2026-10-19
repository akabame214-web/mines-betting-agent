from __future__ import annotations

import math
from typing import List, Tuple


TOTAL_TILES = 25


def _validate_inputs(mine_count: int, safe_clicks: int, total_tiles: int = TOTAL_TILES) -> None:
    if not isinstance(mine_count, int) or not isinstance(safe_clicks, int):
        raise TypeError("mine_count and safe_clicks must be integers")
    if mine_count < 0 or mine_count >= total_tiles:
        raise ValueError("mine_count must be between 0 and total_tiles - 1")
    if safe_clicks < 0 or safe_clicks > total_tiles:
        raise ValueError("safe_clicks must be between 0 and total_tiles")
    if safe_clicks > total_tiles - mine_count:
        raise ValueError("safe_clicks cannot exceed the number of safe tiles available")


def survival_probability(mine_count: int, safe_clicks: int, total_tiles: int = TOTAL_TILES) -> float:
    """Probability of surviving exactly 'safe_clicks' consecutive safe clicks without hitting a mine."""
    _validate_inputs(mine_count, safe_clicks, total_tiles)
    if safe_clicks == 0:
        return 1.0
    probability = 1.0
    for index in range(safe_clicks):
        numerator = total_tiles - mine_count - index
        denominator = total_tiles - index
        probability *= numerator / denominator
    return probability


def probability_table(mine_count: int, max_clicks: int = 5, total_tiles: int = TOTAL_TILES) -> List[dict]:
    """Return cumulative survival and loss probabilities by click number."""
    if max_clicks < 1:
        raise ValueError("max_clicks must be >= 1")
    rows: List[dict] = []
    cumulative = 1.0
    for click_number in range(1, max_clicks + 1):
        # Probability that this specific click is safe given previous successful clicks.
        conditional = 0.0
        if click_number <= total_tiles - mine_count:
            conditional = survival_probability(mine_count, click_number, total_tiles) / max(survival_probability(mine_count, click_number - 1, total_tiles), 1e-12)
        cumulative = survival_probability(mine_count, click_number, total_tiles)
        rows.append(
            {
                "click_number": click_number,
                "conditional_survival": conditional,
                "cumulative_survival": cumulative,
                "loss_by_click": 1.0 - cumulative,
            }
        )
    return rows


def loss_probability_by_click(mine_count: int, click_number: int, total_tiles: int = TOTAL_TILES) -> float:
    return 1.0 - survival_probability(mine_count, click_number, total_tiles)


def probability_summary(mine_count: int, target_clicks: int, total_tiles: int = TOTAL_TILES) -> dict:
    if target_clicks < 1:
        raise ValueError("target_clicks must be >= 1")
    p_survive = survival_probability(mine_count, target_clicks, total_tiles)
    p_loss = 1.0 - p_survive
    return {
        "mine_count": mine_count,
        "target_clicks": target_clicks,
        "survival_probability": p_survive,
        "loss_probability": p_loss,
        "survive_first_click": survival_probability(mine_count, 1, total_tiles),
        "kill_probability_by_target": p_loss,
    }


def validate_probability_inputs(mine_count: int, target_clicks: int, total_tiles: int = TOTAL_TILES) -> None:
    _validate_inputs(mine_count, target_clicks, total_tiles)


# Convenience function for probability tables across standard mine counts.
def standard_probability_tables(max_clicks: int = 5) -> dict:
    return {mine_count: probability_table(mine_count, max_clicks=max_clicks) for mine_count in (3, 5, 10)}
