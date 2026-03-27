# LangGraph 워크플로 실습

## 개요

LangGraph의 Graph API를 사용하여 워크플로를 설계하고 구현한다.

## 노트북

| 순서 | 파일 | 내용 | 시간 |
|------|------|------|------|
| 1 | `01_graph_api.ipynb` | StateGraph, Node-Edge-State, 조건 분기, 리듀서 | 30분 |
| 2 | `02_workflows.ipynb` | 5가지 워크플로 패턴 (Chaining, Parallelization, Routing, Orchestrator-Worker, Evaluator-Optimizer) | 40분 |

## 사전 요구사항

- `labs/day2/00_basics/` 노트북 완료
- `.env` 파일에 `OPENAI_API_KEY` 설정 완료

## 학습 목표

1. StateGraph로 Node-Edge-State 구조를 구현할 수 있다
2. `add_conditional_edges`로 조건 분기를 설계할 수 있다
3. `Annotated`와 `operator.add`로 State 리듀서를 설정할 수 있다
4. 5가지 워크플로 패턴을 구분하고 적합한 패턴을 선택할 수 있다
