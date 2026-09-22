#Spend Tracker

A simple expense tracking application built using FastAPI, PostgreSQL and a basic HTML/JavaScript frontend.

#Tech Stack

Python / FastAPI
PostgreSQL
SQLAlchemy
Pydantic
Pytest
HTML / JavaScript

#Features

Add and view expenses
Filter expenses by category and date range
View total spending
View spending by category
View current and previous month spending
Month-over-month spending change

#Setup

Create the PostgreSQL database:

```text
spend_tracker
```

Create a `.env` file:

```text
DATABASE_URL=postgresql+psycopg://USERNAME:PASSWORD@localhost:5432/spend_tracker
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the API:

```bash
uvicorn app.main:app --reload
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

Open `frontend/index.html` in the browser to use the UI.

#APIs

| Method | Endpoint    | Purpose              |
| ------ | ----------- | -------------------- |
| POST   | `/expenses` | Add expense          |
| GET    | `/expenses` | Get expenses         |
| GET    | `/summary`  | Get spending summary |

`GET /expenses` supports `category`, `start_date` and `end_date` filters.

#Testing

Tests are written using Pytest and cover expense creation, validation, filtering and summary calculation.

Run:

```bash
python -m pytest
```

Current result: 6 tests passed

#Design

I kept the database simple with one `expenses` table. Summary values are calculated from the expense data instead of storing them separately.

Authentication was not added because it was an optional feature in the assignment.

#AI Usage

Due to the limited time available for the assignment, I used ChatGPT during development for guidance, debugging, and code suggestions. I also used it to help create the initial test cases and documentation. I reviewed, adapted, and tested the suggestions before using them in the project.