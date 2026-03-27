# Tool Routing Test Scenarios (app.py 실행 로그 기준)

이 문서는 [app.py](app.py)에서 표시되는 Tool Step 로그(on_tool_start/on_tool_end)를 기준으로,
질문 유형별 도구 라우팅이 의도대로 동작하는지 확인하는 시나리오입니다.

## 사전 조건

- 실행 명령: `uv run chainlit run app.py -w`
- 브라우저에서 채팅 UI 접속
- Tool Step이 보이는지 확인
  - [app.py](app.py#L53)에서 `on_tool_start` 이벤트를 Step으로 출력
  - [app.py](app.py#L58)에서 `on_tool_end` 결과를 Step으로 출력

## 검증 포인트

- 각 질문에 대해 "최초 호출 도구"가 기대값과 일치하는지 확인
- 필요 시 "후속 도구"가 기대 순서로 호출되는지 확인
- 최종 답변에 source/page 근거가 포함되는지 확인

---

## 시나리오 1: 규정 파일 상태 점검

- 사용자 질문:
  - `규정 PDF 파일들이 지금 정상 로드 가능한 상태인지 확인해줘.`
- 기대 최초 도구:
  - `list_regulation_sources`
- 기대 후속 도구:
  - 없음
- 합격 기준:
  - Tool Step에 `list_regulation_sources`가 1회 표시
  - 응답에 파일별 `OK`/`MISSING` 상태가 포함

## 시나리오 2: 일반 규정 검색(전체 카테고리)

- 사용자 질문:
  - `연차 사용 기준을 찾아서 핵심만 정리해줘.`
- 기대 최초 도구:
  - `search_regulations` (category=all)
- 기대 후속 도구:
  - 필요 시 `get_regulation_page`
- 합격 기준:
  - 최초 Tool Step이 `search_regulations`
  - 답변에 최소 1개 이상 `source=... page=...` 근거 포함

## 시나리오 3: 카테고리 지정 검색(급여)

- 사용자 질문:
  - `급여 규정에서 시간외수당 관련 기준을 찾아줘.`
- 기대 최초 도구:
  - `search_regulations` (category=salary)
- 기대 후속 도구:
  - 필요 시 `get_regulation_page` (salary, 특정 page)
- 합격 기준:
  - `search_regulations` 호출 확인
  - 결과 또는 최종 답변에 급여 규정 파일명과 페이지 정보 포함

## 시나리오 4: 규정 비교 질문

- 사용자 질문:
  - `경조사 기준을 인사/급여/복리/지방공기업법 관점에서 비교해줘.`
- 기대 최초 도구:
  - `compare_regulation_topic`
- 기대 후속 도구:
  - 필요 시 `search_regulations`
- 합격 기준:
  - `compare_regulation_topic` 호출 확인
  - 응답에 인사/급여/복리/법령 4개 관점 비교 내용 포함

## 시나리오 5: 지방공기업법 카테고리 검색

- 사용자 질문:
  - `지방공기업법에서 임원 임면 관련 조항을 찾아줘.`
- 기대 최초 도구:
  - `search_regulations` (category=law)
- 기대 후속 도구:
  - 필요 시 `get_regulation_page` (law, 특정 page)
- 합격 기준:
  - `search_regulations` 호출 확인
  - 결과 또는 최종 답변에 `LocalPublicEnterprisesAct.pdf`와 페이지 정보 포함

## 시나리오 6: 계산형 질문

- 사용자 질문:
  - `기본급 2,100,000원과 수당 350,000원, 120,000원의 합계를 계산해줘.`
- 기대 최초 도구:
  - `add`
- 기대 후속 도구:
  - 필요 시 `add` 추가 호출
- 합격 기준:
  - Tool Step에 `add`가 표시
  - 최종 합계 수치가 정확함

---

## 실행 체크리스트

1. 각 시나리오 질문을 순서대로 입력
2. Tool Step 이름과 입력값을 캡처
3. 기대 최초 도구와 실제 최초 도구를 비교
4. 후속 도구 호출 여부와 근거(source/page) 포함 여부 확인
5. 실패 시 [prompts/system.md](prompts/system.md)의 "도구 호출 우선순위(자동 가이드)"와 [agent.py](agent.py)의 MCP 연결 설정 재확인

## 실패 원인 빠른 진단

- `list_regulation_sources`가 호출되지 않음:
  - 질문을 상태 점검형으로 더 명시적으로 작성
- HR 관련 도구 호출 대신 `retrieve`만 호출됨:
  - 질문에 `인사/급여/복리/법령` 키워드를 포함해 재시도
- source/page가 빠짐:
  - 후속 질문으로 `근거 페이지를 포함해 다시 답변해줘` 요청
- 계산 질문에서 도구 미호출:
  - 수치 연산 의도를 명확히 표현
