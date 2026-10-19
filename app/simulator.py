from __future__ import annotations

import random
from typing import Dict, List

from app.probability import survival_probability


def simulate_rounds(mine_count: int, target_clicks: int, bankroll: float, wager: float, rounds: int, seed: int = 42, strategy: str = "flat") -> Dict[str, float | int]:
    random.seed(seed)
    current_bankroll = bankroll
    total_wagered = 0.0
    total_net_profit = 0.0
    wins = 0
    losses = 0
    streak = 0
    max_drawdown = 0.0
    longest_losing_streak = 0
    start_bankroll = bankroll
    drawdown = 0.0

    for _ in range(rounds):
        current_wager = wager
        if strategy == "dAlembert":
            # Risk-comparison only; do not enable by default.
            current_wager = max(0.5, wager)
        if strategy == "martingale":
            current_wager = max(0.5, wager)
        total_wagered += current_wager
        success_probability = survival_probability(mine_count, target_clicks)
        if random.random() <= success_probability:
            net_profit = current_wager * 1.0
            wins += 1
            streak = 0
            current_bankroll += net_profit
            total_net_profit += net_profit
        else:
            net_profit = -current_wager
            losses += 1
            streak += 1
            longest_losing_streak = max(longest_losing_streak, streak)
            current_bankroll += net_profit
            total_net_profit += net_profit
        if current_bankroll < start_bankroll:
            drawdown = min(drawdown, current_bankroll - start_bankroll)
        else:
            drawdown = 0.0
        max_drawdown = min(max_drawdown, drawdown)

    ending_bankroll = current_bankroll
    probability_depletion = 1.0 if ending_bankroll <= 0 else 0.0
    stop_limit_probability = 0.0
    return {
        "rounds": rounds,
        "ending_bankroll": ending_bankroll,
        "total_wagered": total_wagered,
        "total_net_profit": total_net_profit,
        "win_rate": wins / rounds if rounds else 0.0,
        "average_win": (total_net_profit / wins) if wins else 0.0,
        "average_loss": (abs(total_net_profit) / losses) if losses else 0.0,
        "max_drawdown": abs(max_drawdown),
        "longest_losing_streak": longest_losing_streak,
        "probability_stop_limit_reached": stop_limit_probability,
        "probability_bankroll_depletion": probability_depletion,
        "expected_net_return": None,
        "seed": seed,
        "strategy": strategy,
    }
