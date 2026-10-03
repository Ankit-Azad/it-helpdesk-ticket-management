import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

from models import Ticket
from services import (
    create_ticket,
    filter_tickets,
    generate_ticket_id,
    get_summary,
    update_ticket_status,
)
from storage import load_tickets, save_tickets
from validators import ValidationError


TEST_CONFIG = {
    "categories": ["Network", "VPN", "Email", "Hardware", "Software"],
    "priorities": ["Low", "Medium", "High", "Critical"],
    "statuses": ["Open", "In Progress", "Resolved", "Closed"],
    "ticket_prefix": "TST",
}

SLA_HOURS = {
    "Critical": 2,
    "High": 8,
    "Medium": 24,
    "Low": 72,
}


class HelpdeskTests(unittest.TestCase):

    def test_ticket_id_generation(self):
        self.assertEqual(generate_ticket_id([], "TST"), "TST-0001")

        tickets = [
            Ticket(
                "TST-0001",
                "VPN",
                "High",
                "A",
                "Issue",
            ),
            Ticket(
                "TST-0007",
                "Email",
                "Low",
                "B",
                "Issue",
            ),
        ]

        self.assertEqual(generate_ticket_id(tickets, "TST"), "TST-0008")

    def test_create_ticket(self):
        tickets = []

        ticket = create_ticket(
            tickets,
            "vpn",
            "high",
            "Ankit",
            "VPN does not connect",
            TEST_CONFIG,
        )

        self.assertEqual(ticket.category, "VPN")
        self.assertEqual(ticket.priority, "High")
        self.assertEqual(ticket.status, "Open")
        self.assertEqual(ticket.ticket_id, "TST-0001")

    def test_invalid_input_raises(self):
        with self.assertRaises(ValidationError):
            create_ticket(
                [],
                "Invalid Category",
                "High",
                "Ankit",
                "Issue",
                TEST_CONFIG,
            )

        with self.assertRaises(ValidationError):
            create_ticket(
                [],
                "VPN",
                "Urgent",
                "Ankit",
                "Issue",
                TEST_CONFIG,
            )

        with self.assertRaises(ValidationError):
            create_ticket(
                [],
                "VPN",
                "High",
                "Ankit",
                "   ",
                TEST_CONFIG,
            )

    def test_status_flow(self):
        ticket = Ticket(
            "TST-0001",
            "VPN",
            "High",
            "Ankit",
            "Issue",
        )

        update_ticket_status(ticket, "In Progress", TEST_CONFIG["statuses"])
        self.assertEqual(ticket.status, "In Progress")

        update_ticket_status(ticket, "Resolved", TEST_CONFIG["statuses"])
        self.assertEqual(ticket.status, "Resolved")

        update_ticket_status(ticket, "Closed", TEST_CONFIG["statuses"])
        self.assertEqual(ticket.status, "Closed")

    def test_invalid_status_jump(self):
        ticket = Ticket(
            "TST-0001",
            "VPN",
            "High",
            "Ankit",
            "Issue",
        )

        with self.assertRaises(ValidationError):
            update_ticket_status(
                ticket,
                "Closed",
                TEST_CONFIG["statuses"],
            )

    def test_sla_breach(self):
        old_time = datetime.now() - timedelta(hours=3)
        ticket = Ticket(
            "TST-0001",
            "VPN",
            "Critical",
            "Ankit",
            "Issue",
            created_at=old_time,
        )

        self.assertTrue(ticket.is_sla_breached(SLA_HOURS))

    def test_filter(self):
        tickets = [
            Ticket("TST-0001", "VPN", "High", "A", "Issue"),
            Ticket("TST-0002", "Email", "Low", "B", "Issue"),
        ]

        result = filter_tickets(tickets, category="VPN")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].ticket_id, "TST-0001")

    def test_summary(self):
        tickets = [
            Ticket("TST-0001", "VPN", "High", "A", "Issue"),
            Ticket("TST-0002", "Email", "Low", "B", "Issue"),
        ]

        status_counts, category_counts, breached = get_summary(
            tickets,
            TEST_CONFIG["categories"],
            TEST_CONFIG["statuses"],
            SLA_HOURS,
        )

        self.assertEqual(status_counts["Open"], 2)
        self.assertEqual(category_counts["VPN"], 1)
        self.assertEqual(len(breached), 0)

    def test_json_persistence(self):
        tickets = [
            Ticket(
                "TST-0001",
                "VPN",
                "High",
                "Ankit",
                "VPN issue",
            )
        ]

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "tickets.json"

            save_tickets(tickets, path)
            loaded = load_tickets(path)

            self.assertEqual(len(loaded), 1)
            self.assertEqual(loaded[0].ticket_id, "TST-0001")
            self.assertEqual(loaded[0].status, "Open")


if __name__ == "__main__":
    unittest.main()
