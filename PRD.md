# PRD — Unit Converter (Python)

> **Single Source of Truth** for requirements and test traceability.  
> 원본: `README.md` · 실습 슬라이드 · 부록(Appendix) · 목표 아키텍처 통합  
> 프로젝트: `UnitConverter_08`

---

## 1. PRD 요약 — 무엇을 만드는가

**길이 단위 변환 CLI**를 PRD·테스트 추적 가능하게 재구현한다.

| 항목 | 내용 |
|------|------|
| **입력** | `unit:value` 형식 (예: `meter:2.5`) |
| **기준 단위** | meter |
| **지원 단위** | meter, feet, yard |
| **변환 비율** | 1 m = 3.28084 ft = 1.09361 yd (feet↔yard는 meter 경유) |
| **품질** | OCP, SRP, 입력 검증 (음수·형식·unknown unit) |
| **실행** | `python -m unit_converter "meter:2.5"` |

### 기대 출력 예시

```bash
python -m unit_converter "meter:2.5"
# (기본 또는 --format table)
# meter  2.5  → 2.5
# feet   2.5  → 8.2021
# yard   2.5  → 2.7340
```

---

## 2. 기능 요구사항 (FR) — P0

| ID | 요구 | 설명 |
|----|------|------|
| **FR-01** | 입력 파싱 | `meter:2.5` → `unit=meter`, `value=2.5` |
| **FR-02** | 전 단위 출력 | `meter 2.5` 입력 시 feet=`8.2021`, yard=`2.7340` 등 전 단위 변환 결과 |
| **FR-03** | unknown unit | 미등록 단위 `cubit:1` → 명확한 에러 메시지 |
| **FR-04** | 음수 거부 | `meter:-1` → 거부 / 예외 |
| **FR-05** | 형식 오류 | `meter / abc`, `meter`(콜론 없음), 빈 입력 → 형식 에러 |

---

## 3. 비기능 요구사항 (NFR) — P0

| ID | 요구 | 설명 |
|----|------|------|
| **NFR-01** | OCP (개방-폐쇄) | `inch` 등 새 단위 추가 시 **기존 converter 코드 수정 없음** (Registry 등록 또는 config 추가) |
| **NFR-02** | SRP (단일 책임) | **Parser / Registry / Converter / Formatter** 분리 |

---

## 4. 추가 요구사항 (EXT) — P1

| ID | 요구 | 설명 |
|----|------|------|
| **EXT-01** | 설정 외부화 | `units.json` 또는 YAML에서 변환 비율 로드 |
| **EXT-02** | 동적 등록 | `1 cubit = 0.4572 meter` 입력 → 즉시 변환 가능 |
| **EXT-03** | 출력 포맷 | `--format json \| csv \| table` |

---

## 5. 비즈니스 로직

```
1 meter = 3.28084 feet
1 meter = 1.09361 yard
feet ↔ yard 변환은 meter 기준으로 계산
```

변환 공식 (meter 기준):

```
result = input_value × (ratio_from / ratio_to)
```

---

## 6. PRD → 테스트 추적표

| ID | 요구 | Given | Then | P | TC ID | 테스트 파일 |
|----|------|-------|------|---|-------|-------------|
| FR-01 | `meter:2.5` 파싱 | 유효 문자열 `meter:2.5` | `value=2.5`, `unit=meter` | P0 | U-PAR-01 | `tests/test_cli.py` |
| FR-02 | 전 단위 출력 | `meter:2.5` | domain: feet=`8.2021`, yard=`2.7340` · CLI: **등록 단위별 1줄 이상, 입력 단위(meter) 줄 포함**, 최소 3줄(meter/feet/yard) | P0 | U-OUT-01, D-CNV-01~04 | `tests/test_cli.py`, `tests/test_converter.py` |
| FR-03 | unknown unit | `cubit:1` (미등록) | 명확한 에러 | P0 | U-IN-04 | `tests/test_cli.py` |
| FR-04 | 음수 | `meter:-1` | 거부 / 예외 | P0 | U-IN-03 | `tests/test_cli.py` |
| FR-05 | 형식 오류 | `meter`, 빈 입력, `meter / abc` | 형식 에러 | P0 | U-IN-01, U-IN-02, U-IN-05 | `tests/test_cli.py` |
| NFR-01 | OCP | `inch` 추가 | converter 기존 코드 미수정 | P0 | D-REG-01, **D-OCP-01** | `tests/test_converter.py` |
| NFR-02 | SRP | — | Parser/Registry/Converter/Formatter 분리 | P0 | D-SRP-01~03, D-GM-01~03 | `tests/test_srp.py`, `tests/test_golden_master.py` |
| EXT-01 | config | `units.json` | 비율 로드 | P1 | D-CFG-01 | `tests/test_converter.py` |
| EXT-02 | 동적 등록 | `1 cubit = 0.4572 m` | 즉시 변환 | P1 | D-REG-01 | `tests/test_converter.py` |
| EXT-03 | 출력 포맷 | `--format` | json/csv/table 검증 | P1 | U-FMT-01, U-FMT-02, U-FMT-03 | `tests/test_cli.py` |

