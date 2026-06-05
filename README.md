
## Unit Converter (Python)
![unit-converter](./unit-converter.jpg)
### Overview
- 사용자가 입력한 길이(`단위:값`)를 기반으로, 해당 값을 다른 모든 단위로 변환해 출력하는 프로그램.
- 새로운 단위를 추가할 때 기존 코드의 변경이 최소화되도록 설계한다.
- 각 단위 변환 로직은 테스트 코드로 검증한다.

### 가상환경 설정 및 실행
```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate

# 실행
python UnitConverter.py

# 가상환경 비활성화
deactivate
```

### 기본 요구사항
1. 사용자 입력 예시:
   ```
   meter:2.5
   ```
   → 출력:
   ```
   2.5 meter = 8.2 feet
   2.5 meter = 2.7 yard
   ...
   ```

2. 현재 지원 단위:
   - meter
   - feet
   - yard

3. 새로운 단위가 추가될 때도 기존 코드의 변경이 최소화되도록 할 것.

4. 각 단위 간 변환이 정확히 계산되도록 테스트 코드를 작성할 것.

### 비즈니스 로직
- `1 meter = 3.28084 feet`
- `1 meter = 1.09361 yard`
- feet/yard 간의 비율은 meter 기반으로 계산.

### 품질 요구사항
- OCP를 만족하는 설계
- SRP를 만족하는 클래스 구성
- 입력 값 검증 (음수, 잘못된 형식, 없는 단위)

### 추가 요구사항
- **설정 외부화**
   - 변환 비율을 외부 설정 파일(JSON/YAML)에서 로드
- **동적으로 단위와 비율을 등록할 수 있도록 한다**
   - 사용자 입력으로 `1 cubit = 0.4572 meter`를 등록하고 사용 가능
- **출력 포맷 선택 기능** 
   - JSON / CSV / 표 형태 출력


## 생성형AI를 활용한 Activities (6 시간)

1. 문제 코드 및 기본 요구사항 분석 (0.5시간)
   - 기본 코드구조, 로직 이해
2. 기본 요구사항 및 품질 요구사항 구현 (2시간)
   - OCP를 만족하는 인터페이스 구현 
   - SRP를 만족하도록 클래스 구현 
   - 입력값 검증을 위한 구현
3. TC 구현 (0.5시간)
   - 단위변환 기능 검증 및 입력 값 검증 TC 작성
   - → [RED 단계 Checklist](#red-단계-checklist-red-브랜치)
4. 추가 요구사항 구현 (2시간)
   - 3개 요구사항 구현 및 TC 작성 
5. 회고 및 발표 (1시간)
   - 실습 목표와 달성도
   - AI를 어떻게 활용했나? 도움이 된 순간과 한계는?
   - TC를 추가해보면서 개선에 미친 영향, TC 작성 팁
   - 클린코드와 리팩토링에서 느낀 장점과 어려운점

---

## RED 단계 Checklist (`red` 브랜치)

> TC 상세: [PRD.md](PRD.md) §6·§11 · Report: [Report/red-report.md](Report/red-report.md)

### 0. 사전 조건

- [x] `spec`(·Skills / `python-env` rule)이 **staging**에 merge됨
- [x] `git checkout staging && git pull origin staging`
- [x] `git checkout -b red` (또는 기존 `red`를 staging 기준으로 rebase/merge)
- [x] venv 생성·활성화, `pip install pytest`

### 1. Mom Test (요구 검증)

- [x] Mom Test 질답 완료 (제품 설명 X, **과거 행동**만)
- [x] 변환 상황 기록 (예: inch ↔ cm)
- [x] 현재 행동 기록 (예: Google → ChatGPT 재확인)
- [x] Pain 기록 (예: 매번 검색어 입력, 번거로움)
- [x] PRD와 Pain **단위/범위 차이** 메모 (예: inch/cm vs meter/feet/yard)
- [x] Mom Test → FR 연결 메모 (예: Pain → FR-01 입력, FR-02 전 단위 출력)
- [x] 상세는 [Report/red-report.md](Report/red-report.md) § Mom Test

### 2. RED 규칙 (필수 / 금지)

- [x] **production 코드 없음** (`unit_converter/` 등 미구현)
- [x] 전 테스트 `pytest.fail("RED: ...")` 사용
- [x] `skip` / `xfail` **미사용**
- [x] `pytest -v` 실행 → **전부 failed**, passed 0 (16 failed)

### 3. Track B — Domain (`tests/test_converter.py`)

- [x] D-CNV-01 — 1 feet → 0.3048 m (NFR-01)
- [x] D-CNV-02 — 2.5 m → 8.2021 ft (FR-02)
- [x] D-CNV-03 — feet→yard, meter 경유 (FR-02)
- [x] D-CNV-04 — 2.5 m → 2.7340 yd (FR-02)
- [x] D-REG-01 — cubit 0.4572 등록 (EXT-02)
- [x] D-CFG-01 — 깨진 JSON → ConfigError (EXT-01)

### 4. Track A — Boundary (`tests/test_cli.py`)

- [x] U-PAR-01 — `meter:2.5` 파싱 (FR-01)
- [x] U-IN-01 — 빈 입력 (FR-05)
- [x] U-IN-02 — `meter` 콜론 없음 (FR-05)
- [x] U-IN-03 — `meter:-1` 음수 (FR-04)
- [x] U-IN-04 — `cubit:1` unknown unit (FR-03)
- [x] U-IN-05 — `meter / abc` 형식 오류 (FR-05)
- [x] U-OUT-01 — `meter:2.5` 3줄 이상 출력 (FR-02)
- [x] U-FMT-01 — `--format table` (EXT-03)
- [x] U-FMT-02 — `--format json` (EXT-03)
- [x] U-FMT-03 — `--format csv` (EXT-03)

### 5. 문서 · Git

- [x] `PRD.md` §6·§11과 `tests/` TC ID **일치**
- [x] `Report/red-report.md` 작성
- [x] `Prompting/red-transcript.md` Export
- [x] commit 메시지: `[red] ...` + FR/TC ID
- [x] PR 생성: **base `staging`**, head `red` — [PR #3](https://github.com/MINJU-KIMmm/UnitConverter_08/pull/3)
- [x] 팀 리뷰 — **Approve** ([PR #3](https://github.com/MINJU-KIMmm/UnitConverter_08/pull/3), 피드백 `PRD.md` §7.3·§12 반영)
- [ ] staging merge (리뷰어/팀 수행)

### 6. 검증 명령

```bash
venv\Scripts\activate    # Windows
pytest -v                # 기대: N failed, 0 passed
```
