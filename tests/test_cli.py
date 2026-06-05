"""Track A — UI / Boundary tests.

TC mapping: U-PAR-01, U-IN-01 ~ U-IN-05, U-OUT-01, U-FMT-01 ~ U-FMT-03
PRD: FR-01~05, EXT-03
"""

import json
import subprocess
import sys
from pathlib import Path

from unit_converter.app.input_parser import parse_input

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "unit_converter", *args],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )


def test_u_par_01_parse_unit_value():
    """U-PAR-01 / FR-01: Given 'meter:2.5', Then unit=meter, value=2.5."""
    unit, value = parse_input("meter:2.5")
    assert unit == "meter"
    assert value == 2.5


def test_u_in_01_empty_input_format_error():
    """U-IN-01 / FR-05: Given empty input, Then format error message."""
    result = _run_cli("")
    assert result.returncode != 0
    assert "Invalid format" in result.stderr


def test_u_in_02_missing_colon_form_error():
    """U-IN-02 / FR-05: Given 'meter' (no colon), Then form error."""
    result = _run_cli("meter")
    assert result.returncode != 0
    assert "Invalid format" in result.stderr


def test_u_in_03_negative_value_rejected():
    """U-IN-03 / FR-04: Given 'meter:-1', Then reject negative value."""
    result = _run_cli("meter:-1")
    assert result.returncode != 0
    assert "Negative value" in result.stderr


def test_u_in_04_unknown_unit_rejected():
    """U-IN-04 / FR-03: Given 'cubit:1' (unregistered), Then unknown unit error."""
    result = _run_cli("cubit:1")
    assert result.returncode != 0
    assert "Unknown unit" in result.stderr


def test_u_in_05_invalid_format_non_numeric():
    """U-IN-05 / FR-05: Given 'meter / abc', Then format error."""
    result = _run_cli("meter / abc")
    assert result.returncode != 0
    assert "Invalid format" in result.stderr


def test_u_out_01_valid_input_multi_line_output():
    """U-OUT-01 / FR-02: meter:2.5 → ≥3 lines (meter/feet/yard), input unit line included."""
    result = _run_cli("meter:2.5")
    assert result.returncode == 0
    lines = [line for line in result.stdout.strip().splitlines() if line.strip()]
    assert len(lines) >= 3
    output = result.stdout.lower()
    assert "meter" in output
    assert "feet" in output
    assert "yard" in output


def test_u_fmt_01_format_table_three_columns():
    """U-FMT-01 / EXT-03: Given --format table, Then 3-column bordered table output."""
    result = _run_cli("meter:2.5", "--format", "table")
    assert result.returncode == 0
    output = result.stdout
    assert "unit" in output and "input" in output and "result" in output
    assert "8.2021" in output
    assert "2.7340" in output

    data_rows = []
    for line in output.splitlines():
        if not line.startswith("|") or line.startswith("+"):
            continue
        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) == 3 and parts[0] != "unit":
            data_rows.append(parts)

    assert len(data_rows) >= 3
    meter_row = next(row for row in data_rows if row[0] == "meter")
    feet_row = next(row for row in data_rows if row[0] == "feet")
    yard_row = next(row for row in data_rows if row[0] == "yard")
    assert meter_row == ["meter", "2.5", "2.5"]
    assert feet_row == ["feet", "2.5", "8.2021"]
    assert yard_row == ["yard", "2.5", "2.7340"]


def test_u_fmt_02_format_json():
    """U-FMT-02 / EXT-03: Given --format json, Then flat unit→result JSON (units.json 형태)."""
    result = _run_cli("meter:2.5", "--format", "json")
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert isinstance(data, dict)
    assert set(data.keys()) >= {"meter", "feet", "yard"}
    assert data["meter"] == 2.5
    assert abs(data["feet"] - 8.2021) < 1e-4
    assert abs(data["yard"] - 2.7340) < 1e-4


def test_u_fmt_03_format_csv():
    """U-FMT-03 / EXT-03: Given --format csv, Then CSV conversion output."""
    result = _run_cli("meter:2.5", "--format", "csv")
    assert result.returncode == 0
    lines = result.stdout.strip().splitlines()
    assert lines[0] == "unit,input,result"
    assert len(lines) >= 4
