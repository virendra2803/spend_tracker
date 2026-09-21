from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class ExpenseCreate(BaseModel):
    amount: float = Field(gt=0)
    category: str = Field(min_length=1, max_length=100)
    note: str | None = None
    date: date


class ExpenseResponse(BaseModel):
    id: int
    amount: float
    category: str
    note: str | None
    date: date

    model_config = ConfigDict(from_attributes=True)

class SummaryResponse(BaseModel):
    total_spend: float
    spend_by_category: dict[str, float]
    current_month_spend: float
    previous_month_spend: float
    month_over_month_change_percent: float | None