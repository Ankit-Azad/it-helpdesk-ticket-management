from datetime import datetime, timedelta
from typing import Any, Dict, Optional


class Ticket:
    """Represents one IT helpdesk ticket."""

    def __init__(
        self,
        ticket_id: str,
        category: str,
        priority: str,
        requester: str,
        description: str,
        created_at: Optional[datetime] = None,
        status: str = "Open",
    ):
        self.ticket_id = ticket_id
        self.category = category
        self.priority = priority
        self.requester = requester
        self.description = description
        self.created_at = created_at or datetime.now()
        self.status = status

    def update_status(self, new_status: str) -> None:
        self.status = new_status

    def is_sla_breached(
        self,
        sla_hours: Dict[str, int],
        now: Optional[datetime] = None,
    ) -> bool:
        """Return True when an active ticket is past its SLA deadline."""
        now = now or datetime.now()
        deadline = self.created_at + timedelta(hours=sla_hours[self.priority])

        # Resolved/closed work is no longer treated as an active SLA breach.
        return (
            self.status in {"Open", "In Progress"}
            and now > deadline
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert the object into JSON-serializable data."""
        return {
            "ticket_id": self.ticket_id,
            "category": self.category,
            "priority": self.priority,
            "requester": self.requester,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Ticket":
        """Recreate a Ticket object from stored JSON data."""
        return cls(
            ticket_id=data["ticket_id"],
            category=data["category"],
            priority=data["priority"],
            requester=data["requester"],
            description=data["description"],
            created_at=datetime.fromisoformat(data["created_at"]),
            status=data["status"],
        )

    def __str__(self) -> str:
        return (
            f"{self.ticket_id} | {self.category} | "
            f"{self.priority} | {self.status} | {self.requester}"
        )
