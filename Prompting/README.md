# Prompting

Cursor **Export Transcript**로 내보낸 AI 대화 기록을 저장하는 폴더입니다.

## 저장 방법

1. 해당 단계 Cursor 채팅에서 **⋯** → **Export Transcript**
2. `{단계}-transcript.md` 파일에 붙여넣기 (예: `spec-transcript.md`)
3. 같은 단계의 `Report/{단계}-report.md`와 짝을 맞춘다

## 파일 목록

| 단계 | Transcript | Report (짝) |
|------|------------|---------------|
| spec | `spec-transcript.md` | `../Report/spec-report.md` |
| red | `red-transcript.md` | `../Report/red-report.md` |
| green | `green-transcript.md` | `../Report/green-report.md` |
| refactoring | `refactoring-transcript.md` | `../Report/refactoring-report.md` |
| new_features | `new_features-transcript.md` | `../Report/new_features-report.md` |

## 참고

- Transcript는 **대화 원본**, Report는 **정리된 공식 산출물**입니다.
- Agent는 Report를 우선 참조하고, Transcript로 맥락을 보완합니다.
