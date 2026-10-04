# IT Helpdesk Ticket Management System — Design Note

## 1. Personalized Parameters

Run:

```powershell
python generate_parameters.py
```


### Categories
- [VPN]
- [Access Request]
- [Printer]
- [Software]
- [Application Bug]

### SLA Hours
- Critical: [2] hours
- High: [10] hours
- Medium: [48] hours
- Low: [116] hours

### Ticket Prefix
- [TCK]

## 2. System Design

The application is implemented as a modular command-line Python application. A `Ticket` class represents each helpdesk ticket, while validation, business logic, persistence, and CLI interaction are separated into different modules.

## 3. Status Workflow

The status workflow is:

`Open -> In Progress -> Resolved -> Closed`

## 4. SLA Handling

SLA breach detection calculates a deadline by adding the priority-specific SLA duration to the ticket creation timestamp and compares it with the current time for active tickets.

## 5. Design Decision

### Why JSON persistence?

I chose JSON instead of CSV because the application stores structured ticket objects containing multiple attributes, including timestamps and status. JSON maps naturally to Python dictionaries and makes serialization/deserialization straightforward. It also leaves room for adding fields later without redesigning the file structure.

## 6. Error Handling

Invalid categories, priorities, empty requester names/descriptions, and invalid status transitions are handled through a custom `ValidationError`. User-facing errors are displayed clearly and the CLI re-prompts instead of crashing.
