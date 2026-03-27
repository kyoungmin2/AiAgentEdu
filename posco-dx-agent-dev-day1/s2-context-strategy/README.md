# Lab: Context 전략 비교 실습

> **소요 시간**: 120분 (2시간)
> **형태**: Python 코드 실습
> **사전 준비**: OpenAI API 키, LangSmith API 키
> **기술 스택**: Python 3.12+, PydanticAI, LangSmith, Pydantic

## 실습 개요

같은 태스크에 다양한 **컨텍스트 전략**(System Prompt 변형 / 컨텍스트 양 / 구조화 수준)을 적용하고,
토큰 수 / 비용 / 응답 시간 / 품질을 비교한다. PydanticAI Agent와 LangSmith 트레이싱을 함께 익힌다.

---

## 사전 준비

### 1. 패키지 설치

```bash
cd day1
uv sync
```

### 2. 환경변수 설정 (.env 파일)

`day1/` 디렉토리에 `.env` 파일을 생성한다.

```bash
OPENAI_API_KEY=sk-...
LANGSMITH_API_KEY=lsv2_...
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=day1-context-strategy
```

### 3. Jupyter Lab 실행

`day1/` 디렉토리에서 Jupyter Lab을 실행한다.

```bash
uv run jupyter lab
```

---

## 수업 흐름

| 단계 | 시간 | 내용 | 파일 |
|------|------|------|------|
| 강의 | 25분 | Context 전략 이론 (슬라이드) | - |
| 시연 | 20분 | 컨텍스트 전략별 응답 비교 | `src/demo_context_strategies.ipynb` |
| 실습 | 25분 | LangSmith 셋업 + Structured Output | `src/setup_langsmith.ipynb` |
| 과제 | 35분 | 자기 도메인에 전략 적용 | `src/context_lab.ipynb` |
| 정리 | 15분 | 비교 결과 공유 + Q&A | - |

---

## 시연 -- 20분

> 강사가 `src/demo_context_strategies.ipynb` 노트북을 실행하며 시연합니다.

`src/demo_context_strategies.ipynb` 노트북을 열어 셀을 순서대로 실행하세요.

### 관찰 포인트

- System Prompt(instructions) 유무에 따라 응답 형식이 얼마나 달라지는가?
- 컨텍스트를 풍부하게 제공하면 토큰 대비 품질이 어떻게 변하는가?
- Structured Output(output_type)을 사용하면 자유 응답 대비 어떤 장점이 있는가?

---

## 실습 -- 25분

> `src/setup_langsmith.ipynb` 노트북을 함께 실행하며 LangSmith를 셋업하고 Structured Output을 실습합니다.

### 목표

LangSmith 트레이싱 셋업 + PydanticAI Agent의 Structured Output 패턴을 익힌다.

### 진행 방법

`src/setup_langsmith.ipynb` 노트북을 열어 셀을 순서대로 실행하세요.
노트북의 마크다운 셀에 각 단계의 상세 설명이 포함되어 있습니다.

### 체크포인트

- [ ] LangSmith 대시보드에서 트레이스가 보이는가?
- [ ] PydanticAI Agent 호출이 트레이스로 기록되는가?
- [ ] Structured Output 응답이 Pydantic 모델로 파싱되는가?
- [ ] `result.output.sentiment.value` 등으로 필드에 접근할 수 있는가?

---

## 과제 -- 35분

> `src/context_lab.ipynb` 노트북의 TODO를 채워 자신의 도메인에 컨텍스트 전략을 적용합니다.

### 과제

자신의 도메인 태스크(예: 기술 티켓 분류, 이메일 의도 분석 등)에
3가지 컨텍스트 전략을 적용하고 결과를 비교하라.

### 요구사항

1. **스키마 정의** (TODO 1): 자기 도메인에 맞는 Pydantic 모델 작성
   - Enum으로 카테고리 제한
   - Field(description=...)으로 LLM 힌트 제공
2. **테스트 데이터** (TODO 2): 5개 이상의 테스트 케이스 작성
3. **전략 구현** (TODO 3-5):
   - 전략 A: instructions 없이 호출 (`Agent(MODEL, output_type=...)`)
   - 전략 B: 역할 + 제약 instructions (`Agent(MODEL, instructions=..., output_type=...)`)
   - 전략 C: Few-shot 예시 포함 instructions
4. **비교 분석**: 각 전략의 정확도, 토큰, 비용 비교

### 진행 방법

`src/context_lab.ipynb` 노트북을 열어 TODO 셀을 채워가며 순서대로 실행하세요.

### 정답 참고

막히면 `solution/context_strategies.ipynb`를 참고하세요.
단, 정답을 보기 전에 최소 15분은 직접 시도해보세요.

---

## 심화 과제 (선택)

시간이 남는 분을 위한 추가 과제:

1. **전략 D 추가**: CoT(Chain-of-Thought) 전략 -- instructions에 "단계별로 추론하라" 지시 추가
2. **모델 비교**: 같은 전략을 `openai:gpt-5.4`와 `openai:gpt-5.4-mini` 모두에 적용하여 비용/정확도 트레이드오프 분석
3. **컨텍스트 양 실험**: instructions의 길이를 단계적으로 늘려가며 정확도 변화 측정

---

## 체크리스트

실습을 마치기 전 확인하세요:

- [ ] `demo_context_strategies.ipynb` 실행 결과를 관찰했는가?
- [ ] LangSmith에서 트레이스를 확인했는가?
- [ ] PydanticAI Agent의 `instructions`, `output_type`, `await agent.run()` 패턴을 이해했는가?
- [ ] `context_lab.ipynb`에서 3가지 전략을 모두 구현했는가?
- [ ] 전략별 정확도와 비용 비교가 출력되는가?
- [ ] 어떤 상황에서 어떤 전략이 적합한지 설명할 수 있는가?
