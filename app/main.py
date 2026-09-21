from datetime import date

from fastapi import Depends, FastAPI, Query
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Spend Tracker API")


@app.get("/")
def root():
    return {"message": "Spend Tracker API is running"}


@app.post("/expenses", response_model=schemas.ExpenseResponse)
def create_expense(
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db)
):
    new_expense = models.Expense(
        amount=expense.amount,
        category=expense.category,
        note=expense.note,
        date=expense.date
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense

@app.get("/expenses", response_model=list[schemas.ExpenseResponse])
def get_expenses(
    category: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db)
):
    query = select(models.Expense)

    if category:
        query = query.where(models.Expense.category == category)

    if start_date:
        query = query.where(models.Expense.date >= start_date)

    if end_date:
        query = query.where(models.Expense.date <= end_date)

    query = query.order_by(models.Expense.date.desc())

    expenses = db.scalars(query).all()

    return expenses

@app.get("/summary", response_model=schemas.SummaryResponse)
def get_summary(
    db: Session = Depends(get_db)
):
    today = date.today()

    current_month_start = today.replace(day=1)

    if current_month_start.month == 1:
        previous_month_start = current_month_start.replace(
            year=current_month_start.year - 1,
            month=12
        )
    else:
        previous_month_start = current_month_start.replace(
            month=current_month_start.month - 1
        )

    # Total spend
    total_spend = db.scalar(
        select(func.coalesce(func.sum(models.Expense.amount), 0))
    )

    # Spend by category
    category_rows = db.execute(
        select(
            models.Expense.category,
            func.sum(models.Expense.amount)
        )
        .group_by(models.Expense.category)
    ).all()

    spend_by_category = {
        category: float(total)
        for category, total in category_rows
    }

    # Current month spend
    current_month_spend = db.scalar(
        select(func.coalesce(func.sum(models.Expense.amount), 0))
        .where(models.Expense.date >= current_month_start)
        .where(models.Expense.date <= today)
    )

    # Previous month spend
    previous_month_spend = db.scalar(
        select(func.coalesce(func.sum(models.Expense.amount), 0))
        .where(models.Expense.date >= previous_month_start)
        .where(models.Expense.date < current_month_start)
    )

    current_month_spend = float(current_month_spend)
    previous_month_spend = float(previous_month_spend)

    # Month-over-month percentage
    if previous_month_spend == 0:
        month_over_month_change_percent = None
    else:
        month_over_month_change_percent = (
            (current_month_spend - previous_month_spend)
            / previous_month_spend
        ) * 100

    return {
        "total_spend": float(total_spend),
        "spend_by_category": spend_by_category,
        "current_month_spend": current_month_spend,
        "previous_month_spend": previous_month_spend,
        "month_over_month_change_percent": month_over_month_change_percent
    }