# IT Helpdesk Ticket Management System

A command-line IT helpdesk application built in Python for the Python assessment.

## Features

- Raise tickets with personalized categories
- Auto-generated ticket IDs
- Priority validation
- Controlled status flow:
  `Open -> In Progress -> Resolved -> Closed`
- SLA breach detection using `datetime` and `timedelta`
- Summary by status and category
- SLA-breached ticket listing
- Filtering by category, priority, and status
- JSON persistence across program runs
- Basic OOP using a `Ticket` class
- Exception handling and custom validation errors
- Modular code organization

## Project Structure

```text
.
├── main.py
├── cli.py
├── config.py
├── models.py
├── personalization.py
├── services.py
├── storage.py
├── validators.py
├── generate_parameters.py
├── tickets.json
├── requirements.txt
├── .env.example
├── DESIGN_NOTE.md
├── PRESENTATION.md
└── tests/
    └── test_helpdesk.py
```

## Setup on Windows

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and put your employee ID in it:

```text
EMPLOYEE_ID=YOUR_REAL_EMPLOYEE_ID
```

Do not commit `.env`.

## Generate Your Personalized Parameters

```powershell
python generate_parameters.py
```

The output contains the five categories, four SLA thresholds, and ticket prefix generated from your employee ID.

## Run

```powershell
python main.py
```

## Run Tests

```powershell
python -m unittest discover -s tests -v
```

## Ticket Data

Ticket data is persisted in `tickets.json`. The application creates/updates this file automatically.


