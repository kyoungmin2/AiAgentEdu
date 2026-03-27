# Tool 검증 & 미들웨어 실습

## 개요

Pydantic 스키마로 Tool을 정의하고, 미들웨어로 Tool 호출을 통제한다.

## 노트북

| 순서 | 파일 | 내용 | 시간 |
|------|------|------|------|
| 1 | `01_tools.ipynb` | Pydantic args_schema, Structured Output, ToolRuntime | 25분 |
| 2 | `02_middleware.ipynb` | @wrap_tool_call, ToolCallLimit, ModelCallLimit, 커스텀 미들웨어 | 25분 |

## 사전 요구사항

- `labs/day2/00_basics/` 노트북 완료
- `labs/day2/01_langgraph_workflows/` 노트북 완료 (권장)

## 학습 목표

1. `@tool(args_schema=...)` 으로 Tool 입력을 스키마로 강제할 수 있다
2. `with_structured_output()`으로 LLM 응답 형식을 제어할 수 있다
3. 미들웨어로 Tool 호출 횟수를 제한하고 무한 루프를 방지할 수 있다
4. 커스텀 미들웨어를 작성하여 감사 로깅을 구현할 수 있다
