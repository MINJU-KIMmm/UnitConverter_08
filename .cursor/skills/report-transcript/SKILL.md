---
name: report-transcript
description: >-
  Writes ARRR phase Report and Prompting Transcript for UnitConverter_08.
  Use when completing a phase, when the user asks for Report or Export Transcript,
  or when finishing spec, red, green, refactoring, or new_features work.
---

# Report & Transcript

## File Pairs

| Phase | Report | Transcript |
|-------|--------|------------|
| spec | `Report/spec-report.md` | `Prompting/spec-transcript.md` |
| red | `Report/red-report.md` | `Prompting/red-transcript.md` |
| green | `Report/green-report.md` | `Prompting/green-transcript.md` |
| refactoring | `Report/refactoring-report.md` | `Prompting/refactoring-transcript.md` |
| new_features | `Report/new_features-report.md` | `Prompting/new_features-transcript.md` |

**Report** = 공식 산출물 (우선 참조). **Transcript** = Cursor 대화 원본.

## Report 필수 섹션

1. **목표** — 단계별 달성 목표
2. **수행 내용** — 실제 작업 요약
3. **PRD 매핑** — FR/NFR/EXT · TC ID (PRD.md §6)
4. **TC 목록** — 통과/실패/예정 (red 이후)
5. **결과** — 산출물·테스트 상태
6. **회고** — AI 활용·개선점

## Transcript 작성

1. Cursor 채팅 **⋯ → Export Transcript** (또는 대화 요약)
2. `Prompting/{phase}-transcript.md`에 저장
3. 헤더: Export Date, Phase, 짝 Report 경로

## Phase 완료 시 Agent 행동

1. Report 초안 작성·갱신 제안
2. Transcript Export 안내
3. commit: `[{phase}] Report 및 (해당 시) Transcript 추가`
4. PR → staging (사용자 요청 시)

## spec Report 참고

`Report/spec-report.md` — 분석·설계·목표 아키텍처·TC 설계 예시.
