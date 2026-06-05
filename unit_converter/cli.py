import argparse
import sys

from unit_converter.app.input_parser import parse_input
from unit_converter.app.output_formatter import FormatType, format_output
from unit_converter.app.validators import validate_unit, validate_value
from unit_converter.domain.converter import Converter
from unit_converter.infrastructure.config_loader import default_registry


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Length unit converter")
    parser.add_argument("input", nargs="?", default="", help="unit:value (e.g. meter:2.5)")
    parser.add_argument(
        "--format",
        choices=["table", "json", "csv"],
        default="table",
        help="Output format (default: table)",
    )
    return parser


def run(input_text: str, fmt: FormatType = "table") -> str:
    unit, value = parse_input(input_text)
    validate_value(value)

    registry = default_registry()
    validate_unit(unit, registry)

    converter = Converter(registry)
    results = converter.convert_all(value, unit)
    return format_output(fmt, unit, value, results)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        output = run(args.input, args.format)
        print(output)
        return 0
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
