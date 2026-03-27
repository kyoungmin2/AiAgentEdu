# LangChain 에이전트와 Deep Agents의 차이점

현재 디렉토리의 노트북(`02_langchain_basics.ipynb`, `05_deep_agents_basics.ipynb`, `06_comparison.ipynb`)을 기준으로 정리하면 다음과 같습니다.

## 한 줄 요약
- **LangChain 에이전트**: 도구를 붙여 빠르게 에이전트를 만드는 **기본 레벨**의 프레임워크
- **Deep Agents**: 파일 작업, 태스크 관리, 백엔드, 서브에이전트까지 내장된 **올인원 고수준 에이전트**

## 핵심 차이

| 항목 | LangChain 에이전트 | Deep Agents |
|---|---|---|
| 추상화 수준 | 높음 | 매우 높음 |
| 핵심 개념 | 에이전트 + 도구 | 올인원 에이전트 |
| 생성 함수 | `create_agent()` | `create_deep_agent()` |
| 실행 방식 | `agent.invoke()` | `agent.invoke()` |
| 기본 제공 기능 | 도구 연결, ReAct 루프 | 도구 + 메모리 + 백엔드 + 태스크 플래닝 + 서브에이전트 |
| 상태/저장소 | 주로 메모리 기반 | LangGraph 기반 상태 + 파일시스템/샌드박스/로컬 백엔드 활용 |
| 적합한 작업 | 간단한 도구 호출, 빠른 프로토타입 | 파일 조작, 복잡한 작업 분해, 코딩/분석형 에이전트 |

## 노트북 기준으로 본 LangChain 에이전트
`02_langchain_basics.ipynb`에서는 다음처럼 설명합니다.
- `@tool`로 함수를 도구로 만든다
- `create_agent()`로 모델과 도구를 결합한다
- 내부적으로 **ReAct(Reasoning + Acting) 루프**를 사용한다
- 질문 → 도구 호출 → 관찰 → 반복 → 최종 응답의 흐름이다

즉, LangChain 에이전트는 **도구를 잘 호출하는 범용 에이전트**에 가깝습니다.

## 노트북 기준으로 본 Deep Agents
`05_deep_agents_basics.ipynb`에서는 `create_deep_agent()`를 통해 다음 기능이 내장된다고 설명합니다.
- `write_todos`로 태스크를 단계별로 분해
- `read_file`, `write_file`, `ls` 같은 파일 시스템 도구 사용
- 로컬 디스크, 샌드박스 등 **플러거블 백엔드** 지원
- 하위 작업을 위한 **서브에이전트 위임**
- LangGraph의 실행/메모리 인프라 활용

즉, Deep Agents는 단순히 도구를 호출하는 수준을 넘어서 **작업 계획, 파일 작업, 실행 환경 관리까지 포함한 에이전트 하네스**입니다.

## 구조적인 관계
노트북에는 다음처럼 정리되어 있습니다.
- Deep Agents는 **내부적으로 LangGraph를 사용**합니다.
- Deep Agents는 **LangChain의 모델/도구 인터페이스를 공유**합니다.
- 그래서 서로 완전히 대체 관계라기보다, **LangChain → LangGraph → Deep Agents**로 갈수록 추상화와 자동화 수준이 높아집니다.

## 언제 무엇을 쓰나
- **LangChain 에이전트**: 간단한 도구 호출, 빠른 실험, 기본기 학습
- **Deep Agents**: 파일 읽기/쓰기, 긴 작업 분해, 리포트 생성, 코딩 보조처럼 실제 작업 수행이 중요한 경우

## 결론
LangChain 에이전트는 **기본적인 에이전트 프레임워크**이고, Deep Agents는 그 위에 **작업 계획, 파일 시스템, 실행 백엔드, 서브에이전트**를 얹은 **더 완성도 높은 에이전트 시스템**입니다.

즉,
- **LangChain = 에이전트 만들기**
- **Deep Agents = 일을 실제로 끝내는 에이전트**
