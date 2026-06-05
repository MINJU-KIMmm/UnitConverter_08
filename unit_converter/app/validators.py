from unit_converter.app.exceptions import NegativeValueError, UnknownUnitError
from unit_converter.domain.unit_registry import UnitRegistry


def validate_value(value: float) -> None:
    if value < 0:
        raise NegativeValueError("Negative value not allowed")


def validate_unit(unit: str, registry: UnitRegistry) -> None:
    if not registry.has(unit):
        raise UnknownUnitError(f"Unknown unit: {unit}")
