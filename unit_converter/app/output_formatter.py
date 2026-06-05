import csv
import io
import json
from typing import Literal

FormatType = Literal["table", "json", "csv"]

_PRECISION = 4


def _round_result(value: float) -> float:
    return round(value, _PRECISION)


def _format_input_value(value: float) -> str:
    return f"{value:.4f}".rstrip("0").rstrip(".")


def _format_result_value(value: float, same_unit: bool) -> str:
    rounded = _round_result(value)
    if same_unit:
        return _format_input_value(rounded)
    return f"{rounded:.4f}"


def _make_bordered_table(headers: tuple[str, ...], rows: list[tuple[str, ...]]) -> str:
    widths = [len(header) for header in headers]
    for row in rows:
        for index, cell in enumerate(row):
            widths[index] = max(widths[index], len(cell))

    def border() -> str:
        return "+" + "+".join("-" * (width + 2) for width in widths) + "+"

    def row_line(cells: tuple[str, ...]) -> str:
        return "|" + "|".join(f" {cells[i]:<{widths[i]}} " for i in range(len(cells))) + "|"

    lines = [border(), row_line(headers), border()]
    lines.extend(row_line(row) for row in rows)
    lines.append(border())
    return "\n".join(lines)


def format_table(input_unit: str, input_value: float, results: dict[str, float]) -> str:
    input_display = _format_input_value(input_value)
    rows = [
        (
            unit,
            input_display,
            _format_result_value(result, unit == input_unit),
        )
        for unit, result in results.items()
    ]
    return _make_bordered_table(("unit", "input", "result"), rows)


def format_json(input_unit: str, input_value: float, results: dict[str, float]) -> str:
    output = {unit: _round_result(result) for unit, result in results.items()}
    return json.dumps(output, indent=2)


def format_csv(input_unit: str, input_value: float, results: dict[str, float]) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["unit", "input", "result"])
    input_display = _format_input_value(input_value)
    for unit, result in results.items():
        writer.writerow([
            unit,
            input_display,
            _format_result_value(result, unit == input_unit),
        ])
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