### Track A / Track B

| Track | 파일 | 범위 |
|-------|------|------|
| **A** (Boundary) | `tests/test_cli.py` | FR-01, FR-03~05, EXT-03 — U-PAR-01, U-IN-*, U-OUT-01, U-FMT-* |
| **B** (Domain) | `tests/test_converter.py` | FR-02 (D-CNV-*), EXT-01~02, NFR-01 (D-REG-01, D-OCP-01), D-CFG-01 |

---

## 7. 부록 (Appendix) — 설정 · 출력

### 7.1 `config/units.json` (meter = 1.0 기준, flat)

```json
{
  "meter": 1.0,
  "feet": 3.28084,
  "yard": 1.09361
}
```

### 7.2 `--format table` 출력

입력: `meter:2.5`

| unit | input | result |
|------|-------|--------|
| meter | 2.5 | 2.5 |
| feet | 2.5 | 8.2021 |
| yard | 2.5 | 2.7340 |

- **소수 자릿수:** 부록 기준 **4자리** (`8.2021`, `2.7340`)
- README 예시(`8.2 feet`)와 상이 → **본 PRD·부록 우선**

### 7.3 출력 포맷 SSOT (green 구현 기준)

| 구분 | SSOT | 비고 |
|------|------|------|
| **기본(default)** | §7.2 **table** 3열 (`unit` \| `input` \| `result`) | CLI 인자 없을 때와 `--format table` 동일 |
| **명시 포맷** | `--format json` \| `csv` \| `table` | EXT-03 · U-FMT-01~03 |
| **비-SSOT** | README 한 줄형 `2.5 meter = 8.2 feet` | 레거시 **참고용**, green에서 구현 대상 아님 |

U-FMT-01(3열 table)과 U-OUT-01(다줄 출력)은 **동일 table SSOT**를 따른다. U-OUT-01은 formatter 미지정 시 default table 행 수로 검증한다.

### 7.4 CLI

```bash
python -m unit_converter "meter:2.5"
python -m unit_converter "meter:2.5" --format table
python -m unit_converter "meter:2.5" --format json
python -m unit_converter "meter:2.5" --format csv
```

---

## 8. 목표 아키텍처 (Target Architecture)

```
unit_converter/
├── domain/
│   ├── length_unit.py       # LengthUnit Protocol (name, to_meter) — OCP
│   ├── unit_registry.py     # 단위 등록/조회 — OCP 핵심
│   └── converter.py         # meter 기준 변환 — SRP
├── infrastructure/
│   └── config_loader.py     # JSON/YAML → Registry (EXT-01)
├── app/
│   ├── input_parser.py      # unit:value (FR-01)
│   ├── validators.py        # FR-03~05
│   ├── unit_registration_parser.py  # EXT-02
│   └── output_formatter.py  # json | csv | table (EXT-03)
├── cli.py                   # 진입점
tests/
├── test_converter.py        # Track B
└── test_cli.py              # Track A
config/units.json
```

**OCP:** 새 단위 = `LengthUnit` 구현 + `registry.register()` 또는 config 1줄 추가  
**SRP:** 변환 ≠ 파싱 ≠ 출력 ≠ 설정 로드

---

## 9. 구현 우선순위 (Activities)

| 순서 | 브랜치 | P | 대상 ID |
|------|--------|---|---------|
| 1 | spec | — | 분석·설계 (본 PRD) |
| 2 | red | P0 | FR-01~05, NFR-01~02 TC (RED) |
| 3 | green | P0 | FR-01~05, NFR-01~02 구현 |
| 4 | refactoring | P0 | NFR-01 OCP, NFR-02 SRP |
| 5 | new_features | P1 | EXT-01~03 |

---

## 10. 관련 문서

| 문서 | 역할 |
|------|------|
| **`PRD.md`** (본 문서) | 요구사항·추적표 SSOT |
| `README.md` | 프로젝트 소개·환경 설정·Activities |
| `Report/spec-report.md` | spec 단계 분석·설계 Report |
| `Report/red-report.md` | red 단계 TC Report |

