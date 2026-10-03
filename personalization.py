import hashlib
import random


def get_my_parameters(employee_id: str) -> dict:
    """Deterministic personalized parameters derived from employee ID."""
    seed = int(hashlib.sha256(employee_id.encode()).hexdigest(), 16) % 231
    rng = random.Random(seed)

    all_categories = [
        "Hardware",
        "Software",
        "Network",
        "Access Request",
        "Email",
        "Printer",
        "VPN",
        "Application Bug",
        "Account Lockout",
        "Data Backup",
    ]

    return {
        "categories": rng.sample(all_categories, 5),
        "sla_hours": {
            "Critical": rng.randint(2, 4),
            "High": rng.randint(6, 12),
            "Medium": rng.randint(24, 48),
            "Low": rng.randint(72, 120),
        },
        "ticket_prefix": rng.choice(["TCK", "INC", "REQ", "SR"]),
    }