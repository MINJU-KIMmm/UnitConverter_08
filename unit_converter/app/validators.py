from unit_converter.domain.unit_registry import UnitRegistry


def validate_value(value: float) -> None:
    if value < 0:
        raise ValueError("Negative value not allowed")


def validate_unit(unit: str, registry: UnitRegistry) -> None:
    if not registry.has(unit):
        raise ValueError(f"Unknown unit: {unit}")
