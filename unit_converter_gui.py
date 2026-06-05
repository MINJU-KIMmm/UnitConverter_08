"""Unit Converter GUI — 기존 domain/CLI 로직 재사용."""

import tkinter as tk
from tkinter import messagebox, ttk

from unit_converter.app.output_formatter import FormatType
from unit_converter.cli import run
from unit_converter.infrastructure.config_loader import default_registry


class UnitConverterApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Unit Converter")
        self.geometry("520x420")
        self.minsize(480, 380)
        self.configure(padx=12, pady=12)

        self._format = tk.StringVar(value="table")
        self._status = tk.StringVar(value="입력 후 Convert를 누르세요. (예: meter:2.5)")

        self._build_input_section()
        self._build_result_section()
        self._build_status_section()

        self.bind("<Return>", lambda _event: self._convert())

    def _build_input_section(self) -> None:
        frame = ttk.LabelFrame(self, text="입력", padding=10)
        frame.pack(fill="x", pady=(0, 10))

        ttk.Label(frame, text="unit:value").grid(row=0, column=0, sticky="w")
        self._input_entry = ttk.Entry(frame, width=32)
        self._input_entry.grid(row=0, column=1, padx=(8, 8), sticky="ew")
        self._input_entry.insert(0, "meter:2.5")

        ttk.Button(frame, text="Convert", command=self._convert).grid(row=0, column=2)

        quick = ttk.Frame(frame)
        quick.grid(row=1, column=0, columnspan=3, sticky="w", pady=(10, 0))
        ttk.Label(quick, text="빠른 입력:").pack(side="left")
        for sample in ("meter:2.5", "feet:1", "yard:3"):
            ttk.Button(
                quick,
                text=sample,
                width=10,
                command=lambda s=sample: self._set_sample(s),
            ).pack(side="left", padx=(6, 0))

        format_row = ttk.Frame(frame)
        format_row.grid(row=2, column=0, columnspan=3, sticky="w", pady=(10, 0))
        ttk.Label(format_row, text="출력 형식:").pack(side="left")
        for label, value in (("Table", "table"), ("JSON", "json"), ("CSV", "csv")):
            ttk.Radiobutton(
                format_row,
                text=label,
                value=value,
                variable=self._format,
                command=self._convert,
            ).pack(side="left", padx=(8, 0))

        frame.columnconfigure(1, weight=1)

    def _build_result_section(self) -> None:
        frame = ttk.LabelFrame(self, text="변환 결과", padding=10)
        frame.pack(fill="both", expand=True)

        self._notebook = ttk.Notebook(frame)
        self._notebook.pack(fill="both", expand=True)

        table_tab = ttk.Frame(self._notebook)
        raw_tab = ttk.Frame(self._notebook)
        self._notebook.add(table_tab, text="표")
        self._notebook.add(raw_tab, text="원문")

        columns = ("unit", "input", "result")
        self._tree = ttk.Treeview(table_tab, columns=columns, show="headings", height=6)
        for col, heading in zip(columns, ("단위", "입력값", "결과")):
            self._tree.heading(col, text=heading)
            self._tree.column(col, width=120, anchor="center")
        self._tree.pack(fill="both", expand=True, side="left")

        scrollbar = ttk.Scrollbar(table_tab, orient="vertical", command=self._tree.yview)
        scrollbar.pack(side="right", fill="y")
        self._tree.configure(yscrollcommand=scrollbar.set)

        self._raw_text = tk.Text(raw_tab, wrap="none", font=("Consolas", 10))
        self._raw_text.pack(fill="both", expand=True)
        self._raw_text.configure(state="disabled")

    def _build_status_section(self) -> None:
        status_frame = ttk.Frame(self)
        status_frame.pack(fill="x", pady=(10, 0))

        units = ", ".join(default_registry().names())
        ttk.Label(status_frame, text=f"지원 단위: {units}").pack(anchor="w")
        self._status_label = ttk.Label(
            status_frame,
            textvariable=self._status,
            foreground="#333333",
        )
        self._status_label.pack(anchor="w", pady=(4, 0))

    def _set_sample(self, sample: str) -> None:
        self._input_entry.delete(0, tk.END)
        self._input_entry.insert(0, sample)
        self._convert()

    def _convert(self) -> None:
        input_text = self._input_entry.get().strip()
        fmt: FormatType = self._format.get()  # type: ignore[assignment]

        try:
            output = run(input_text, fmt)
        except ValueError as exc:
            self._status.set(str(exc))
            self._status_label.configure(foreground="#b00020")
            self._clear_results()
            return

        self._status.set("변환 완료")
        self._status_label.configure(foreground="#1b5e20")
        self._show_results(output, fmt)

    def _clear_results(self) -> None:
        for item in self._tree.get_children():
            self._tree.delete(item)
        self._set_raw_text("")

    def _show_results(self, output: str, fmt: FormatType) -> None:
        self._set_raw_text(output)

        for item in self._tree.get_children():
            self._tree.delete(item)

        if fmt != "table":
            self._notebook.select(1)
            return

        self._notebook.select(0)
        for line in output.splitlines():
            if not line.startswith("|") or line.startswith("+"):
                continue
            parts = [part.strip() for part in line.strip("|").split("|")]
            if len(parts) == 3 and parts[0] != "unit":
                self._tree.insert("", "end", values=tuple(parts))

    def _set_raw_text(self, text: str) -> None:
        self._raw_text.configure(state="normal")
        self._raw_text.delete("1.0", tk.END)
        self._raw_text.insert("1.0", text)
        self._raw_text.configure(state="disabled")


def main() -> None:
    app = UnitConverterApp()
    app.mainloop()


if __name__ == "__main__":
    main()
