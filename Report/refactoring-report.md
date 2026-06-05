# refactoring Report — Golden Master & SRP Safe Refactor

> 브랜치: `refactoring` | 작성일: 2026-06-05 | 프로젝트: UnitConverter_08

## 목표

- **Golden Master** 확보 후 동작 불변 Safe Refactor
- **NFR-02 SRP**: `input_parser` / `UnitRegistry` 단일 책임 분리 검증
- **PR #3·#4 리뷰** refactoring 후보 반영
- green 17건 + refactoring TC 유지 · `pytest -v` 전체 통과

## 수행 내용

### 1. Golden Master (D-GM-01~03)

| TC ID | 포맷 | 입력 | 역할 |
|-------|------|------|------|
| D-GM-01 | table | `meter:2.5` | §7.2 테두리 표 스냅샷 고정 |
| D-GM-02 | json | `meter:2.5` | flat JSON 스냅샷 고정 |
| D-GM-03 | csv | `meter:2.5` | 3열 CSV 스냅샷 고정 |

- 파일: `tests/test_golden_master.py`
- `cli.run()` 출력과 기대 문자열 1:1 비교 → 리팩터링 중 회귀 즉시 탐지

### 2. SRP 구조 검증 (D-SRP-01~03)

| TC ID | 검증 |
|-------|------|
| D-SRP-01 | Parser / Registry / Converter / Formatter 모듈 분리 (AST·import 경계) |
| D-SRP-02 | `input_parser` — 파싱만, registry·변환 없음 |
| D-SRP-03 | `UnitRegistry` — 등록·조회만, 파싱·I/O 없음 |

- 파일: `tests/test_srp.py`

### 3. Safe Refactor

