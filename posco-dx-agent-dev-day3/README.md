# Day 3 실습 — MCP · Agentic RAG · Deep Agents Skills

## 환경 설정

```bash
# 의존성 설치
uv sync
```

`.env` 파일에 아래 키를 설정하세요:

```env
OPENAI_API_KEY=sk-...

# (선택) Langfuse 트레이싱
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_HOST=https://lf.ddok.ai

# (선택) LangSmith 트레이싱
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=lsv2_...
LANGSMITH_PROJECT=day3-lab
```

## 실습 순서

아래 순서대로 진행합니다. 각 노트북은 이전 개념을 기반으로 확장됩니다.

### 1. `00-mcp/` — MCP (Model Context Protocol)

| 파일 | 설명 |
|------|------|
| `math_server.py` | Stdio 전송 MCP 서버 (add, multiply) |
| `get_weather.py` | Streamable HTTP 전송 MCP 서버 (get_weather) |
| `mcp.ipynb` | `MultiServerMCPClient`로 다중 MCP 서버 연결 |

```bash
# weather 서버는 별도 터미널에서 미리 실행
python 00-mcp/get_weather.py
```

**학습 포인트**: MCP 아키텍처(서버/클라이언트/호스트), Stdio vs HTTP 전송 방식, `langchain-mcp-adapters` 활용

### 2. `01-rag/` — Agentic RAG

| 파일 | 설명 |
|------|------|
| `01-langgraph-agentic-rag.ipynb` | 3가지 RAG 방식 비교 구현 |

**학습 포인트**:
- **RAG Agent** — `create_agent` + `@tool`로 자율 검색
- **RAG Chain** — `@dynamic_prompt` 미들웨어로 단일 패스 RAG
- **LangGraph 커스텀 RAG** — `StateGraph`로 관련성 평가 + 쿼리 리라이트 + 조건부 라우팅

### 3. `02-skills/` — Deep Agents 백엔드 & 스킬

| 파일 | 설명 |
|------|------|
| `00-backends.ipynb` | 5가지 스토리지 백엔드 비교 (State, Filesystem, Store, Composite, LocalShell) |
| `01-deepagents-skills.ipynb` | 장기 메모리, AGENTS.md 컨텍스트 주입, SKILL.md 점진적 공개 |
| `02-github-copilot-skill-활용.md` | GitHub Copilot Skill 활용 실습 |

**학습 포인트**: 에페메럴 vs 영속 저장, 크로스 스레드 메모리 공유, Memory vs Skills 차이

### 4. `03-hybrid/` — 하이브리드 에이전트 (통합 실습)

| 파일 | 설명 |
|------|------|
| `01-hybrid-agent.ipynb` | RAG + MCP + Skills를 `create_deep_agent` 하나로 통합 |

**학습 포인트**: 사내 규정 RAG 검색, MCP 수학 도구 호출, SKILL.md 보고서 양식 적용, Langfuse 트레이스 검증

## 핵심 개념 요약

| 개념 | 도구/API | 설명 |
|------|---------|------|
| MCP | `MultiServerMCPClient` | 외부 도구를 표준 프로토콜로 연결 |
| RAG | `InMemoryVectorStore` + `@tool` | 벡터 검색으로 LLM에 외부 지식 제공 |
| Backend | `StateBackend`, `CompositeBackend` 등 | 에이전트 파일 시스템 추상화 |
| Skills | `SKILL.md` + `skills=` 파라미터 | 도메인 전문 지식 점진적 공개 |
| Memory | `AGENTS.md` + `memory=` 파라미터 | 항상 로드되는 규칙/컨벤션 주입 |
