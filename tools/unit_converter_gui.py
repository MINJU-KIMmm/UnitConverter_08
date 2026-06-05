"""Unit Converter GUI — PRD 범위 외 수동 검증 도구 (PyQt6, cli.run 재사용)."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPlainTextEdit,
    QPushButton,
    QRadioButton,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from unit_converter.app.exceptions import UnitConverterError
from unit_converter.app.output_formatter import FormatType
from unit_converter.cli import run
from unit_converter.infrastructure.config_loader import default_registry

_STATUS_OK = "#1b5e20"
_STATUS_ERROR = "#b00020"
_STATUS_IDLE = "#333333"


class UnitConverterWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Unit Converter")
        self.resize(520, 420)
        self.setMinimumSize(480, 380)

        self._format: FormatType = "table"

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(12, 12, 12, 12)

        layout.addWidget(self._build_input_section())
        layout.addWidget(self._build_result_section(), stretch=1)
        layout.addLayout(self._build_status_section())

    def _build_input_section(self) -> QGroupBox:
        group = QGroupBox("입력")
        outer = QVBoxLayout(group)

        row = QHBoxLayout()
        row.addWidget(QLabel("unit:value"))
        self._input_entry = QLineEdit("meter:2.5")
        self._input_entry.returnPressed.connect(self._convert)
        row.addWidget(self._input_entry, stretch=1)

        convert_btn = QPushButton("Convert")
        convert_btn.clicked.connect(self._convert)
        row.addWidget(convert_btn)
        outer.addLayout(row)

        quick_row = QHBoxLayout()
        quick_row.addWidget(QLabel("빠른 입력:"))
        for sample in ("meter:2.5", "feet:1", "yard:3"):
            btn = QPushButton(sample)
            btn.setFixedWidth(90)
            btn.clicked.connect(lambda _checked=False, s=sample: self._set_sample(s))
            quick_row.addWidget(btn)
        quick_row.addStretch()
        outer.addLayout(quick_row)

        format_row = QHBoxLayout()
        format_row.addWidget(QLabel("출력 형식:"))
        self._format_group = QButtonGroup(self)
        for index, (label, value) in enumerate((("Table", "table"), ("JSON", "json"), ("CSV", "csv"))):
            radio = QRadioButton(label)
            radio.setProperty("format", value)
            self._format_group.addButton(radio, index)
            format_row.addWidget(radio)
            if value == "table":
                radio.setChecked(True)
        self._format_group.idClicked.connect(self._on_format_changed)
        format_row.addStretch()
        outer.addLayout(format_row)

        return group

    def _build_result_section(self) -> QGroupBox:
        group = QGroupBox("변환 결과")
        layout = QVBoxLayout(group)

        self._tabs = QTabWidget()
        self._table = QTableWidget(0, 3)
        self._table.setHorizontalHeaderLabels(["단위", "입력값", "결과"])
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._table.verticalHeader().setVisible(False)
        self._table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        self._raw_text = QPlainTextEdit()
        self._raw_text.setReadOnly(True)
        self._raw_text.setFont(QFont("Consolas", 10))

        self._tabs.addTab(self._table, "표")
        self._tabs.addTab(self._raw_text, "원문")
        layout.addWidget(self._tabs)
        return group

    def _build_status_section(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        units = ", ".join(default_registry().names())
        layout.addWidget(QLabel(f"지원 단위: {units}"))

        self._status_label = QLabel("입력 후 Convert를 누르세요. (예: meter:2.5)")
        self._status_label.setStyleSheet(f"color: {_STATUS_IDLE};")
        layout.addWidget(self._status_label)
        return layout

    def _on_format_changed(self, _button_id: int) -> None:
        button = self._format_group.checkedButton()
        if button is not None:
            self._format = button.property("format")
        self._convert()

    def _set_sample(self, sample: str) -> None:
        self._input_entry.setText(sample)
        self._convert()

    def _convert(self) -> None:
        input_text = self._input_entry.text().strip()
        button = self._format_group.checkedButton()
        fmt: FormatType = button.property("format") if button else self._format

        try:
            output = run(input_text, fmt)
        except UnitConverterError as exc:
            self._set_status(str(exc), error=True)
            self._clear_results()
            return

        self._set_status("변환 완료", error=False)
        self._show_results(output, fmt)

    def _set_status(self, message: str, *, error: bool) -> None:
        self._status_label.setText(message)
        color = _STATUS_ERROR if error else _STATUS_OK
        self._status_label.setStyleSheet(f"color: {color};")

    def _clear_results(self) -> None:
        self._table.setRowCount(0)
        self._raw_text.setPlainText("")

    def _show_results(self, output: str, fmt: FormatType) -> None:
        self._raw_text.setPlainText(output)
        self._table.setRowCount(0)

        if fmt != "table":
            self._tabs.setCurrentIndex(1)
            return

        self._tabs.setCurrentIndex(0)
        rows: list[tuple[str, str, str]] = []
        for line in output.splitlines():
            if not line.startswith("|") or line.startswith("+"):
                continue
            parts = [part.strip() for part in line.strip("|").split("|")]
            if len(parts) == 3 and parts[0] != "unit":
                rows.append((parts[0], parts[1], parts[2]))

        self._table.setRowCount(len(rows))
        for row_index, row in enumerate(rows):
            for col_index, value in enumerate(row):
                self._table.setItem(row_index, col_index, QTableWidgetItem(value))


def main() -> None:
    app = QApplication(sys.argv)
    window = UnitConverterWindow()
    window.show()
    raise SystemExit(app.exec())


if __name__ == "__main__":
    main()
