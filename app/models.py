from datetime import date as DateType, datetime

from sqlalchemy import Date, DateTime, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    note: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    date: Mapped[DateType] = mapped_column(
        Date,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )