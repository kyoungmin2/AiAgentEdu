# Day 1 실습

## 실습 목록

| 세션 | 실습 | 주제 | 유형 |
|:----:|------|------|------|
| 1교시 | [s1-agent-problem-definition](./s1-agent-problem-definition/) | Agent 문제 정의 — Pain→Task→Skill→Tool + 3가지 Agent 시연 | 시연 + 설계 |
| 2교시 | [s2-context-strategy](./s2-context-strategy/) | 컨텍스트 전략 심화 — System Prompt/메모리/Structured Output + LangSmith | 코드 실습 |
| 3교시 | [s3-agent-blueprint](./s3-agent-blueprint/) | Agent 구조 다이어그램 — Excalidraw로 Workflow 시각화 | 설계 |
| 4교시 | [s4-architecture-decision](./s4-architecture-decision/) | MCP(Tool) vs RAG 구조 비교 — 같은 문제를 두 방식으로 해결 | 코드 실습 |

---

## 환경 세팅

### 1. uv 설치

uv는 Rust로 만든 Python 패키지 매니저로, pip보다 10~100배 빠릅니다.

```bash
# Linux / WSL
curl -LsSf https://astral.sh/uv/install.sh | sh

# 설치 후 셸 재시작 또는 PATH 적용
source $HOME/.local/bin/env
```

설치 확인:

```bash
uv --version
```

### 2. 의존성 설치

이 디렉토리(`day1/`)에서 아래 명령어 한 번이면 가상환경 생성 + 패키지 설치가 완료됩니다.

```bash
cd day1
uv sync
```

> `uv sync`는 `pyproject.toml`을 읽어 `.venv/` 가상환경을 자동 생성하고 모든 의존성을 설치합니다.
> Python 버전도 `.python-version` 파일에 따라 자동으로 설치합니다.

### 3. 환경변수 설정

`.env` 파일을 `day1/` 디렉토리에 생성합니다.

```bash
cp .env.example .env   # 또는 직접 생성
```

![교육용 API KEY 노션](https://teamsparta.notion.site/GPT-api-key-0332dc3ef5148217807001b7a6b067b8?source=copy_link)

```env
OPENAI_API_KEY=sk-your-key-here
```

### 4. 실시간 API 연동 (선택)

실습에서 사용하는 도구들은 실제 API를 호출합니다. API 키가 없어도 fallback으로 실습이 가능하지만,
실제 API를 연동하면 더 현실적인 결과를 확인할 수 있습니다.

#### GitHub Token 발급

GitHub API rate limit을 높이려면 Personal Access Token을 발급합니다.
토큰이 없어도 공개 저장소 이슈 조회는 가능합니다 (시간당 60회 제한).

1. [github.com](https://github.com) → Settings → Developer settings → Personal access tokens → Fine-grained tokens
2. "Generate new token" 클릭 → Token name, Expiration 설정
3. Repository access: **Public Repositories (read-only)** 선택
4. 토큰 복사 → `.env` 파일에 추가:

```bash
GITHUB_TOKEN=ghp_your-token-here
```

#### Slack Bot 생성 + Token 발급

Slack 메시지 발송을 위해 Bot을 생성하고 OAuth Token을 발급합니다.
토큰이 없으면 메시지가 콘솔에만 출력됩니다.

1. [api.slack.com/apps](https://api.slack.com/apps) 접속 → **Create New App** → **From scratch**
2. App Name 입력 (예: `day1-lab-bot`), 워크스페이스 선택 → **Create App**
3. 좌측 메뉴 **OAuth & Permissions** → Bot Token Scopes에 `chat:write` 추가
4. 상단 **Install to Workspace** → **Allow** → `xoxb-...` 토큰 복사
5. Slack 채널에서 `/invite @day1-lab-bot` 으로 봇 초대
6. `.env` 파일에 추가:

```bash
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_CHANNEL=general
```

#### DuckDuckGo 검색

API 키 불필요 — `uv sync` 후 자동으로 사용 가능합니다.
네트워크가 불안정하면 자동으로 mock 데이터로 전환됩니다.

### 5. Jupyter Notebook 실행

실습은 Jupyter Notebook(`.ipynb`) 파일로 구성되어 있습니다.
`day1/` 디렉토리에서 아래 명령어로 Jupyter Lab을 실행합니다.

```bash
uv run jupyter lab
```

브라우저가 열리면 각 실습 폴더의 `src/` 디렉토리에서 노트북을 열어 셀을 순서대로 실행하세요.

> 가상환경을 직접 활성화하고 싶다면: `source .venv/bin/activate` 후 `jupyter lab`

---

## uv 주요 명령어

실습 중 자주 쓰는 명령어만 정리했습니다.

### 의존성 설치/관리

```bash
# 의존성 설치 (pyproject.toml 기준)
uv sync

# 패키지 추가
uv add requests

# 패키지 제거
uv remove requests

# 잠금 파일만 갱신 (설치 없이)
uv lock
```

### 코드 실행

```bash
# Jupyter Notebook 실행
uv run jupyter lab

# 가상환경 내에서 Python 실행 (스크립트 직접 실행 시)
uv run python script.py

# 가상환경 내에서 모듈 실행
uv run python -m pytest
```

### 가상환경 관리

```bash
# 가상환경 직접 생성 (보통 uv sync가 자동 처리)
uv venv

# 설치된 패키지 목록 확인
uv pip list

# 특정 패키지 정보 확인
uv pip show openai
```

### pip과 비교

| 작업 | pip | uv |
|------|-----|-----|
| 가상환경 생성 | `python -m venv .venv` | `uv venv` (또는 `uv sync` 시 자동) |
| 의존성 설치 | `pip install -r requirements.txt` | `uv sync` |
| 패키지 추가 | `pip install requests` + 수동으로 requirements.txt 수정 | `uv add requests` |
| 패키지 제거 | `pip uninstall requests` + 수동 삭제 | `uv remove requests` |
| 스크립트 실행 | `source .venv/bin/activate && python script.py` | `uv run python script.py` |
| Jupyter 실행 | `source .venv/bin/activate && jupyter lab` | `uv run jupyter lab` |
