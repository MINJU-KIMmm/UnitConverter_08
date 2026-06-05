from typing import Protocol


class LengthUnit(Protocol):
    name: str

    def to_meter(self, value: float) -> float: ...


class RatioUnit:
    """Unit defined by how many of itself equal one meter."""

    def __init__(self, name: str, units_per_meter: float) -> None:
        self.name = name
        self._units_per_meter = units_per_meter

    def to_meter(self, value: float) -> float:
        return value / self._units_per_meter

    def from_meter(self, meter_value: float) -> float:
        return meter_value * self._units_per_meter
