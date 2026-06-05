"""Parse unit:value CLI input (FR-01). No conversion or registry access."""

from unit_converter.app.exceptions import InvalidInputError


def parse_input(text: str) -> tuple[str, float]:
    if not text or not text.strip():
        raise InvalidInputError("Invalid format: empty input")

    stripped = text.strip()
    if ":" not in stripped:
        raise InvalidInputError("Invalid format: expected unit:value")

    unit, value_str = stripped.split(":", 1)
    unit = unit.strip()
    value_str = value_str.strip()

    if not unit:
        raise InvalidInputError("Invalid format: missing unit")

    try:
        value = float(value_str)
    except ValueError as exc:
        raise InvalidInputError(f"Invalid format: not a number ({value_str})") from exc

    return unit, value
