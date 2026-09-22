# Spend Tracker

A simple REST API and minimal web UI for tracking personal expenses.

## Tech Stack

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* Pydantic
* Pytest
* HTML / JavaScript

## Features

* Create an expense with amount, category, note, and date
* List all expenses
* Filter expenses by category
* Filter expenses by date range
* View total spending
* View spending by category
* View current-month and previous-month spending
* Calculate month-over-month spending change
* Minimal browser-based UI for adding and viewing expenses
* Automated API tests

## Project Structure

```text
spend-tracker/
│
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
│
├── tests/
│   └── test_api.py
│
├── frontend/
│   └── index.html
│
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd spend-tracker
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Create a PostgreSQL database named:

```text
spend_tracker
```

Create a `.env` file in the project root:

```text
DATABASE_URL=postgresql+psycopg://USERNAME:PASSWORD@localhost:5432/spend_tracker
```

Replace `USERNAME` and `PASSWORD` with the local PostgreSQL credentials.

### 5. Start the API

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

### 6. Run the UI

Open:

```text
frontend/index.html
```

in a browser while the FastAPI server is running.

## API Endpoints

### Create Expense

```text
POST /expenses
```

Example request:

```json
{
  "amount": 500,
  "category": "Food",
  "note": "Lunch",
  "date": "2026-09-22"
}
```

### List Expenses

```text
GET /expenses
```

Optional filters:

```text
GET /expenses?category=Food
```

```text
GET /expenses?start_date=2026-09-01&end_date=2026-09-30
```

The category and date filters can also be combined.

### Summary

```text
GET /summary
```

Returns:

* Total spend
* Spend by category
* Current-month spend
* Previous-month spend
* Month-over-month percentage change

## Validation and Error Handling

The API validates:

* Amount must be greater than zero
* Category is required and limited to 100 characters
* Date must be a valid date
* Request payloads are validated using Pydantic

Invalid request data returns appropriate HTTP validation errors.

## Database Design

The MVP uses a single `expenses` table containing:

* `id`
* `amount`
* `category`
* `note`
* `date`
* `created_at`

The summary is calculated dynamically from the expense data rather than stored separately. This avoids duplicated summary data and keeps the implementation simple for the scope of the assignment.

Authentication and user-specific expense ownership were not included because authentication was listed as an optional bonus feature.

## Testing

Automated tests are implemented using Pytest and FastAPI's `TestClient`.

The tests cover:

* Successful expense creation
* Invalid amount validation
* Expense listing
* Category filtering
* Date-range filtering
* Summary calculation

Run the tests with:

```bash
python -m pytest
```

## Design Decisions

* **FastAPI** was selected for its simple REST API development and automatic OpenAPI documentation.
* **SQLAlchemy** provides database access through an ORM while keeping database logic separate from API logic.
* **PostgreSQL** was used as the relational database.
* **Pydantic** handles request validation and response schemas.
* **Plain HTML/JavaScript** was used for the UI to keep the frontend minimal and avoid unnecessary frontend setup.
* Summary values are calculated from the source expense data instead of maintaining a separate summary table.

## What I Would Improve With More Time
For a production-ready version, I would consider:

* User authentication using JWT
* User-specific expense data
* Pagination for large expense lists
* Database indexes on commonly filtered fields
* More comprehensive API and edge-case tests
* Better frontend error handling and validation
* Structured logging and monitoring
* Docker-based development and deployment
* CI/CD pipeline
* Deployment to a cloud platform
* Additional insights such as spending trends and unusually high expenses

## AI Usage Note

AI tools were used during development for guidance, code suggestions, debugging assistance, and documentation. The generated suggestions were reviewed, adapted, and tested as part of the implementation.
