# green Report — 최소 구현 (Dual-Track)

> 브랜치: `green` | 작성일: 2026-06-05 | 프로젝트: UnitConverter_08

## 목표

- RED 16건 TC를 통과하는 **최소 구현** (Track B → Track A, 1 RED 묶음당 1 커밋)
- PRD §7.3 출력 SSOT(table 기본) 반영
- green 예정 **D-OCP-01** (NFR-01 OCP 회귀) 추가
- `pytest -v` 전 TC 통과

## 수행 내용

### 1. Track B — Domain 구현 (`172bfba`)

| 모듈 | 역할 |
|------|------|
| `unit_converter/domain/` | `RatioUnit`, `UnitRegistry`, `Converter` |
| `unit_converter/infrastructure/config_loader.py` | `ConfigError`, JSON → Registry |
| `config/units.json` | meter/feet/yard 비율 (부록 §7.1) |

| TC ID | PRD | 결과 |
|-------|-----|------|
| D-CNV-01~04 | FR-02 | ✅ |
| D-REG-01 | EXT-02 | ✅ |
| D-CFG-01 | EXT-01 | ✅ |

### 2. Track A — CLI 구현 (`109c899`)

| 모듈 | 역할 |
|------|------|
| `unit_converter/app/input_parser.py` | FR-01 `unit:value` 파싱 |
| `unit_converter/app/validators.py` | FR-03~05 검증 |
| `unit_converter/app/output_formatter.py` | EXT-03 table/json/csv |
| `unit_converter/cli.py`, `__main__.py` | CLI 진입점 |

| TC ID | PRD | 결과 |
|-------|-----|------|
| U-PAR-01 | FR-01 | ✅ |
| U-IN-01~05 | FR-03~05 | ✅ |
| U-OUT-01 | FR-02 | ✅ |
| U-FMT-01~03 | EXT-03 | ✅ |

### 3. 출력 SSOT 보강 (부록 §7.2)

- **table:** 테두리 ASCII 표 (`unit | input | result`), 소수 4자리 (`8.2021`, `2.7340`)
- **json:** flat 객체 (`{"meter": 2.5, "feet": 8.2021, ...}`) — `units.json` 형태
- **csv:** 3열 (`unit,input,result`)

### 4. D-OCP-01 — NFR-01 OCP 회귀

- `tmp_path/units.json`에 `inch: 39.3701` 추가
- **`converter.py` 소스 변경 없이** `load_registry_from_json` → `Converter` 로 변환 검증
- 1 inch → 0.0254 m (±ε)

### 5. 검증용 GUI (PRD 외 편의)

- `unit_converter_gui.py` — tkinter, `cli.run()` 재사용
- table / json / csv 원문·표 탭 표시

## PRD 매핑

| ID | TC ID | 파일 | 상태 |
|----|-------|------|------|
| FR-01 | U-PAR-01 | test_cli.py | ✅ |
| FR-02 | U-OUT-01, D-CNV-01~04 | test_cli.py, test_converter.py | ✅ |
| FR-03 | U-IN-04 | test_cli.py | ✅ |
| FR-04 | U-IN-03 | test_cli.py | ✅ |
| FR-05 | U-IN-01, U-IN-02, U-IN-05 | test_cli.py | ✅ |
| NFR-01 | D-REG-01, D-OCP-01 | test_converter.py | ✅ |
| NFR-02 | — | 구조 분리 *(리뷰)* | 🔄 refactoring 예정 |
| EXT-01 | D-CFG-01 | test_converter.py | ✅ |
| EXT-02 | D-REG-01 | test_converter.py | ✅ |
| EXT-03 | U-FMT-01~03 | test_cli.py | ✅ |

## TC 목록 · 결과

### 검증 명령

```bash
venv\Scripts\activate
pytest -v
```

### 실행 환경 (2026-06-05)

| 항목 | 값 |
|------|-----|
| 브랜치 | `green` |
| Python | 3.10.11 |
| pytest | 9.0.3 |
| 실행 경로 | `C:\DEV\UnitConverter_08\venv\Scripts\python.exe` |

### 요약

```text
pytest -v  →  17 passed, 0 failed, 0 skipped  (2.41s)
```

| Track | TC 수 | 결과 |
|-------|-------|------|
| B (Domain) | 7 | ✅ |
| A (CLI) | 10 | ✅ |

### 상세 로그

```text
tests/test_cli.py::test_u_par_01_parse_unit_value PASSED
tests/test_cli.py::test_u_in_01_empty_input_format_error PASSED
tests/test_cli.py::test_u_in_02_missing_colon_form_error PASSED
tests/test_cli.py::test_u_in_03_negative_value_rejected PASSED
tests/test_cli.py::test_u_in_04_unknown_unit_rejected PASSED
tests/test_cli.py::test_u_in_05_invalid_format_non_numeric PASSED
tests/test_cli.py::test_u_out_01_valid_input_multi_line_output PASSED
tests/test_cli.py::test_u_fmt_01_format_table_three_columns PASSED
tests/test_cli.py::test_u_fmt_02_format_json PASSED
tests/test_cli.py::test_u_fmt_03_format_csv PASSED
tests/test_converter.py::test_d_cnv_01_to_meter_feet PASSED
tests/test_converter.py::test_d_cnv_02_convert_all_meter_to_feet PASSED
tests/test_converter.py::test_d_cnv_03_convert_all_feet_to_yard_via_meter PASSED
tests/test_converter.py::test_d_cnv_04_convert_all_meter_to_yard PASSED
tests/test_converter.py::test_d_reg_01_register_cubit PASSED
tests/test_converter.py::test_d_cfg_01_load_json_corrupted_config_error PASSED
tests/test_converter.py::test_d_ocp_01_inch_via_config_without_converter_change PASSED
```

## 결과

| 항목 | 상태 |
|------|------|
| RED 16건 green 구현 | ✅ |
| D-OCP-01 (NFR-01) | ✅ |
| 출력 SSOT (§7.2 table, JSON flat) | ✅ |
| GUI 검증 도구 | ✅ |
| `Report/green-report.md` | ✅ (본 문서) |
| PR → staging | ⏳ PR 생성 |

**다음 단계:** 팀 리뷰 → `staging` merge → `refactoring` 브랜치 (NFR-02 SRP)

## 회고

- Dual-Track 1:1 커밋으로 RED 묶음 추적성 유지
- D-CNV-01(환산) vs D-OCP-01(OCP) 분리로 NFR-01 검증 명확화
- 부록 table 형식·JSON flat 객체는 사용자 확인 피드백으로 SSOT 정렬
- GUI는 PRD 범위 밖이나 수동 검증에 유용
