import os
from pathlib import Path

from dotenv import load_dotenv

from personalization import get_my_parameters

load_dotenv()

EMPLOYEE_ID = os.getenv("EMPLOYEE_ID", "").strip()

if not EMPLOYEE_ID:
    raise RuntimeError(
        "EMPLOYEE_ID is not configured. "
        "Copy .env.example to .env and set your team's employee ID."
    )

PARAMETERS = get_my_parameters(EMPLOYEE_ID)

CATEGORIES = PARAMETERS["categories"]
SLA_HOURS = PARAMETERS["sla_hours"]
TICKET_PREFIX = PARAMETERS["ticket_prefix"]

PRIORITIES = ["Low", "Medium", "High", "Critical"]
STATUSES = ["Open", "In Progress", "Resolved", "Closed"]

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_FILE = PROJECT_ROOT / "tickets.json"