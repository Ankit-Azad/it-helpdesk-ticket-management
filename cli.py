from typing import List, Optional

from config import (
    CATEGORIES,
    DATA_FILE,
    PRIORITIES,
    SLA_HOURS,
    STATUSES,
    TICKET_PREFIX,
)
from models import Ticket
from services import (
    create_ticket,
    filter_tickets,
    find_ticket,
    get_summary,
    update_ticket_status,
)
from storage import save_tickets
from validators import ValidationError


CONFIG = {
    "categories": CATEGORIES,
    "priorities": PRIORITIES,
    "statuses": STATUSES,
    "ticket_prefix": TICKET_PREFIX,
}


def show_menu() -> None:
    print("\n" + "=" * 52)
    print("            IT HELPDESK MANAGEMENT SYSTEM")
    print("=" * 52)
    print("1. Raise Ticket")
    print("2. View All Tickets")
    print("3. Update Ticket Status")
    print("4. Filter / Search Tickets")
    print("5. View Summary")
    print("6. View SLA-Breached Tickets")
    print("7. Exit")
    print("=" * 52)


def pause() -> None:
    input("\nPress Enter to continue...")


def print_tickets(tickets: List[Ticket]) -> None:
    if not tickets:
        print("\nNo tickets found.")
        return

    print("\n" + "-" * 100)
    print(
        f"{'ID':<12}{'Category':<20}{'Priority':<12}"
        f"{'Status':<15}{'Requester':<18}"
    )
    print("-" * 100)

    for ticket in tickets:
        print(
            f"{ticket.ticket_id:<12}"
            f"{ticket.category:<20}"
            f"{ticket.priority:<12}"
            f"{ticket.status:<15}"
            f"{ticket.requester:<18}"
        )

    print("-" * 100)


def print_ticket_details(ticket: Ticket) -> None:
    print("\n" + "=" * 60)
    print("TICKET DETAILS")
    print("=" * 60)
    print(f"Ticket ID   : {ticket.ticket_id}")
    print(f"Category    : {ticket.category}")
    print(f"Priority    : {ticket.priority}")
    print(f"Requester   : {ticket.requester}")
    print(f"Description : {ticket.description}")
    print(f"Created At  : {ticket.created_at:%Y-%m-%d %H:%M:%S}")
    print(f"Status      : {ticket.status}")
    print(f"SLA Breach  : {'YES' if ticket.is_sla_breached(SLA_HOURS) else 'NO'}")
    print("=" * 60)


def handle_raise_ticket(tickets: List[Ticket]) -> None:
    print("\nAssigned categories:")
    print(", ".join(CATEGORIES))
    print("Priority options:", ", ".join(PRIORITIES))

    while True:
        category = input("Category: ").strip()
        priority = input("Priority: ").strip()
        requester = input("Requester name: ").strip()
        description = input("Description: ").strip()

        try:
            ticket = create_ticket(
                tickets=tickets,
                category=category,
                priority=priority,
                requester=requester,
                description=description,
                config=CONFIG,
            )
            save_tickets(tickets, DATA_FILE)
            print("\nTicket created successfully.")
            print_ticket_details(ticket)
            break

        except ValidationError as exc:
            print(f"\nInput error: {exc}")
            print("Please enter the ticket details again.\n")


def handle_view_all(tickets: List[Ticket]) -> None:
    print_tickets(tickets)


def handle_update_ticket(tickets: List[Ticket]) -> None:
    if not tickets:
        print("\nNo tickets available.")
        return

    ticket_id = input("\nEnter Ticket ID: ").strip()
    ticket = find_ticket(tickets, ticket_id)

    if ticket is None:
        print("Error: Ticket ID not found.")
        return

    print_ticket_details(ticket)
    print("\nStatus options:", ", ".join(STATUSES))
    new_status = input("New status: ").strip()

    try:
        update_ticket_status(ticket, new_status, STATUSES)
        save_tickets(tickets, DATA_FILE)
        print(f"\nStatus updated successfully to '{ticket.status}'.")
    except ValidationError as exc:
        print(f"\nStatus update error: {exc}")


def prompt_optional_choice(
    label: str,
    options: List[str],
) -> Optional[str]:
    print(f"\n{label}")
    print("Available:", ", ".join(options))
    value = input(
        f"Enter {label.lower()} or press Enter for no filter: "
    ).strip()

    if not value:
        return None

    for option in options:
        if value.lower() == option.lower():
            return option

    print(f"Invalid {label.lower()}. No filter applied for this field.")
    return None


def handle_filter(tickets: List[Ticket]) -> None:
    category = prompt_optional_choice("Category", CATEGORIES)
    priority = prompt_optional_choice("Priority", PRIORITIES)
    status = prompt_optional_choice("Status", STATUSES)

    filtered = filter_tickets(
        tickets,
        category=category,
        priority=priority,
        status=status,
    )

    print(f"\nMatching tickets: {len(filtered)}")
    print_tickets(filtered)


def handle_summary(tickets: List[Ticket]) -> None:
    status_counts, category_counts, breached = get_summary(
        tickets,
        CATEGORIES,
        STATUSES,
        SLA_HOURS,
    )

    print("\n========== SUMMARY ==========")

    print("\nTicket counts by status:")
    for status, count in status_counts.items():
        print(f"  {status:<12}: {count}")

    print("\nTicket counts by category:")
    for category, count in category_counts.items():
        print(f"  {category:<20}: {count}")

    print(f"\nSLA-breached active tickets: {len(breached)}")

    if breached:
        for ticket in breached:
            print(f"  - {ticket.ticket_id} ({ticket.priority})")


def handle_sla_breaches(tickets: List[Ticket]) -> None:
    _, _, breached = get_summary(
        tickets,
        CATEGORIES,
        STATUSES,
        SLA_HOURS,
    )

    print("\n====== SLA-BREACHED TICKETS ======")

    if not breached:
        print("No active SLA-breached tickets.")
        return

    for ticket in breached:
        print_ticket_details(ticket)


def run_cli(tickets: List[Ticket]) -> None:
    print(
        f"\nLoaded {len(tickets)} ticket(s). "
        f"Ticket prefix: {TICKET_PREFIX}"
    )

    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            handle_raise_ticket(tickets)
            pause()
        elif choice == "2":
            handle_view_all(tickets)
            pause()
        elif choice == "3":
            handle_update_ticket(tickets)
            pause()
        elif choice == "4":
            handle_filter(tickets)
            pause()
        elif choice == "5":
            handle_summary(tickets)
            pause()
        elif choice == "6":
            handle_sla_breaches(tickets)
            pause()
        elif choice == "7":
            save_tickets(tickets, DATA_FILE)
            print("\nAll tickets saved. Goodbye!")
            break
        else:
            print("\nInvalid menu choice. Please enter a number from 1 to 7.")
