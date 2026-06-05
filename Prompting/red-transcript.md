# red Transcript — 2. RED

> Export Date: 2026-06-05 | Project: UnitConverter_08 | Stage: red
> 짝 Report: `Report/red-report.md`
> 채팅: RED 단계 (Dual-Track TC · venv · GitHub 반영)

---

## User

[Dual-Track RED 설계표 이미지] pytest RED 스켈레톤만 작성해줘. 구현은 금지. Dual-Track 표 기준, pytest.fail 사용

코드 실행 및 테스트 실행은 가상환경에서 하고 싶은데 rules로 정의해야할까, skills로 정의해야할까?
@README.md (9-24)

---

## Assistant

- `tests/test_cli.py` — Track A: U-IN-01~03, U-OUT-01 (4건)
- `tests/test_converter.py` — Track B: D-CNV-01~03, D-REG-01, D-CFG-01 (5건)
- 전 TC `pytest.fail("RED: ...")`, skip/xfail 없음
- **Rule 권장** — venv 사용은 프로젝트 전역 규약 → `.cursor/rules/python-env.mdc` 예시 제안 (Skill은 복잡 절차용)

---

## User

Rule 파일 만들어줘

---

## Assistant

`.cursor/rules/python-env.mdc` 생성 (`alwaysApply: true` — venv 활성화 후 python/pytest/pip).

---

## User

테스트 수행해주고 RED 규칙에 맞게 다 실패하는지 확인해줘

---

## Assistant

`pytest -v` → **9 failed, 0 passed**. RED 규칙 체크: 구현 없음, pytest.fail 9/9, skip/xfail 없음. (당시 venv pip SSL 이슈로 시스템 pytest 사용됨)

---

## User

venv 전용 환경이 필요하면 SSL 설정을 맞춘 뒤 venv\Scripts\activate → pip install pytest를 다시 실행하면 됩니다. — 이거 해줘

---

## Assistant

- venv에 `pytest` 설치 (`--trusted-host` 우회)
- `%APPDATA%\pip\pip.ini`에 `trusted-host` 추가 (기존 proxy·cert 유지)
- venv `site-packages`에서 pytest 로드 확인

---

## User

그래 (pip.ini trusted-host 설정)

---

## Assistant

`pip.ini` 갱신 완료. venv에서 `--trusted-host` 없이 `pip install` 동작 확인.

---

## User

PRD.md 참고해서 tc 빠진 거 있으면 추가해줄래?

---

## Assistant

PRD §6·§11 대비 누락 TC 추가:

**Track A (+6):** U-PAR-01, U-IN-04, U-IN-05, U-FMT-01~03  
**Track B (+1):** D-CNV-04 (yard 2.7340)  
D-CNV-02 기대값 `8.2021` (부록 4자리)  
→ **16 failed** 확인

---

## User

PRD.md §11 미작성 TC 목록도 갱신해줘 → 그래

---

## Assistant

`PRD.md` §6 추적표 TC ID 반영, §11 → 「RED TC 목록」16건 ✅ RED 정리.

---

## User

RED 단계에 대해 github에 반영하고 싶은데 어떤 순서로 할거야? (Ask mode)

---

## Assistant

순서 안내: spec→staging merge 선행 → `staging`에서 `red` 분기 → pytest 16 failed → Track B/A 커밋 → PR(base=staging) → 팀 리뷰 → staging merge.

---

## User

그렇게 해줘

---

## Assistant

- `staging` pull → `red` 브랜치 생성
- 커밋 2건: Track B (`test_converter.py`), Track A (`test_cli.py`, `PRD.md`, `red-report.md`, `.gitignore`)
- `origin/red` push
- `gh` 미설치 → PR 수동 생성 URL 안내

---

## User

Prompting/red-transcript.md는 Cursor에서 Export 후 저장하면 됩니다. — 이것도 만들어줘

---

## Assistant

본 Transcript 작성 (`Prompting/red-transcript.md`).

---

## 산출물 요약

| 산출물 | 경로 |
|--------|------|
| Track B tests | `tests/test_converter.py` (6 TC) |
| Track A tests | `tests/test_cli.py` (10 TC) |
| PRD 갱신 | `PRD.md` §6, §11 |
| Report | `Report/red-report.md` |
| Transcript | `Prompting/red-transcript.md` (본 문서) |
| Rule | `.cursor/rules/python-env.mdc` (spec/staging 반영) |
| Git | `red` → PR → `staging` (2 commits pushed) |

**pytest (venv):** `16 failed in 0.08s` — RED 단계 완료

**다음:** PR merge 후 `green` 브랜치에서 최소 구현

---

*End of Transcript*
