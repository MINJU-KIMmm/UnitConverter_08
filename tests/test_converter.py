"""Track B — Domain / Logic tests.

TC mapping: D-CNV-01 ~ D-CNV-04, D-REG-01, D-CFG-01, D-OCP-01
PRD: FR-02, NFR-01, EXT-01~02
"""

import json

import pytest

from unit_converter.domain.converter import Converter
from unit_converter.domain.unit_registry import UnitRegistry
from unit_converter.infrastructure.config_loader import ConfigError, load_registry_from_json


def _default_registry() -> UnitRegistry:
    registry = UnitRegistry()
    registry.register("meter", 1.0)
    registry.register("feet", 3.28084)
    registry.register("yard", 1.09361)
    return registry


def test_d_cnv_01_to_meter_feet():
    """D-CNV-01 / FR-02: to_meter — 1 feet -> 0.3048 m (±ε). OCP 회귀는 green D-OCP-01."""
    registry = _default_registry()
    converter = Converter(registry)
    result = converter.to_meter(1, "feet")
    assert abs(result - 0.3048) < 1e-4


def test_d_cnv_02_convert_all_meter_to_feet():
    """D-CNV-02 / FR-02: convert_all — 2.5 m -> 8.2021 ft."""
    converter = Converter(_default_registry())
    results = converter.convert_all(2.5, "meter")
    assert abs(results["feet"] - 8.2021) < 1e-4


def test_d_cnv_03_convert_all_feet_to_yard_via_meter():
    """D-CNV-03 / FR-02: convert_all — feet→yard conversion consistent via meter."""
    converter = Converter(_default_registry())
    results = converter.convert_all(3.28084, "feet")
    meter_value = converter.to_meter(3.28084, "feet")
    expected_yard = meter_value * 1.09361
    assert abs(results["yard"] - expected_yard) < 1e-4


def test_d_cnv_04_convert_all_meter_to_yard():
    """D-CNV-04 / FR-02: convert_all — 2.5 m -> 2.7340 yd."""
    converter = Converter(_default_registry())
    results = converter.convert_all(2.5, "meter")
    assert abs(results["yard"] - 2.7340) < 1e-4


def test_d_reg_01_register_cubit():
    """D-REG-01: register — cubit 0.4572 enables conversion."""
    registry = _default_registry()
    registry.register("cubit", 1 / 0.4572)
    converter = Converter(registry)
    results = converter.convert_all(1, "cubit")
    assert abs(results["meter"] - 0.4572) < 1e-4


def test_d_cfg_01_load_json_corrupted_config_error(tmp_path):
    """D-CFG-01: load json — corrupted file raises ConfigError."""
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("{invalid", encoding="utf-8")
    with pytest.raises(ConfigError):
        load_registry_from_json(bad_file)


def test_d_ocp_01_inch_via_config_without_converter_change(tmp_path):
    """D-OCP-01 / NFR-01: units.json에 inch 추가 — Converter 소스 변경 없이 config만으로 변환."""
    config_file = tmp_path / "units.json"
    config_file.write_text(
        json.dumps(
            {
                "meter": 1.0,
                "feet": 3.28084,
                "yard": 1.09361,
                "inch": 39.3701,
            }
        ),
        encoding="utf-8",
    )

    registry = load_registry_from_json(config_file)
    converter = Converter(registry)
    results = converter.convert_all(1, "inch")

    assert "inch" in results
    assert abs(results["meter"] - 0.0254) < 1e-4
    assert abs(results["feet"] - 0.0833) < 1e-3
