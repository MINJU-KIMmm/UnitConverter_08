# red Report — RED 테스트 (Dual-Track)

> 브랜치: `red` | 작성일: 2026-06-05 | 프로젝트: UnitConverter_08

## 목표

- PRD(`PRD.md`) §6·§11 기준 **Dual-Track RED** 스켈레톤 TC 작성
- 구현 코드 없이 `pytest.fail("RED: ...")` 로 전 TC 실패 확인
- `skip` / `xfail` 금지, Track B → Track A 순서로 커밋

## 수행 내용

### Mom Test (요구 검증)

| 항목 | 기록 |
|------|------|
| 변환 상황 | inch ↔ cm |
| 현재 행동 | Google 검색 → ChatGPT로 재확인 |
| Pain | 매번 검색어 입력, 번거로움 |
| PRD vs Pain (단위/범위) | *(메모 예정)* inch/cm vs meter/feet/yard |
| Mom Test → FR | *(메모 예정)* Pain → FR-01 입력, FR-02 전 단위 출력 |

### 1. Track B — Domain (`tests/test_converter.py`)

| TC ID | PRD | 시나리오 |
|-------|-----|----------|
| D-CNV-01 | NFR-01 | `to_meter` — 1 feet → 0.3048 m (±ε) |
| D-CNV-02 | FR-02 | 2.5 m → 8.2021 ft |
| D-CNV-03 | FR-02 | feet→yard, meter 경유 일치 |
| D-CNV-04 | FR-02 | 2.5 m → 2.7340 yd |
| D-REG-01 | EXT-02 | cubit 0.4572 등록 |
| D-CFG-01 | EXT-01 | 깨진 JSON → ConfigError |

### 2. Track A — Boundary (`tests/test_cli.py`)

| TC ID | PRD | 시나리오 |
|-------|-----|----------|
| U-PAR-01 | FR-01 | `meter:2.5` 파싱 |
| U-IN-01 | FR-05 | 빈 입력 |
| U-IN-02 | FR-05 | 콜론 없음 (`meter`) |
| U-IN-03 | FR-04 | `meter:-1` |
| U-IN-04 | FR-03 | `cubit:1` unknown unit |
| U-IN-05 | FR-05 | `meter / abc` |
| U-OUT-01 | FR-02 | 3줄 이상 출력 |
| U-FMT-01~03 | EXT-03 | table / json / csv |

### 3. PRD·환경

- `PRD.md` §6 추적표·§11 RED TC 목록 갱신 (16건 ✅ RED)
- `.gitignore` — `venv/`, `.pytest_cache/` 제외

## PRD 매핑

| ID | TC ID | 파일 |
|----|-------|------|
| FR-01 | U-PAR-01 | test_cli.py |
| FR-02 | U-OUT-01, D-CNV-02, D-CNV-04 | test_cli.py, test_converter.py |
| FR-03 | U-IN-04 | test_cli.py |
| FR-04 | U-IN-03 | test_cli.py |
| FR-05 | U-IN-01, U-IN-02, U-IN-05 | test_cli.py |
| NFR-01 | D-CNV-01~03, D-REG-01 | test_converter.py |
| EXT-01 | D-CFG-01 | test_converter.py |
| EXT-02 | D-REG-01 | test_converter.py |
| EXT-03 | U-FMT-01~03 | test_cli.py |
| NFR-02 | — | 구조 리뷰 (자동 TC 없음) |

## TC 목록 · 결과

```text
pytest -q  →  16 failed, 0 passed, 0 skipped
```

| 규칙 | 결과 |
|------|------|
| 구현 코드 없음 | ✅ `unit_converter/` 미존재 |
| `pytest.fail("RED: ...")` | ✅ 16/16 |
| skip / xfail 금지 | ✅ |
| venv에서 실행 | ✅ |

## 결과

| 항목 | 상태 |
|------|------|
| Track B RED (6건) | ✅ |
| Track A RED (10건) | ✅ |
| PRD §11 반영 | ✅ |
| green 구현 | ❌ 다음 단계 |

**다음 단계:** 팀 리뷰 → `red` → `staging` merge → `green` 브랜치

## 회고

- Dual-Track 표·PRD §11 대조로 누락 TC(U-IN-04, U-FMT-*, U-PAR-01, D-CNV-04) 보완
- RED 단계는 스켈레톤만 유지해 green에서 본문 구현 예정
