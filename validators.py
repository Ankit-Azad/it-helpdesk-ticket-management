class ValidationError(Exception):
    """Raised when user input violates a business rule."""


def validate_non_empty(value: str, field_name: str) -> str:
    value = value.strip()

    if not value:
        raise ValidationError(
            f"{field_name} cannot be empty."
        )

    return value


def validate_category(category, categories):
    category = category.strip()

    for allowed in categories:
        if category.lower() == allowed.lower():
            return allowed

    raise ValidationError(
        f"Invalid category. Choose one of: {', '.join(categories)}."
    )


def validate_priority(priority, priorities):
    priority = priority.strip()

    for allowed in priorities:
        if priority.lower() == allowed.lower():
            return allowed

    raise ValidationError(
        f"Invalid priority. Choose one of: {', '.join(priorities)}."
    )


def validate_status(status, statuses):
    status = status.strip()

    for allowed in statuses:
        if status.lower() == allowed.lower():
            return allowed

    raise ValidationError(
        f"Invalid status. Choose one of: {', '.join(statuses)}."
    )


def validate_requester(requester):
    return validate_non_empty(requester, "Requester name")


def validate_description(description):
    return validate_non_empty(description, "Description")