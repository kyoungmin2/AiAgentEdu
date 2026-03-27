# Day 4 실습 — Agent 평가 · 성능 튜닝 · 운영 모니터링

## 환경 설정

### 1. 패키지 설치

```bash
uv sync
```

### 2. `.env` 파일 준비

이전 day3 폴더에서 복사하거나, 직접 작성합니다.

```bash
cp ../day3-폴더-이름/.env .env
```

`.env` 파일에 다음 키가 필요합니다:

```
OPENAI_API_KEY=sk-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_BASE_URL=http://localhost:3000
```

---

## 각 노트북 간단 설명

| 노트북 | 주제 | 설명 |
|--------|------|------|
| `01_agent_evaluation.ipynb` | Agent 품질 평가 | Golden Test Set 구축, 정량 지표(Accuracy·Faithfulness·Robustness), LM-as-a-Judge 평가 |
| `02a_prompt_versioning.ipynb` | Prompt 버전 관리 | SemVer 기반 프롬프트 버전 관리, A/B 테스트로 Prompt Drift 방지 |
| `02b_retrieval_drift.ipynb` | Retrieval Drift 감지 | 문서 업데이트에 따른 검색 결과 변화 감지 및 대응 전략 |
| `02c_tool_call_tuning.ipynb` | Tool 호출 정확도 개선 | Tool description 품질에 따른 호출 정확도 비교 (나쁜 설명 vs 좋은 설명) |
| `03_agent_ops_monitoring.ipynb` | 운영 모니터링 | Trace 수집, 장애 분류, Guardrail 설정 (Langfuse 활용) |
| `bonus1_sql_agent.ipynb` | SQL 에이전트 심화 | LangChain + LangGraph 기반 SQL 에이전트, Human-in-the-Loop 패턴 |
| `bonus2_service_architecture.ipynb` | 서비스 아키텍처 | 환경 분리, 모델 라우팅, Semantic Cache, Multi-Agent, 비용 최적화 |

### 실습 순서

1. **`01`** → Agent 평가의 기본 프레임워크 이해
2. **`02a` → `02b` → `02c`** → 성능 튜닝 3종 세트 (Prompt · Retrieval · Tool)
3. **`03`** → 운영 환경 모니터링 구축
4. **`bonus1`** → SQL 에이전트로 심화 실습 (01번에서 평가 대상으로 활용)
5. **`bonus2`** → 프로덕션 배포를 위한 아키텍처 패턴