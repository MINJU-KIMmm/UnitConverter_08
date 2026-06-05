"""Track A — UI / Boundary RED skeleton tests.

TC mapping: U-PAR-01, U-IN-01 ~ U-IN-05, U-OUT-01, U-FMT-01 ~ U-FMT-03
PRD: FR-01~05, EXT-03
"""

import pytest


def test_u_par_01_parse_unit_value():
    """U-PAR-01 / FR-01: Given 'meter:2.5', Then unit=meter, value=2.5."""
    pytest.fail("RED: U-PAR-01 meter:2.5 should parse to unit=meter, value=2.5")


def test_u_in_01_empty_input_format_error():
    """U-IN-01 / FR-05: Given empty input, Then format error message."""
    pytest.fail("RED: U-IN-01 empty input should produce format error message")


def test_u_in_02_missing_colon_form_error():
    """U-IN-02 / FR-05: Given 'meter' (no colon), Then form error."""
    pytest.fail("RED: U-IN-02 input without colon should produce form error")


def test_u_in_03_negative_value_rejected():
    """U-IN-03 / FR-04: Given 'meter:-1', Then reject negative value."""
    pytest.fail("RED: U-IN-03 negative value should be rejected")


def test_u_in_04_unknown_unit_rejected():
    """U-IN-04 / FR-03: Given 'cubit:1' (unregistered), Then unknown unit error."""
    pytest.fail("RED: U-IN-04 cubit:1 should produce unknown unit error")


def test_u_in_05_invalid_format_non_numeric():
    """U-IN-05 / FR-05: Given 'meter / abc', Then format error."""
    pytest.fail("RED: U-IN-05 meter / abc should produce format error")


def test_u_out_01_valid_input_multi_line_output():
    """U-OUT-01 / FR-02: Given 'meter:2.5', Then output 3 or more lines."""
    pytest.fail("RED: U-OUT-01 meter:2.5 should produce 3+ line conversion output")


def test_u_fmt_01_format_table_three_columns():
    """U-FMT-01 / EXT-03: Given --format table, Then 3-column table output."""
    pytest.fail("RED: U-FMT-01 --format table should produce unit|input|result columns")


def test_u_fmt_02_format_json():
    """U-FMT-02 / EXT-03: Given --format json, Then valid JSON conversion output."""
    pytest.fail("RED: U-FMT-02 --format json should produce JSON conversion output")


def test_u_fmt_03_format_csv():
    """U-FMT-03 / EXT-03: Given --format csv, Then CSV conversion output."""
    pytest.fail("RED: U-FMT-03 --format csv should produce CSV conversion output")
