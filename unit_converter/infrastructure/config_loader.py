import json
from pathlib import Path

from unit_converter.domain.unit_registry import UnitRegistry


class ConfigError(Exception):
    pass


def load_registry_from_json(path: Path | str) -> UnitRegistry:
    try:
        text = Path(path).read_text(encoding="utf-8")
        data = json.loads(text)
    except (OSError, json.JSONDecodeError) as exc:
        raise ConfigError(f"Failed to load config: {path}") from exc

    if not isinstance(data, dict):
        raise ConfigError(f"Invalid config format: {path}")

    registry = UnitRegistry()
    for name, ratio in data.items():
        registry.register(name, float(ratio))
    return registry


def default_registry() -> UnitRegistry:
    config_path = Path(__file__).resolve().parents[2] / "config" / "units.json"
    return load_registry_from_json(config_path)
