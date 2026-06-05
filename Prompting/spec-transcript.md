# spec Transcript — 1. 분석

> Export Date: 2026-06-05 (갱신) | Project: UnitConverter_08 | Stage: spec
> 짝 Report: `Report/spec-report.md`

---

## User

@README.md @UnitConverter.py 레거시 코드 스멜과 PRD 갭을 목록으로 정리해줘

---

## Assistant

README와 `UnitConverter.py`를 읽고 PRD 대비 구현 상태를 비교. 레거시 코드 스멜 18건, PRD 갭( OCP/SRP/TC/추가 FR 전면 미구현) 정리. Activities 1단계만 완료.

---

## User

채팅 이름을 1. 분석으로 바꿔줘

---

## Assistant

Cursor 채팅 이름은 Agent가 직접 변경 불가. Chat 패널 → Rename → `1. 분석` 수동 입력 안내.

---

## User

OCP/SRP 를 만족하는 Python 패키지 구조를 제안하고, PRD의 FR/NFR을 매핑해줘

---

## Assistant

초안 패키지 구조 제안 (7계층: domain, validation, infrastructure, output, application, cli, tests/unit).

- FR-01~09, NFR-01~06 모듈 매핑
- UnitRegistry, OutputFormatter Strategy, config/units.json (중첩 JSON) 설계

---

## User

[Git Workflow 이미지] git 브랜치를 이렇게 만들 예정인데 rules 로 등록해서 사용하고 싶어

---

## Assistant

`.cursor/rules/git-workflow.mdc` 등록 (`alwaysApply: true`).

브랜치: `main → staging → spec|red|green|refactoring|new_features`
팀 리뷰 3원칙: 개별 merge 금지, PRD→TC→Code 추적성, TC 통과 커밋 공유.

---

## User

각 작업 Report는 /Report, Export Transcript는 /Prompting 폴더에 넣고싶어

---

## Assistant

git-workflow rule에 Report/Prompting 규칙 추가. `{단계}-report.md` ↔ `{단계}-transcript.md` 짝 맞춤.

---

## User

Report 작성해주고 Export Transcript해줘

---

## Assistant

`Report/spec-report.md`, `Prompting/spec-transcript.md` 작성 완료.

---

## User

그래서 내가 만들 프로젝트 주제가 뭔데?

---

## Assistant

**Unit Converter (Python)** — 길이 단위 변환 프로그램.

- 입력: `meter:2.5` (단위:값)
- 출력: 모든 길이 단위로 변환 (meter, feet, yard)
- PRD 방향: OCP/SRP, TDD, 설정 외부화, 동적 단위 등록, JSON/CSV/표 출력

---

## User

지금까지 작업한 내용 깃허브에 올린다면 어떻게 올릴래?

---

## Assistant

git-workflow rule 기준 권장 흐름:

1. `staging` 브랜치 생성 (main에서)
2. `spec` 브랜치에서 Report·Prompting·rule 커밋
3. `git push -u origin spec`
4. `gh pr create --base staging --head spec` (팀 리뷰)
5. merge 후 `staging` → (전체 완료 시) `main`

`main`에 바로 push하지 않음.

---

## User

[Appendix 이미지] 이런 출력에 대한 설계가 이미 있어? 아님 추가해야돼?

---

## Assistant

**추가·보완 필요.**

| 항목 | spec 초안 | 부록 Appendix | 코드 |
|------|-----------|---------------|------|
| units.json flat | 중첩 JSON | `{ meter, feet, yard }` flat | ❌ |
| `--format table` | 미명시 | unit/input/result 3열 | ❌ |
| 소수 자릿수 | 1자리 (README) | 4자리 (8.2021) | ❌ |

개념(Formatter, config_loader)만 spec에 있고, 부록 구체 스펙은 미반영.

---

## User

[Target Architecture 이미지] 참고로 목표 아키텍처 예시는 다음과 같아 수정할 부분이 있어?

---

## Assistant

**수정 필요.** spec 초안(7계층)을 목표 아키텍처에 맞춰 단순화:

| 변경 | 내용 |
|------|------|
| 통합 | `validation/` + `output/` + `application/` → **`app/`** |
| 진입점 | `cli/main.py` → **`cli.py`** |
| OCP | **`domain/length_unit.py`** Protocol 추가 |
| Formatter | **`app/output_formatter.py`** 1파일 (json\|csv\|table) |
| 테스트 | Track B `test_converter.py`, Track A `test_cli.py` |
| PRD 추가 | `validators.py`, `unit_registration_parser.py` 유지 |

---

## User

위 구조로 갱신해주고 Transcript도 같이 업로드해줘

---

## Assistant

`Report/spec-report.md` 목표 아키텍처·부록 스펙 반영 갱신.
`Prompting/spec-transcript.md` 전체 대화 Transcript 갱신.

**확정 구조:**
```
unit_converter/
├── domain/       length_unit.py, unit_registry.py, converter.py
├── infrastructure/ config_loader.py
├── app/          input_parser, validators, unit_registration_parser, output_formatter
├── cli.py
tests/            test_converter.py (Track B), test_cli.py (Track A)
config/units.json (flat)
```

---

*End of Transcript*
