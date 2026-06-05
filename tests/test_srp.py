"""SRP structure verification — Parser / Registry / Converter / Formatter separation.

TC mapping: D-SRP-01
PRD: NFR-02
"""

import ast
import importlib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _module_source(relative_path: str) -> str:
    return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")


def _defined_names(source: str) -> set[str]:
    tree = ast.parse(source)
    return {node.name for node in tree.body if isinstance(node, ast.FunctionDef | ast.ClassDef)}


def test_d_srp_01_parser_registry_converter_formatter_separated():
    """D-SRP-01 / NFR-02: Parser, Registry, Converter, Formatter live in dedicated modules."""
    parser_names = _defined_names(_module_source("unit_converter/app/input_parser.py"))
    registry_names = _defined_names(_module_source("unit_converter/domain/unit_registry.py"))
    converter_names = _defined_names(_module_source("unit_converter/domain/converter.py"))
    formatter_names = _defined_names(_module_source("unit_converter/app/output_formatter.py"))

    assert "parse_input" in parser_names
    assert "UnitRegistry" in registry_names
    assert "Converter" in converter_names
    assert "format_output" in formatter_names

    parser_source = _module_source("unit_converter/app/input_parser.py")
    registry_source = _module_source("unit_converter/domain/unit_registry.py")
    converter_source = _module_source("unit_converter/domain/converter.py")
    cli_source = _module_source("unit_converter/cli.py")

    assert "UnitRegistry" not in parser_source
    assert "Converter" not in parser_source
    assert "format_output" not in parser_source

    assert "parse_input" not in registry_source
    assert "json" not in registry_source
    assert "csv" not in registry_source

    assert "parse_input" not in converter_source
    assert "argparse" not in converter_source

    assert "parse_input" not in cli_source or "from unit_converter.app.input_parser import parse_input" in cli_source
    assert "class UnitRegistry" not in cli_source
    assert "def parse_input" not in cli_source


def test_d_srp_02_input_parser_only_parses():
    """D-SRP-01 / NFR-02: input_parser returns unit/value without registry or conversion."""
    parser = importlib.import_module("unit_converter.app.input_parser")

    unit, value = parser.parse_input("meter:2.5")
    assert unit == "meter"
    assert value == 2.5


def test_d_srp_03_registry_only_manages_units():
    """D-SRP-01 / NFR-02: UnitRegistry registers and resolves units only."""
    registry_module = importlib.import_module("unit_converter.domain.unit_registry")

    registry = registry_module.UnitRegistry()
    registry.register("meter", 1.0)
    registry.register("feet", 3.28084)

    assert registry.has("meter")
    assert registry.get("feet").to_meter(3.28084) == 1.0
    assert registry.names() == ["meter", "feet"]
