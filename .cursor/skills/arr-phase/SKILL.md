---
name: arr-phase
description: >-
  Guides ARRR phase workflow for UnitConverter_08 — branch check, PRD read,
  phase scope, Report/Transcript. Use when starting or finishing spec, red,
  green, refactoring, or new_features work, or when the user mentions ARRR,
  phase, or branch strategy.
---

# ARRR Phase Workflow

UnitConverter_08 실습은 **spec → red → green → refactoring → new_features** 순서로 진행한다.

## Phase Start (작업 시작)

1. `git branch --show-current` — 현재 브랜치가 단계와 일치하는지 확인
2. `@PRD.md` §6 추적표 읽기 — 이번 단계 대상 FR/NFR/EXT·TC ID 확인
3. `.cursor/rules/git-workflow.mdc` — staging 하위 브랜치에서만 작업
4. 단계별 **허용 범위**:

| 브랜치 | 허용 | 금지 |
|--------|------|------|
| spec | PRD, Report, 설계, rules/skills | production 코드, tests |
| red | RED tests (`pytest.fail`) | production 코드 구현 |
| green | 최소 구현 (테스트 통과) | 범위 밖 FR |
| refactoring | OCP/SRP 리팩 (테스트 유지) | PRD 외 기능 추가 |
| new_features | EXT-01~03 | P0 요구 변경 |

5. `main` / `staging`에 직접 commit하지 않는다

## Phase End (작업 종료)

1. `Report/{phase}-report.md` 작성·갱신 (report-transcript skill 참고)
2. Transcript → `Prompting/{phase}-transcript.md` 저장 안내
3. commit 메시지: `[spec|red|green|refactoring|new_features] ...`
4. PR base = **staging**, merge/push는 사용자 요청 시만

## Branch Creation

```bash
git checkout staging
git pull origin staging
git checkout -b red   # spec merge 후 다음 단계
```

## Cursor Agent (채팅) 운영

- 단계별 **별도 채팅** (예: `1. 분석`, `2. RED`)
- spec/red: `@PRD.md` + 해당 `@Report/{phase}-report.md`
- Agents 설정은 Git에 없음 — Transcript로 대화 기록 보존
