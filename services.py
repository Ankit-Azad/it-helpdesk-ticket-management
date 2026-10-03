from typing import Dict, List, Optional, Tuple

from models import Ticket
from validators import (
    ValidationError,
    validate_category,
    validate_description,
    validate_priority,
    validate_requester,
    validate_status,
)


STATUS_TRANSITIONS = {
    "Open": "In Progress",
    "In Progress": "Resolved",
    "Resolved": "Closed",
}


def generate_ticket_id(tickets: List[Ticket], prefix: str) -> str:
    """Generate the next zero-padded ticket ID."""
    if not tickets:
        next_number = 1
    else:
        numbers = [
            int(ticket.ticket_id.rsplit("-", 1)[1])
            for ticket in tickets
            if "-" in ticket.ticket_id
            and ticket.ticket_id.rsplit("-", 1)[1].isdigit()
        ]
        next_number = max(numbers, default=0) + 1

    return f"{prefix}-{next_number:04d}"


def create_ticket(
    tickets: List[Ticket],
    category: str,
    priority: str,
    requester: str,
    description: str,
    config: Dict,
) -> Ticket:
    """Validate input, create a ticket object, and add it to the list."""
    category = validate_category(category, config["categories"])
    priority = validate_priority(priority, config["priorities"])
    requester = validate_requester(requester)
    description = validate_description(description)

    ticket_id = generate_ticket_id(tickets, config["ticket_prefix"])

    ticket = Ticket(
        ticket_id=ticket_id,
        category=category,
        priority=priority,
        requester=requester,
        description=description,
    )

    tickets.append(ticket)
    return ticket


def find_ticket(tickets: List[Ticket], ticket_id: str) -> Optional[Ticket]:
    """Find a ticket by ID, case-insensitively."""
    normalized = ticket_id.strip().upper()

    for ticket in tickets:
        if ticket.ticket_id.upper() == normalized:
            return ticket

    return None


def update_ticket_status(
    ticket: Ticket,
    new_status: str,
    statuses: List[str],
) -> None:
    """Enforce Open -> In Progress -> Resolved -> Closed."""
    new_status = validate_status(new_status, statuses)

    if new_status == ticket.status:
        raise ValidationError(
            f"Ticket is already in '{ticket.status}' status."
        )

    expected_next = STATUS_TRANSITIONS.get(ticket.status)

    if new_status != expected_next:
        if expected_next:
            raise ValidationError(
                f"Invalid transition: {ticket.status} -> {new_status}. "
                f"Next allowed status is '{expected_next}'."
            )
        raise ValidationError(
            f"No further status transition is allowed from '{ticket.status}'."
        )

    ticket.update_status(new_status)


def filter_tickets(
    tickets: List[Ticket],
    category: Optional[str] = None,
    priority: Optional[str] = None,
    status: Optional[str] = None,
) -> List[Ticket]:
    """Filter tickets by any combination of category, priority, and status."""
    category_filter = category.lower() if category else None
    priority_filter = priority.lower() if priority else None
    status_filter = status.lower() if status else None

    return [
        ticket
        for ticket in tickets
        if (category_filter is None or ticket.category.lower() == category_filter)
        and (priority_filter is None or ticket.priority.lower() == priority_filter)
        and (status_filter is None or ticket.status.lower() == status_filter)
    ]


def get_summary(
    tickets: List[Ticket],
    categories: List[str],
    statuses: List[str],
    sla_hours: Dict[str, int],
) -> Tuple[Dict[str, int], Dict[str, int], List[Ticket]]:
    """Return status counts, category counts, and active SLA breaches."""

    status_counts = {
        status: len([ticket for ticket in tickets if ticket.status == status])
        for status in statuses
    }

    category_counts = {
        category: len(
            [ticket for ticket in tickets if ticket.category == category]
        )
        for category in categories
    }

    breached_tickets = [
        ticket
        for ticket in tickets
        if ticket.is_sla_breached(sla_hours)
    ]

    return status_counts, category_counts, breached_tickets
