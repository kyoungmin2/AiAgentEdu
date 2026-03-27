# HR Regulation MCP 서버 함수 가이드

이 문서는 [mcp_servers/hr_regulation_server.py](mcp_servers/hr_regulation_server.py)의 MCP 도구 함수 용도와 활용 방법을 설명합니다.

## 1) 서버 개요

- 목적: 인사, 급여, 복리 규정 + 지방공기업법 PDF 4종에서 근거 기반 검색과 조회를 수행
- 서버명: HRRegulation
- 전송 방식: stdio
- 대상 파일:
  - UlsanPersonnelRegulations.pdf
  - UlsanSalaryRegulations.pdf
  - UlsanWalfareRegulations.pdf
  - LocalPublicEnterprisesAct.pdf

## 2) 함수별 용도와 활용

### list_regulation_sources

- 용도: 서버가 읽을 규정 파일이 정상 위치에 있는지 확인
- 입력: 없음
- 출력: 규정 파일 목록과 상태(OK 또는 MISSING)
- 활용 시점:
  - 서버 첫 실행 직후
  - 배포 경로 변경 후
  - 파일명 오타 의심 시

추천 질문 예시
- 인사 규정 파일이 정상적으로 로드되었는지 확인해줘
- 급여/복리 파일 상태 점검해줘

### search_regulations(query, category="all", top_k=5)

- 용도: 규정 본문에서 키워드 또는 문장을 검색
- 입력:
  - query: 검색어(필수)
  - category: personnel, salary, welfare, law, all 또는 한글 별칭(인사, 급여, 복리, 법령, 지방공기업법)
  - top_k: 결과 개수(1~10)
- 출력: 카테고리별 검색 결과, 파일명, 페이지, 점수, 발췌문
- 활용 시점:
  - 사용자의 일반 규정 질의에 대한 1차 탐색
  - 특정 주제 근거 페이지 후보 추출

추천 질문 예시
- 연차 사용 기준을 찾아줘
- 급여 category로 초과근무 수당 규정을 검색해줘
- 복리후생 중 경조사 관련 조항을 찾아줘
- 지방공기업법에서 임원 임면 관련 조항을 찾아줘

운영 팁
- 검색어가 길어서 결과가 없으면 짧은 핵심어로 재검색
- category를 all로 먼저 탐색한 뒤 세부 category로 좁히기

### get_regulation_page(category, page)

- 용도: 특정 규정 PDF의 지정 페이지 원문 조회
- 입력:
  - category: personnel, salary, welfare, law 또는 한글 별칭
  - page: 1 이상의 페이지 번호
- 출력: 파일명, 페이지 번호, 원문 텍스트
- 활용 시점:
  - search_regulations 결과를 근거 확인용으로 상세 조회
  - 답변 전 원문 문구 검증

추천 질문 예시
- 인사 규정 12페이지 원문 보여줘
- 급여 규정 page 7 내용을 확인해줘

운영 팁
- category에 all은 허용되지 않음
- 페이지가 존재하지 않으면 오류 반환

### compare_regulation_topic(topic)

- 용도: 동일 주제를 인사, 급여, 복리, 지방공기업법에서 각각 1건씩 비교
- 입력:
  - topic: 비교할 주제(예: 연차, 수당, 경조사)
- 출력: 각 규정별 최상위 매칭 1건(파일, 페이지, 점수, 발췌)
- 활용 시점:
  - 규정 간 적용 기준 비교
  - 답변 작성 전 충돌 가능성 탐지

추천 질문 예시
- 연차를 인사/급여/복리/법령 관점에서 비교해줘
- 경조사 관련 내용을 4개 문서에서 비교해줘

## 3) 권장 호출 순서

1. list_regulation_sources로 파일 상태 점검
2. search_regulations로 관련 조항 후보 검색
3. get_regulation_page로 원문 확인
4. compare_regulation_topic으로 규정 간 차이 검토

## 4) 에이전트 응답 품질을 높이는 사용 전략

- 근거 우선: 검색 결과의 source와 page를 반드시 함께 제시
- 추정 금지: 결과가 없으면 없다고 명확히 답변
- 검증 루프: 검색 후 페이지 원문 확인을 거쳐 최종 답변
- 비교 질문 대응: 단일 규정 답변 전에 compare 함수로 교차 확인

## 5) 에러/예외 상황

- 파일 누락: list_regulation_sources에서 MISSING 표기
- 잘못된 category: category 입력값 오류
- 빈 query 또는 topic: 필수 입력값 오류
- 잘못된 page: 1 미만 또는 존재하지 않는 페이지 오류

## 6) 실무 적용 시나리오

- 인사 담당자 질의 응답
  - 예: 연차, 휴직, 징계, 승진 관련 규정 확인
- 급여 검증 지원
  - 예: 수당 지급 기준, 공제, 보수 체계 확인
- 복리후생 안내
  - 예: 복지 항목, 경조사 지원 기준 안내
- 규정 충돌 점검
  - 예: 동일 주제의 부서별 해석 차이 사전 검토
- 법령 적합성 점검
  - 예: 내부 규정이 지방공기업법 취지와 상충하는지 1차 검토

## 7) 관련 파일

- 서버 구현: [mcp_servers/hr_regulation_server.py](mcp_servers/hr_regulation_server.py)
- 기존 예제 서버: [mcp_servers/math_server.py](mcp_servers/math_server.py)
- MCP 설명 문서: [mcp_servers/README.md](mcp_servers/README.md)
