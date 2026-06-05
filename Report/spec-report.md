# spec Report — 분석·설계

> 브랜치: `spec` | 작성일: 2026-06-05 | 프로젝트: UnitConverter_08
> 최종 갱신: 목표 아키텍처·부록(Appendix) 스펙 반영

## 목표

- PRD(`README.md`)와 레거시 코드(`UnitConverter.py`) 분석
- 레거시 코드 스멜 및 PRD 갭 식별
- **목표 아키텍처(Target Architecture)** 기준 OCP/SRP 패키지 구조 확정
- FR/NFR 매핑, 부록 출력/`units.json` 스펙, Git 워크플로우·산출물 규칙 수립

## 수행 내용

### 1. 레거시 코드 분석

`UnitConverter.py`(37줄)는 `main()` 단일 함수에 입력·검증·변환·출력이 모두 포함된 절차적 스크립트이다.

**식별된 코드 스멜 (18건)**

| 구분 | 스멜 | 핵심 |
|------|------|------|
| 구조·설계 | God Function, OCP/SRP 위반, 매직 넘버, 중복 로직, 확장 불가 | if/elif 하드코딩, 3단위 고정 |
| 입력·검증 | 형식 검증 불완전, 음수 미검증, 공백/대소문자 미처리 | PRD 품질 요구 미충족 |
| 출력·정확度 | 반올림 불일치, 자기 단위 중복 출력, 정밀도 정책 없음 | README·부록 스펙과 불일치 |
| 테스트·유지보수 | I/O 결합, 테스트 부재, 타입/문서 부재, 설정 외부화 없음 | Activities 2~4 전면 미착수 |

### 2. PRD 갭 분석

| 영역 | PRD | 현재 | 갭 |
|------|-----|------|-----|
| 기본 FR | 입력 파싱, 3단위 변환, OCP 확장, TC | 변환만 부분 구현 | OCP·TC **미구현** |
| 품질 NFR | OCP, SRP, 입력 검증 | 단일 함수, 검증 부분 | **전면 미구현** |
| 추가 FR | 설정 외부화, 동적 등록, 출력 포맷 | 없음 | **전면 미구현** |

**현재 달성도:** Activities 1단계(분석·설계) ✅ / 2~4단계 ❌

### 3. 목표 아키텍처 (확정)

슬라이드 **Target Architecture (Python)** + PRD/부록 요구사항을 반영한 최종 구조.

```
UnitConverter_08/
├── config/
│   └── units.json                      # 부록: meter=1.0 기준 flat JSON
├── unit_converter/
│   ├── domain/
│   │   ├── length_unit.py              # LengthUnit Protocol (name, to_meter) — OCP
│   │   ├── unit_registry.py            # 단위 등록/조회 — OCP 핵심
│   │   └── converter.py                # meter 기준 변환 — SRP
│   ├── infrastructure/
│   │   └── config_loader.py            # JSON/YAML → Registry
│   ├── app/
│   │   ├── input_parser.py             # "unit:value" 파싱
│   │   ├── validators.py               # 음수·형식·unknown unit (PRD 필수)
│   │   ├── unit_registration_parser.py # "1 cubit = 0.4572 meter" (FR-08)
│   │   └── output_formatter.py         # json | csv | table (--format)
│   └── cli.py                          # CLI 진입점, 컴포넌트 조합
├── tests/
│   ├── test_converter.py               # Track B — domain 로직
│   └── test_cli.py                     # Track A — CLI 경계
├── Report/                             # ARRR 단계 Report (팀 규칙)
├── Prompting/                          # Export Transcript (팀 규칙)
├── UnitConverter.py                    # (선택) 하위 호환 thin wrapper
└── README.md
```

#### OCP / SRP 원칙 (목표 아키텍처)

| 원칙 | 적용 |
|------|------|
| **OCP** | 새 단위 = `LengthUnit` 구현 + `registry.register()` 또는 `units.json` 1줄 추가. **기존 converter 코드 수정 없음** |
| **SRP** | 변환 ≠ 파싱 ≠ 출력 ≠ 설정 로드 → **Parser, Registry, Converter, Formatter** 4모듈 분리 |

#### 초기 설계 대비 변경 사항

