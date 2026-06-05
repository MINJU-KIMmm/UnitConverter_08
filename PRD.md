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
| FR-01 | `meter:2.5` 파싱 | 유효 문자열 `meter:2.5` | `value=2.5`, `unit=meter` | P0 | *(파서 단위 TC)* | `tests/test_cli.py` |
| FR-02 | 전 단위 출력 | `meter:2.5` | feet=`8.2021`, yard=`2.7340` | P0 | D-CNV-02 | `tests/test_converter.py` |
| FR-03 | unknown unit | `cubit:1` (미등록) | 명확한 에러 | P0 | *(추가 예정)* | `tests/test_cli.py` |
| FR-04 | 음수 | `meter:-1` | 거부 / 예외 | P0 | U-IN-03 | `tests/test_cli.py` |
| FR-05 | 형식 오류 | `meter`, 빈 입력, `meter / abc` | 형식 에러 | P0 | U-IN-01, U-IN-02 | `tests/test_cli.py` |
| NFR-01 | OCP | `inch` 추가 | converter 기존 코드 미수정 | P0 | D-CNV-01~03, D-REG-01 | `tests/test_converter.py` |
| NFR-02 | SRP | — | Parser/Registry/Converter/Formatter 분리 | P0 | *(구조 리뷰)* | — |
| EXT-01 | config | `units.json` | 비율 로드 | P1 | D-CFG-01 | `tests/test_converter.py` |
| EXT-02 | 동적 등록 | `1 cubit = 0.4572 m` | 즉시 변환 | P1 | D-REG-01 | `tests/test_converter.py` |
| EXT-03 | 출력 포맷 | `--format` | json/csv/table 검증 | P1 | *(추가 예정)* | `tests/test_cli.py` |

### Track A / Track B

| Track | 파일 | 범위 |
|-------|------|------|
| **A** (Boundary) | `tests/test_cli.py` | FR-03~05, EXT-03, U-IN-*, U-OUT-* |
| **B** (Domain) | `tests/test_converter.py` | FR-02, EXT-01~02, D-CNV-*, D-REG-*, D-CFG-* |

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

### 7.3 CLI

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
| `Report/red-report.md` | red 단계 TC Report (예정) |

---

## 11. 미작성 TC (red 브랜치 추가 예정)

| TC ID | 대상 | 시나리오 |
|-------|------|----------|
| U-IN-04 | FR-03 | `cubit:1` (미등록) → unknown unit 에러 |
| U-FMT-01 | EXT-03 | `--format table` 3열 출력 |
| U-FMT-02 | EXT-03 | `--format json` |
| U-FMT-03 | EXT-03 | `--format csv` |
| U-OUT-01 | FR-02 | `meter:2.5` → 3줄 이상 출력 (기존 스켈레톤) |
