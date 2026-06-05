def parse_input(text: str) -> tuple[str, float]:
    if not text or not text.strip():
        raise ValueError("Invalid format: empty input")

    stripped = text.strip()
    if ":" not in stripped:
        raise ValueError("Invalid format: expected unit:value")

    unit, value_str = stripped.split(":", 1)
    unit = unit.strip()
    value_str = value_str.strip()

    if not unit:
        raise ValueError("Invalid format: missing unit")

    try:
        value = float(value_str)
    except ValueError as exc:
        raise ValueError(f"Invalid format: not a number ({value_str})") from exc

    return unit, value
