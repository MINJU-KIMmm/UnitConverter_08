import csv
import io
import json
from typing import Literal

FormatType = Literal["table", "json", "csv"]

_PRECISION = 4


def _round_result(value: float) -> float:
    return round(value, _PRECISION)


def _display_result(value: float) -> str:
    return f"{_round_result(value):.{_PRECISION}f}"


def format_table(input_unit: str, input_value: float, results: dict[str, float]) -> str:
    lines = ["unit | input | result"]
    for unit, result in results.items():
        lines.append(f"{unit} | {input_value} | {_display_result(result)}")
    return "\n".join(lines)


def format_json(input_unit: str, input_value: float, results: dict[str, float]) -> str:
    rows = [
        {
            "unit": unit,
            "input": input_value,
            "result": _round_result(result),
        }
        for unit, result in results.items()
    ]
    return json.dumps(rows, indent=2)


def format_csv(input_unit: str, input_value: float, results: dict[str, float]) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["unit", "input", "result"])
    for unit, result in results.items():
        writer.writerow([unit, input_value, _display_result(result)])
    return buffer.getvalue().strip()


def format_output(
    fmt: FormatType,
    input_unit: str,
    input_value: float,
    results: dict[str, float],
) -> str:
    if fmt == "table":
        return format_table(input_unit, input_value, results)
    if fmt == "json":
        return format_json(input_unit, input_value, results)
    return format_csv(input_unit, input_value, results)
