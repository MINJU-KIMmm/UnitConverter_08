---
name: prd-traceability
description: >-
  Enforces PRD to TC to Code traceability for UnitConverter_08 — FR/NFR/EXT IDs,
  TC IDs, commit and PR templates. Use when writing tests, implementing features,
  committing, or creating pull requests.
---

# PRD → TC → Code Traceability

SSOT: **`PRD.md` §6** (추적표). ID 체계는 슬라이드 기준을 따른다.

## Requirement IDs

| Prefix | 예 | 우선순위 |
|--------|-----|----------|
| FR-01~05 | 입력·출력·검증 | P0 |
| NFR-01~02 | OCP, SRP | P0 |
| EXT-01~03 | config, 동적등록, format | P1 |

## Test IDs

| Track | 파일 | ID 패턴 |
|-------|------|---------|
| B (Domain) | `tests/test_converter.py` | D-CNV-*, D-REG-*, D-CFG-* |
| A (Boundary) | `tests/test_cli.py` | U-IN-*, U-OUT-*, U-FMT-* |

새 TC 추가 시 **PRD.md §6 표에 TC ID·파일 반영**을 제안한다.

## Commit Message

```
[red] FR-03: unknown unit TC 추가 (U-IN-04)

PRD: FR-03
TC: U-IN-04
```

접두: `[spec|red|green|refactoring|new_features]`

## Pull Request Template

```markdown
## Summary
- (변경 요약)

## Traceability
| ID | TC | Code |
|----|-----|------|
| FR-03 | U-IN-04 | tests/test_cli.py |

## Test plan
- [ ] pytest -v (venv)
- [ ] PRD §6 해당 행 충족
```

## Before Merge Checklist

- [ ] 변경이 PRD 범위 내 (PRD.md, README.md)
- [ ] FR/NFR/EXT ID가 commit 또는 PR 본문에 명시
- [ ] TC ID와 테스트 파일명 일치
- [ ] PR base = **staging** (main 직접 merge 금지)
