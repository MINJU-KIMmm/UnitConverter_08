"""Track B — Domain / Logic RED skeleton tests.

TC mapping: D-CNV-01 ~ D-CNV-04, D-REG-01, D-CFG-01
PRD: FR-02, NFR-01, EXT-01~02
"""

import pytest


def test_d_cnv_01_to_meter_feet():
    """D-CNV-01 / FR-02: to_meter — 1 feet -> 0.3048 m (±ε). OCP 회귀는 green D-OCP-01."""
    pytest.fail("RED: D-CNV-01 to_meter(1 feet) should equal 0.3048 m within tolerance")


def test_d_cnv_02_convert_all_meter_to_feet():
    """D-CNV-02 / FR-02: convert_all — 2.5 m -> 8.2021 ft."""
    pytest.fail("RED: D-CNV-02 convert_all(2.5 meter) should yield 8.2021 feet")


def test_d_cnv_03_convert_all_feet_to_yard_via_meter():
    """D-CNV-03 / FR-02: convert_all — feet→yard conversion consistent via meter."""
    pytest.fail("RED: D-CNV-03 feet→yard should match meter-based conversion path")


def test_d_cnv_04_convert_all_meter_to_yard():
    """D-CNV-04 / FR-02: convert_all — 2.5 m -> 2.7340 yd."""
    pytest.fail("RED: D-CNV-04 convert_all(2.5 meter) should yield 2.7340 yard")


def test_d_reg_01_register_cubit():
    """D-REG-01: register — cubit 0.4572 enables conversion."""
    pytest.fail("RED: D-REG-01 register(cubit, 0.4572) should enable cubit conversion")


def test_d_cfg_01_load_json_corrupted_config_error():
    """D-CFG-01: load json — corrupted file raises ConfigError."""
    pytest.fail("RED: D-CFG-01 corrupted config file should raise ConfigError")
