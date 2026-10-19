from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class BankrollState:
    bankroll: float
    session_start: float
    daily_start: float
    max_wager_fraction: float = 0.01
    max_daily_loss_fraction: float = 0.05
    max_session_loss_fraction: float = 0.03
    max_consecutive_losses: int = 8
    max_rounds_per_session: int = 1000
    current_round_count: int = 0
    consecutive_losses: int = 0
    daily_loss: float = 0.0
    session_loss: float = 0.0
    stop_limits: List[str] = field(default_factory=list)

    def max_individual_wager(self) -> float:
        return self.bankroll * self.max_wager_fraction

    def daily_loss_limit(self) -> float:
        return self.daily_start * self.max_daily_loss_fraction

    def session_loss_limit(self) -> float:
        return self.session_start * self.max_session_loss_fraction

    def record_round(self, net_profit: float) -> dict:
        self.bankroll += net_profit
        self.current_round_count += 1
        if net_profit < 0:
            self.consecutive_losses += 1
            self.daily_loss += abs(net_profit)
            self.session_loss += abs(net_profit)
        else:
            self.consecutive_losses = 0
        warning = []
        if self.bankroll <= 0:
            self.stop_limits.append("bankroll_depleted")
            warning.append("bankroll depleted")
        if self.session_loss >= self.session_loss_limit():
            self.stop_limits.append("session_loss_limit_reached")
            warning.append("session loss limit reached")
        if self.daily_loss >= self.daily_loss_limit():
            self.stop_limits.append("daily_loss_limit_reached")
            warning.append("daily loss limit reached")
        if self.consecutive_losses >= self.max_consecutive_losses:
            self.stop_limits.append("consecutive_loss_limit_reached")
            warning.append("consecutive loss limit reached")
        return {
            "bankroll": self.bankroll,
            "daily_loss": self.daily_loss,
            "session_loss": self.session_loss,
            "consecutive_losses": self.consecutive_losses,
            "warnings": warning,
        }

    def allowed_wager(self, requested_wager: float) -> float:
        safe = min(requested_wager, self.max_individual_wager())
        if self.session_loss + safe > self.session_loss_limit():
            safe = max(0.0, self.session_loss_limit() - self.session_loss)
        if self.daily_loss + safe > self.daily_loss_limit():
            safe = max(0.0, self.daily_loss_limit() - self.daily_loss)
        if self.consecutive_losses >= self.max_consecutive_losses:
            return 0.0
        return safe