| 변경 | 내용 |
|------|------|
| `app/input_parser.py` | FR-01 파싱 전용, `InvalidInputError` |
| `app/validators.py` | `NegativeValueError`, `UnknownUnitError` |
| `app/exceptions.py` | app 계층 예외 (PR #4: ValueError 단일 계층 분리) |
| `domain/unit_registry.py` | OCP 등록·조회 전용 |
| `cli.py` | `run(..., registry=None)` DI, `UnitConverterError` 처리 |
| `conftest.py` | `default_registry` fixture — `units.json` SSOT |
| `tests/test_converter.py` | fixture 사용, `_default_registry()` 리터럴 제거 |
| `tools/unit_converter_gui.py` | PRD 범위 외 GUI — `tools/` 이동 후 **PyQt6** 전환 |
| `requirements-gui.txt` | GUI 의존성 (`PyQt6>=6.6`) |

### 4. PR 리뷰 코멘트 참조 및 반영

아래는 refactoring 단계에서 **직접 참고·반영**한 팀 리뷰 코멘트입니다.  
green 단계에서 이미 닫힌 항목(D-OCP-01 구현 등)은 유지·회귀 방지(Golden Master)로 연결했습니다.

#### PR #3 — `[red] Dual-Track RED TC` ([PR #3](https://github.com/MINJU-KIMmm/UnitConverter_08/pull/3))

| # | 리뷰 코멘트 (요지) | 리뷰 URL | refactoring 반영 | 변경 파일 |
|---|-------------------|----------|------------------|-----------|
| 1 | **출력 SSOT** — U-FMT-01(3열 table)과 README 한 줄형(`2.5 meter = 8.2 feet`) 중 포맷 SSOT를 하나로 맞출 것 | [jeonggyunkim — Approve review](https://github.com/MINJU-KIMmm/UnitConverter_08/pull/3#pullrequestreview-4432733247) | green에서 table/JSON SSOT 구현 완료 → refactoring에서 **D-GM-01~03** Golden Master로 동작 잠금 | `tests/test_golden_master.py` |
| 2 | **U-OUT-01** — 「3줄 이상」 조건에 **입력 단위(meter) 줄·입력값 포함** 여부를 PRD Then에 명시 | [동일 review](https://github.com/MINJU-KIMmm/UnitConverter_08/pull/3#pullrequestreview-4432733247) | `test_u_out_01`에 `"2.5" in result.stdout` assert 추가 | `tests/test_cli.py` |
| 3 | **D-CNV-01 vs OCP** — D-CNV-01은 환산(FR-02) 검증; OCP 회귀는 green **D-OCP-01**으로 분리 | [동일 review](https://github.com/MINJU-KIMmm/UnitConverter_08/pull/3#pullrequestreview-4432733247) | green에서 D-OCP-01 구현 완료 → refactoring에서 **회귀 없음** 확인 (17건 유지) | `tests/test_converter.py` |

> PR #3 Verdict: **Approve** — staging merge 후 green P0 구현  
> red 단계 transcript·Report 반영: [Prompting/red-transcript.md](../Prompting/red-transcript.md) (User: 「D-CNV-01/OCP, 출력 SSOT, U-OUT-01 Then… 반영해줘」)

#### PR #4 — `[green] P0 최소 구현` ([PR #4](https://github.com/MINJU-KIMmm/UnitConverter_08/pull/4))

| # | 리뷰 코멘트 (요지) | 리뷰 URL | refactoring 반영 | 변경 파일 |
|---|-------------------|----------|------------------|-----------|
| 1 | **`_default_registry()` 리터럴** ↔ `config/units.json` — fixture로 SSOT 통일 | [jeonggyunkim — Approve review (REFACTOR 후보 #2)](https://github.com/MINJU-KIMmm/UnitConverter_08/pull/4#pullrequestreview-4433392482) · [yeonnwoo — PR comment](https://github.com/MINJU-KIMmm/UnitConverter_08/pull/4#issuecomment-4628203194) · [somin926kim — PR comment](https://github.com/MINJU-KIMmm/UnitConverter_08/pull/4#issuecomment-4628325308) | `conftest.py` `default_registry` fixture 추가; `test_converter.py`에서 `_default_registry()`·비율 리터럴 제거 | `conftest.py`, `tests/test_converter.py` |
| 2 | **`ValueError` 단일 계층** → domain/app exception 분리 (선택) | [jeonggyunkim — Approve review (REFACTOR 후보 #3)](https://github.com/MINJU-KIMmm/UnitConverter_08/pull/4#pullrequestreview-4433392482) | `app/exceptions.py` — `InvalidInputError`, `NegativeValueError`, `UnknownUnitError`; CLI stderr 메시지 문자열 유지 | `unit_converter/app/exceptions.py`, `input_parser.py`, `validators.py`, `cli.py` |
| 3 | **GUI는 PRD 범위 외** — refactoring 시 `tools/` 또는 README 표기 | [jeonggyunkim — Approve review (REFACTOR 후보 #4)](https://github.com/MINJU-KIMmm/UnitConverter_08/pull/4#pullrequestreview-4433392482) · [somin926kim — PR comment](https://github.com/MINJU-KIMmm/UnitConverter_08/pull/4#issuecomment-4628325308) | `unit_converter_gui.py` → `tools/unit_converter_gui.py` 이동; **PyQt6** GUI로 전환; README §7 안내 | `tools/unit_converter_gui.py`, `requirements-gui.txt`, `README.md` |
| 4 | **green-report「1 RED 묶음 = 1 커밋」** — 실제는 Track B/A bulk 2커밋 + 후속 5커밋; 문구 정정 권장 | [jeonggyunkim — Approve review (REFACTOR 후보 #1)](https://github.com/MINJU-KIMmm/UnitConverter_08/pull/4#pullrequestreview-4433392482) | green-report 목표 문구를 실제 7커밋 구조에 맞게 수정 | `Report/green-report.md` |
| 5 | **NFR-02 SRP** — refactoring 단계에서 진행 | [jeonggyunkim — Approve review](https://github.com/MINJU-KIMmm/UnitConverter_08/pull/4#pullrequestreview-4433392482) · [yeonnwoo — PR comment](https://github.com/MINJU-KIMmm/UnitConverter_08/pull/4#issuecomment-4628203194) | **D-SRP-01~03** SRP 구조 검증 TC 추가; `input_parser` / `UnitRegistry` 모듈 경계 강화 | `tests/test_srp.py`, `unit_converter/app/input_parser.py`, `unit_converter/domain/unit_registry.py`, `unit_converter/cli.py` |

> PR #4 Verdict: **Approve** — staging merge OK; refactoring에서 NFR-02 SRP 진행  
> yeonnwoo 코멘트 원문: 「refactoring 단계에서 `tests/test_converter.py`의 `_default_registry()` 비율 리터럴을 `config/units.json` SSOT로 통일하면 테스트·설정 간 드리프트를 예방할 수 있을 것 같습니다.」

#### 반영 요약 (PR #3·#4)

| PR | 피드백 | refactoring 반영 |
|----|--------|------------------|
| #3 | D-OCP-01 green 예약 | ✅ green 완료 (유지) |
| #3 | 출력 SSOT table default | ✅ Golden Master로 잠금 |
| #3 | U-OUT-01 입력 단위·값 포함 | ✅ `test_cli.py` `2.5` assert 추가 |
| #4 | `_default_registry()` ↔ `units.json` | ✅ conftest fixture SSOT |
| #4 | app 예외 계층 (선택) | ✅ `app/exceptions.py` |
| #4 | GUI PRD 외 → `tools/` | ✅ `tools/unit_converter_gui.py` |
| #4 | green-report「1묶음=1커밋」 | ✅ 실제 7커밋 구조로 문구 정정 |

## PRD 매핑

| ID | TC ID | 파일 | 상태 |
|----|-------|------|------|
| NFR-01 | D-OCP-01 | test_converter.py | ✅ |
| NFR-02 | D-SRP-01~03, D-GM-01~03 | test_srp.py, test_golden_master.py | ✅ |
| FR-02 | D-GM-01~03, U-OUT-01 | test_golden_master.py, test_cli.py | ✅ |
| FR-01 | U-PAR-01 | test_cli.py | ✅ |
| EXT-03 | U-FMT-01~03 | test_cli.py | ✅ |

## TC 목록 · 결과

### 검증 명령

```bash
venv\Scripts\activate
pytest -v
```

### 요약

```text
pytest -v  →  23 passed, 0 failed, 0 skipped
```

| 구분 | TC 수 | 결과 |
|------|-------|------|
| green (기존) | 17 | ✅ |
| Golden Master | 3 | ✅ |
| SRP | 3 | ✅ |

### 실행 환경 (2026-06-05)

| 항목 | 값 |
|------|-----|
| 브랜치 | `refactoring` |
| Python | 3.10.11 |
| pytest | 9.0.3 |
| PyQt6 | 6.11.0 (GUI, PRD 외) |

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
tests/test_golden_master.py::test_d_gm_01_golden_master_table PASSED
tests/test_golden_master.py::test_d_gm_02_golden_master_json PASSED
tests/test_golden_master.py::test_d_gm_03_golden_master_csv PASSED
tests/test_srp.py::test_d_srp_01_parser_registry_converter_formatter_separated PASSED
tests/test_srp.py::test_d_srp_02_input_parser_only_parses PASSED
tests/test_srp.py::test_d_srp_03_registry_only_manages_units PASSED
```

## 결과

| 항목 | 상태 |
|------|------|
| Golden Master 확보 | ✅ |
| input_parser / UnitRegistry SRP 분리 검증 | ✅ |
| PR #3·#4 리뷰 후보 반영 | ✅ |
| Safe Refactor (DI, fixture SSOT, exceptions) | ✅ |
| PyQt6 GUI (`tools/`, PRD 외) | ✅ |
| `Report/refactoring-report.md` | ✅ (본 문서) |
| `Prompting/refactoring-transcript.md` | ✅ |
| PR → staging | ⏳ 사용자 요청 시 |

**다음 단계:** 팀 리뷰 → `staging` merge → `new_features` 브랜치 (EXT-01~03)

## 회고

### AI 활용

- Golden Master 선행 확보로 Safe Refactor 시 **동작 불변** 검증 자동화
- PR #3·#4 GitHub 리뷰 URL·코멘트를 Report §4에 추적성 매핑
- SRP AST 검증 TC로 NFR-02 구조 리뷰를 자동화

### 도움이 된 순간

- `_default_registry()` 제거 → `conftest` fixture + `units.json` SSOT로 테스트·설정 드리프트 방지
- PR #4 예외 계층 분리 후에도 CLI stderr 메시지 유지 → 기존 17 TC 무수정 통과
- GUI PyQt6 전환 시 `cli.run()` 재사용으로 domain/app 변경 없음

### 한계·결정 사항

| 항목 | 결정 |
|------|------|
| green 모듈 추출 선행 | refactoring은 GM + SRP 검증 + 리뷰 후보에 집중 |
| CSV Golden Master | Windows `\r\n` 정규화 후 비교 |
| GUI | PRD 범위 외 — `tools/` + PyQt6, `requirements-gui.txt` 분리 |

### 다음 단계 메모

1. Cursor **Export Transcript** → `Prompting/refactoring-transcript.md` 갱신 (대화 원본 보존)
2. commit: `[refactoring] NFR-02 SRP · Golden Master · PR #4 리뷰 반영`
3. PR → **staging** (사용자 요청 시)
4. `new_features` 브랜치 — EXT-01~03
