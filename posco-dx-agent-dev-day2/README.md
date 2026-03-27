# Day 2 실습 — Agent 제어 흐름 설계 & 상태 관리

## 수업 시간표 (08:00~17:00)

| 시간 | 내용 | 실습 |
|------|------|------|
| 08:00~08:20 | Langfuse 셀프 호스팅 | `langfuse-self-host/` Docker Compose |
| 08:20~09:30 | 프레임워크 기초 (I DO) | `00_basics/` 00~04 노트북 |
| 09:30~09:50 | Deep Agents 체험 (WE DO) | `00_basics/05_deep_agents_basics.ipynb` |
| 09:50~10:00 | 프레임워크 비교 (YOU DO) | `00_basics/06_comparison.ipynb` |
| 10:00~10:10 | 휴식 | |
| 10:10~11:00 | Agent 4요소 이론 | 가이드 day2-session1 |
| 11:00~12:00 | LangGraph 제어 흐름 이론 | 가이드 day2-session2 |
| 12:00~13:00 | 점심 | |
| 13:00~14:30 | LangGraph 워크플로 실습 | `01_langgraph_workflows/` |
| 14:30~14:40 | 휴식 | |
| 14:40~15:40 | Tool 통제 & 미들웨어 | `02_tool_middleware/` |
| 15:40~15:50 | 휴식 | |
| 15:50~17:00 | 리팩토링 & Observability | 가이드 day2-session4 코드 예제 |

## 실습 디렉토리

```
labs/day2/
├── 00_basics/                    # 프레임워크 기초 (~3h)
│   ├── 00_setup.ipynb               환경 설정
│   ├── 01_llm_basics.ipynb          LLM 호출 기초
│   ├── 02_langchain_basics.ipynb    LangChain 에이전트
│   ├── 03_langchain_memory.ipynb    메모리 & 스트리밍
│   ├── 04_langgraph_basics.ipynb    LangGraph StateGraph
│   ├── 05_deep_agents_basics.ipynb  Deep Agents 하네스
│   ├── 06_comparison.ipynb          3 프레임워크 비교
│   └── bonus_mini_project.ipynb     미니 프로젝트
├── 01_langgraph_workflows/       # LangGraph 워크플로 (~1.5h)
│   ├── 01_graph_api.ipynb           Graph API 기초
│   └── 02_workflows.ipynb           5가지 워크플로 패턴
├── 02_tool_middleware/            # Tool 검증 & 미들웨어 (~1h)
│   ├── 01_tools.ipynb               Tool 스키마 & Structured Output
│   └── 02_middleware.ipynb           미들웨어 패턴
└── langfuse-self-host/           # Langfuse 로컬 서버
```

## 환경 설정

```bash
cd labs/day2
uv sync          # 의존성 설치
cp .env.example .env  # API 키 설정
```

## 실행 순서

1. `00_basics/00_setup.ipynb` — 환경 확인 및 Langfuse 연동
2. `00_basics/01~06` — 프레임워크 기초 순서대로 실행
3. `01_langgraph_workflows/01_graph_api.ipynb` → `02_workflows.ipynb`
4. `02_tool_middleware/01_tools.ipynb` → `02_middleware.ipynb`
