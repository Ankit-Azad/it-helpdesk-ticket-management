from config import CATEGORIES, SLA_HOURS, TICKET_PREFIX


def main():
    print("\n=== YOUR TEAM'S PERSONALIZED PARAMETERS ===\n")

    print("Categories:")
    for category in CATEGORIES:
        print(f"  - {category}")

    print("\nSLA hours:")
    for priority, hours in SLA_HOURS.items():
        print(f"  - {priority}: {hours} hours")

    print(f"\nTicket prefix: {TICKET_PREFIX}")

    # print("\nUse this output for your DESIGN_NOTE.md.")
    # print("Do not replace it with the assessment's EMP1042 example.")


if __name__ == "__main__":
    main()