| 변경 | 이유 |
|------|------|
| `validation/` + `output/` + `application/` → **`app/`** 통합 | 목표 아키텍처 단순화 |
| `cli/main.py` → **`cli.py`** | 슬라이드 진입점 일치 |
| `models.py` → **`length_unit.py` Protocol** | OCP 명시 |
| `output/*_formatter.py` 분리 → **`output_formatter.py` 1파일** | 슬라이드 일치, 내부 Strategy로 확장 |
| `tests/unit/` → **Track A/B** | `test_converter.py` + `test_cli.py` |
| `validators.py`, `unit_registration_parser.py` **유지** | PRD NFR-03, FR-08 (슬라이드 미포함) |

### 4. 부록(Appendix) — 설정·출력 스펙

#### config/units.json (flat, meter=1.0 기준)

```json
{
  "meter": 1.0,
  "feet": 3.28084,
  "yard": 1.09361
}
```

#### `--format table` 출력 (입력: `meter:2.5`)

```
| unit  | input | result  |
| meter | 2.5   | 2.5     |
| feet  | 2.5   | 8.2021  |
| yard  | 2.5   | 2.7340  |
```

- `input`: 사용자가 입력한 원본 값
- `result`: 해당 단위로 변환된 값
- **소수 자릿수:** 부록 기준 **4자리** (`8.2021`, `2.7340`). README 예시(8.2)와 상이 → **부록 우선**, TC-FMT-01에서 검증

#### CLI 옵션 (설계)

```bash
python -m unit_converter --format table    # table | json | csv
```

### 5. Git 워크플로우 Rule 등록

`.cursor/rules/git-workflow.mdc` 등록 (`alwaysApply: true`)

- 브랜치: `main` → `staging` → `spec|red|green|refactoring|new_features`
- ARRR 순서, 팀 리뷰 3원칙, PRD→TC→Code 추적성
- `Report/`, `Prompting/` 산출물 규칙 포함

## PRD 매핑

### 기능 요구사항 (FR)

| ID | PRD 요구사항 | 담당 모듈 | 구현 브랜치 |
|----|-------------|-----------|-------------|
| FR-01 | `unit:value` 입력 파싱 | `app/input_parser.py` | green |
| FR-02 | 모든 단위로 변환 출력 | `domain/converter.py` + `app/output_formatter.py` | green |
| FR-03 | meter/feet/yard 지원 | `config/units.json` + `domain/unit_registry.py` | green |
| FR-04 | meter 기준 비즈니스 로직 | `domain/converter.py` | green |
| FR-05 | 변환 결과 표시 | `app/output_formatter.py` (table 4자리) | green |
| FR-06 | 단위 추가 시 변경 최소화 | `domain/length_unit.py` + `unit_registry.py` | refactoring |
| FR-07 | 설정 외부화 (JSON/YAML) | `infrastructure/config_loader.py` | new_features |
| FR-08 | 동적 단위 등록 | `app/unit_registration_parser.py` + `register()` | new_features |
| FR-09 | 출력 포맷 선택 (JSON/CSV/표) | `app/output_formatter.py` + `cli.py --format` | new_features |

### 비기능 요구사항 (NFR)

| ID | PRD 요구사항 | 담당 모듈 | 검증 TC |
|----|-------------|-----------|---------|
| NFR-01 | OCP | `length_unit`, `unit_registry`, `config_loader` | TC-OCP-01~02 |
| NFR-02 | SRP | domain / app / infrastructure / cli 분리 | TC-SRP-01 |
| NFR-03 | 입력 검증 (음수, 형식, 없는 단위) | `app/validators.py` | TC-VAL-01~04 |
| NFR-04 | 변환 정확성 테스트 | `domain/converter.py` | TC-CONV-01~03 |
| NFR-05 | 테스트 용이성 | domain I/O 분리 | Track B |
| NFR-06 | 유지보수성 | `cli.py` 조합 | Track A |

### TC 목록 (red 브랜치 작성 예정)

#### Track B — domain (`tests/test_converter.py`)

