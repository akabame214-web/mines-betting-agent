from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, model_validator


class ProbabilityRow(BaseModel):
    click_number: int
    conditional_survival: float
    cumulative_survival: float
    loss_by_click: float


class ProbabilitiesRequest(BaseModel):
    mine_count: int = Field(..., ge=1, le=24)
    target_clicks: int = Field(..., ge=1)
    max_clicks: int = Field(5, ge=1, le=25)

    @model_validator(mode="after")
    def validate_bounds(self) -> "ProbabilitiesRequest":
        if self.target_clicks > self.max_clicks:
            self.max_clicks = max(self.target_clicks, self.max_clicks)
        return self


class RoundRecord(BaseModel):
    round_id: str
    timestamp: Optional[str] = None
    mine_count: int = Field(..., ge=1, le=24)
    bet_amount: float = Field(..., gt=0)
    target_clicks: int = Field(..., ge=1)
    actual_clicks: int = Field(..., ge=0)
    success: bool = False
    gross_payout: Optional[float] = None
    net_profit: Optional[float] = None
    balance_before: Optional[float] = None
    balance_after: Optional[float] = None
    source: str = "manual"
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Recommendation(BaseModel):
    action: str
    mine_count: int
    target_clicks: int
    survival_probability: float
    loss_probability: float
    gross_multiplier: Optional[float] = None
    expected_net_return: Optional[float] = None
    proposed_stake: float
    estimated_loss_if_fail: float
    current_bankroll: float
    remaining_daily_loss_limit: float
    assumptions: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    reasons: List[str] = Field(default_factory=list)
    reject_reasons: List[str] = Field(default_factory=list)
    confidence: float = 0.0


class SimulationConfig(BaseModel):
    mine_count: int = Field(3, ge=1, le=24)
    target_clicks: int = Field(2, ge=1)
    bankroll: float = Field(100.0, gt=0)
    wager: float = Field(1.0, gt=0)
    rounds: int = Field(1000, gt=0)
    seed: int = 42
    strategy: str = "flat"


class SimulationSummary(BaseModel):
    rounds: int
    ending_bankroll: float
    total_wagered: float
    total_net_profit: float
    win_rate: float
    average_win: float
    average_loss: float
    max_drawdown: float
    longest_losing_streak: int
    probability_stop_limit_reached: float
    probability_bankroll_depletion: float
    expected_net_return: Optional[float]
    seed: int
    strategy: str
