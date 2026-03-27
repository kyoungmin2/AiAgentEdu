# 울산시설공단 HR·법령 어시스턴트 아키텍처 정리

## 1) 챗봇 제목
- 울산시설공단 HR·법령 어시스턴트 (인사/급여/복리/지방공기업법)

## 2) 활용 목적
- 인사·급여·복리 규정과 지방공기업법을 근거 기반으로 빠르게 조회, 비교, 실무 적용까지 지원
- 단순 질의응답을 넘어 근거 확인, 비교 분석, 실행 체크리스트를 한 번에 제공

## 3) 적용 기술 구성
- RAG
- rag/documents의 md/pdf 문서를 임베딩(text-embedding-3-small)으로 인덱싱
- retrieve 도구로 관련 문서 Top-K 검색 후 근거 텍스트 반환

- MCP Server
- math_server: add, multiply 계산 도구 제공
- hr_regulation_server: list_regulation_sources, search_regulations, get_regulation_page, compare_regulation_topic 제공
- stdio 기반 MultiServerMCPClient로 에이전트에 통합

- Skills
- skills/hr-regulation-report/SKILL.md: 인사/급여/복리/법령 질의 보고서 양식
- skills/weekly-report/SKILL.md: 주간 보고서 양식
- 질의 유형에 맞춰 정형화된 출력 형식 적용

- 프롬프팅
- prompts/system.md: 도구 호출 우선순위, 답변 형식, 주의사항 규칙 정의
- agent.py의 hybrid_tool_guide: 도구 선택 가이드(규정/계산/보고서)
- prompts/AGNETS.md 메모리 규칙을 함께 주입해 응답 일관성 강화

## 4) 전체 Workflow (End-to-End)
1. 사용자 질문 수신 (Chainlit UI)
2. 에이전트가 질문 의도를 분류 (규정 질의, 계산 질의, 보고서 질의 등)
3. 필요 도구 선택
4. 규정/법령 질의: hr_regulation MCP 도구 우선 호출
5. 사내 일반 규정 보강: RAG retrieve 호출
6. 계산 요청: math MCP 도구 호출
7. 응답 구성 시 Skill 양식 적용 (해당 시)
8. 본문은 비교정리/실무적용/주의사항 중심으로 생성
9. 근거 문서는 우측 Preview 패널에 별도 표시
10. 최종 답변 전달 및 Langfuse 트레이싱 기록

## 5) 기대 효과
- 근거 기반 정확도 향상: 규정/법령 문서 검색과 원문 확인 가능
- 확장성 확보: MCP 서버 추가만으로 도메인 기능 확장 용이
- 실무 활용성 강화: Skill 양식으로 보고서형 결과를 일관되게 제공
- 운영 가시성 확보: Langfuse 기반 도구 호출 및 추론 흐름 추적 가능
