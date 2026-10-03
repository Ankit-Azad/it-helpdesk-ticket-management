import json
from pathlib import Path
from typing import Iterable, List, Union

from models import Ticket


class StorageError(Exception):
    """Raised when ticket persistence fails."""


def save_tickets(
    tickets: Iterable[Ticket],
    file_path: Union[str, Path],
) -> None:
    """Persist all tickets to JSON."""
    path = Path(file_path)

    try:
        with path.open("w", encoding="utf-8") as file:
            json.dump(
                [ticket.to_dict() for ticket in tickets],
                file,
                indent=4,
            )
    except OSError as exc:
        raise StorageError(f"Unable to save tickets: {exc}") from exc


def load_tickets(file_path: Union[str, Path]) -> List[Ticket]:
    """Load tickets from JSON; return an empty list if the file is absent."""
    path = Path(file_path)

    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise StorageError("Ticket data must be stored as a JSON list.")

        return [Ticket.from_dict(item) for item in data]

    except json.JSONDecodeError as exc:
        raise StorageError(
            "tickets.json contains invalid JSON. "
            "Fix or restore the file before continuing."
        ) from exc
    except (OSError, KeyError, TypeError, ValueError) as exc:
        raise StorageError(
            f"Unable to load tickets: {exc}"
        ) from exc