---

## 11. RED TC 목록 (red 브랜치)

> 상태: **RED 스켈레톤** (`pytest.fail("RED: ...")`) · skip/xfail 금지 · green 단계에서 본문 구현

### Track A — `tests/test_cli.py` (10건)

| TC ID | PRD | 시나리오 | 상태 |
|-------|-----|----------|------|
| U-PAR-01 | FR-01 | `meter:2.5` → `unit=meter`, `value=2.5` | ✅ RED |
| U-IN-01 | FR-05 | 빈 입력 → 형식 에러 | ✅ RED |
| U-IN-02 | FR-05 | `meter` (콜론 없음) → 형식 에러 | ✅ RED |
| U-IN-03 | FR-04 | `meter:-1` → 음수 거부 | ✅ RED |
| U-IN-04 | FR-03 | `cubit:1` (미등록) → unknown unit 에러 | ✅ RED |
| U-IN-05 | FR-05 | `meter / abc` → 형식 에러 | ✅ RED |
| U-OUT-01 | FR-02 | `meter:2.5` → 등록 3단위 각 1줄(**meter 줄 포함**), ≥3줄 | ✅ RED |
| U-FMT-01 | EXT-03 | `--format table` 3열 출력 | ✅ RED |
| U-FMT-02 | EXT-03 | `--format json` | ✅ RED |
| U-FMT-03 | EXT-03 | `--format csv` | ✅ RED |

### Track B — `tests/test_converter.py` (7건)

| TC ID | PRD | 시나리오 | 상태 |
|-------|-----|----------|------|
| D-CNV-01 | FR-02 | `to_meter` — 1 feet → 0.3048 m (±ε), 환산 정확성 | ✅ GREEN |
| D-CNV-02 | FR-02 | `convert_all` — 2.5 m → 8.2021 ft | ✅ GREEN |
| D-CNV-03 | FR-02 | feet→yard, meter 경유 일치 | ✅ GREEN |
| D-CNV-04 | FR-02 | `convert_all` — 2.5 m → 2.7340 yd | ✅ GREEN |
| D-REG-01 | EXT-02 | `cubit 0.4572` 등록 → 변환 가능 | ✅ GREEN |
| D-CFG-01 | EXT-01 | 깨진 JSON → `ConfigError` | ✅ GREEN |
| D-OCP-01 | NFR-01 | `units.json`에 `inch` 추가 — `converter.py` 무변경 | ✅ GREEN |

**합계:** 23건 REFACTORING · green 17건 + GM 3건 + SRP 3건

---

## 13. refactoring 단계 TC (PR #4 리뷰 반영)

| TC ID | PRD | 시나리오 | 비고 |
|-------|-----|----------|------|
| D-GM-01~03 | FR-02, EXT-03 | `meter:2.5` table/json/csv Golden Master | 리팩터링 전 동작 잠금 |
| D-SRP-01~03 | NFR-02 | Parser/Registry/Converter/Formatter 모듈 분리 | AST·행위 검증 |
| *(PR #4 REFACTOR)* | — | `_default_registry()` → `conftest` fixture + `units.json` SSOT | `test_converter.py` |
| *(PR #4 REFACTOR)* | — | `app/exceptions.py` — 입력·검증 예외 계층 | CLI stderr 메시지 유지 |
| *(PR #4 REFACTOR)* | — | GUI → `tools/` PyQt6 (PRD 범위 외) | `tools/unit_converter_gui.py`, `requirements-gui.txt` |

## 12. green 단계 완료 TC (PR #3 리뷰 반영)

| TC ID | PRD | 시나리오 | 비고 |
|-------|-----|----------|------|
| **D-OCP-01** | NFR-01 | `units.json`에 `inch` 추가 후 **`converter.py` 소스 변경 없음** (Registry/config만) | RED의 D-CNV-01은 **환산 검증**(FR-02)이며 OCP 회귀 TC가 아님 |
| *(기존 RED 16건)* | FR-02 / EXT | D-CNV-01~04, U-OUT-01, U-FMT-* 등 | green에서 `pytest.fail` → 본문 구현 완료 |

### PR #3 리뷰 요약

- **Verdict:** Approve — staging merge 후 green P0 구현
- **잘한 점:** Dual Track, TC ID 1:1, FR-02 경계/도메인 분리, Track B→A 커밋·산출물
- **반영:** 출력 SSOT(§7.3), U-OUT-01 Then(입력 단위 줄 포함), D-CNV-01↔FR-02 라벨, D-OCP-01 green 예약
