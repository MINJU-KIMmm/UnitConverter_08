"""Unit registration and lookup — OCP extension point (NFR-01). No parsing or I/O."""

from unit_converter.domain.length_unit import LengthUnit, RatioUnit


class UnitRegistry:
    def __init__(self) -> None:
        self._units: dict[str, RatioUnit] = {}

    def register(self, name: str, units_per_meter: float) -> None:
        self._units[name] = RatioUnit(name, units_per_meter)

    def get(self, name: str) -> LengthUnit:
        if name not in self._units:
            raise KeyError(f"Unknown unit: {name}")
        return self._units[name]

    def names(self) -> list[str]:
        return list(self._units.keys())

    def has(self, name: str) -> bool:
        return name in self._units
