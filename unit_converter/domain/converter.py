from unit_converter.domain.unit_registry import UnitRegistry


class Converter:
    def __init__(self, registry: UnitRegistry) -> None:
        self._registry = registry

    def to_meter(self, value: float, unit_name: str) -> float:
        return self._registry.get(unit_name).to_meter(value)

    def convert_all(self, value: float, from_unit: str) -> dict[str, float]:
        meter_value = self.to_meter(value, from_unit)
        return {
            name: self._registry.get(name).from_meter(meter_value)
            for name in self._registry.names()
        }
