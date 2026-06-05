"""Golden Master — characterization tests before safe refactor.

TC mapping: D-GM-01 ~ D-GM-03
PRD: FR-02, EXT-03 (behavior lock for NFR-02 refactoring)
"""

from unit_converter.cli import run

EXPECTED_TABLE = """\
+-------+-------+--------+
| unit  | input | result |
+-------+-------+--------+
| meter | 2.5   | 2.5    |
| feet  | 2.5   | 8.2021 |
| yard  | 2.5   | 2.7340 |
+-------+-------+--------+"""

EXPECTED_JSON = """\
{
  "meter": 2.5,
  "feet": 8.2021,
  "yard": 2.734
}"""

EXPECTED_CSV = """\
unit,input,result
meter,2.5,2.5
feet,2.5,8.2021
yard,2.5,2.7340"""


def test_d_gm_01_golden_master_table():
    """D-GM-01: meter:2.5 table output must not change during refactor."""
    assert run("meter:2.5", "table") == EXPECTED_TABLE


def test_d_gm_02_golden_master_json():
    """D-GM-02: meter:2.5 json output must not change during refactor."""
    assert run("meter:2.5", "json") == EXPECTED_JSON


def test_d_gm_03_golden_master_csv():
    """D-GM-03: meter:2.5 csv output must not change during refactor."""
    output = run("meter:2.5", "csv").replace("\r\n", "\n")
    assert output == EXPECTED_CSV