| TC ID | 대상 | 시나리오 | 상태 |
|-------|------|----------|------|
| TC-CONV-01 | FR-04 | 2.5 meter → feet = 8.2021 | 예정 |
| TC-CONV-02 | FR-04 | 2.5 meter → yard = 2.7340 | 예정 |
| TC-CONV-03 | FR-04 | feet→yard meter 경유 변환 | 예정 |
| TC-OCP-01 | NFR-01 | units.json에 단위 추가 시 converter 미수정 | 예정 |
| TC-REG-01 | FR-08 | `1 cubit = 0.4572 meter` 동적 등록 | 예정 |

#### Track A — CLI 경계 (`tests/test_cli.py`)

| TC ID | 대상 | 시나리오 | 상태 |
|-------|------|----------|------|
| TC-VAL-01 | NFR-03 | 음수 입력 거부 | 예정 |
| TC-VAL-02 | NFR-03 | 잘못된 형식 (`meter`, `:2.5`) | 예정 |
| TC-VAL-03 | NFR-03 | unknown unit 거부 | 예정 |
| TC-VAL-04 | NFR-03 | 공백 trim 처리 | 예정 |
| TC-FMT-01 | FR-09 | `--format table` 3열 출력 | 예정 |
| TC-FMT-02 | FR-09 | `--format json` 출력 | 예정 |
| TC-FMT-03 | FR-09 | `--format csv` 출력 | 예정 |

## 설계 산출물

| 산출물 | 경로 |
|--------|------|
| Git Workflow Rule | `.cursor/rules/git-workflow.mdc` |
| spec Report | `Report/spec-report.md` (본 문서) |
| spec Transcript | `Prompting/spec-transcript.md` |
| 레거시 코드 | `UnitConverter.py` (리팩토링 대상) |
| PRD | `README.md` |

### 데이터 흐름

```
cli.py
  │
  ├─ input_parser        ── FR-01
  ├─ validators          ── NFR-03
  ├─ unit_registration_parser ── FR-08 (선택)
  │
  ├─ config_loader → unit_registry ← units.json  ── FR-07
  ├─ converter (domain)  ── FR-02, FR-04
  └─ output_formatter  ── FR-05, FR-09 (--format)
       ↓
     stdout
```

### LengthUnit Protocol (OCP 핵심)

```python
# domain/length_unit.py
class LengthUnit(Protocol):
    name: str
    def to_meter(self, value: float) -> float: ...
```

## 결과

| 항목 | 상태 |
|------|------|
| 레거시 코드 스멜 식별 | ✅ 18건 |
| PRD 갭 분석 | ✅ 완료 |
| 목표 아키텍처 구조 확정 | ✅ 갱신 완료 |
| 부록 units.json / table 출력 스펙 | ✅ 반영 |
| FR/NFR 매핑 | ✅ FR-01~09, NFR-01~06 |
| Track A/B TC 설계 | ✅ 갱신 |
| Git Workflow Rule | ✅ 등록 |
| Report/Prompting 규칙 | ✅ 등록 |
| 코드 구현 | ❌ red 브랜치에서 TC 작성 예정 |

**다음 단계:** `red` 브랜치에서 Track B(TC-CONV) → Track A(TC-VAL, TC-FMT) RED 테스트 작성

## 회고

### AI 활용

- PRD·레거시 코드 `@` 참조로 갭 분석 자동화
- 목표 아키텍처 슬라이드·부록 Appendix와 spec 설계 **대조 검토**로 구조 단순화
- Git Workflow → Cursor Rule 등록으로 후속 Agent 작업 가이드 확보

### 도움이 된 순간

- 초안(7계층) vs 목표 아키텍처(4계층) 비교로 **과설계 조기 제거**
- 부록 `--format table` 스펙 발견 → TC-FMT-01 구체화

### 한계·결정 사항

| 항목 | 결정 |
|------|------|
| 소수 자릿수 | README(1자리) vs 부록(4자리) → **부록 4자리 우선** |
| units.json | 중첩 vs flat → **부록 flat 우선** |
| 채팅 이름 변경 | Cursor UI 수동 작업 |

### 다음 단계 메모

1. `staging` → `spec` 브랜치 생성, 본 Report 커밋
2. 팀 리뷰 → `staging` merge
3. `red` 브랜치: Track B `test_converter.py` RED 테스트 선행
