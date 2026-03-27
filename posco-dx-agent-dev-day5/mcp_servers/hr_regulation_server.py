"""
MCP HR Regulation Server (Stdio transport)

울산 인사/급여/복리 규정 및 지방공기업법 PDF를 조회하기 위한 MCP 서버입니다.
MCP 클라이언트가 이 파일을 서브프로세스로 실행합니다.

제공 도구:
  - list_regulation_sources(): 로드 가능한 규정 파일 목록
  - search_regulations(query, category, top_k): 규정 본문 검색
  - get_regulation_page(category, page): 특정 페이지 원문 확인
    - compare_regulation_topic(topic): 인사/급여/복리/법령 간 토픽 비교
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Tuple

from fastmcp import FastMCP
from pypdf import PdfReader

mcp = FastMCP("HRRegulation")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REGULATION_DIR = PROJECT_ROOT / "rag" / "documents"

REGULATION_FILES: Dict[str, str] = {
    "personnel": "UlsanPersonnelRegulations.pdf",
    "salary": "UlsanSalaryRegulations.pdf",
    "welfare": "UlsanWalfareRegulations.pdf",
    "law": "LocalPublicEnterprisesAct.pdf",
}

CATEGORY_ALIASES: Dict[str, str] = {
    "personnel": "personnel",
    "hr": "personnel",
    "insa": "personnel",
    "인사": "personnel",
    "salary": "salary",
    "pay": "salary",
    "급여": "salary",
    "보수": "salary",
    "welfare": "welfare",
    "benefit": "welfare",
    "복리": "welfare",
    "복리후생": "welfare",
    "law": "law",
    "act": "law",
    "legal": "law",
    "법령": "law",
    "지방공기업법": "law",
}

# category -> list of (page_number, text)
_page_cache: Dict[str, List[Tuple[int, str]]] = {}

def _resolve_category(raw: str) -> str:
    key = (raw or "").strip().lower()
    if key in ("", "all"):
        return "all"
    if key in CATEGORY_ALIASES:
        return CATEGORY_ALIASES[key]
    raise ValueError(
        "category는 personnel/hr/인사, salary/급여/보수, welfare/복리, law/법령/지방공기업법 중 하나여야 합니다."
    )


def _category_display_name(category: str) -> str:
    mapping = {
        "personnel": "인사",
        "salary": "급여",
        "welfare": "복리",
        "law": "지방공기업법",
    }
    return mapping.get(category, category)


def _resolve_regulation_path(filename: str) -> Path:
    preferred = REGULATION_DIR / filename
    if preferred.exists():
        return preferred

    # Backward compatibility: support old location at project root.
    legacy = PROJECT_ROOT / filename
    return legacy


def _load_pages(category: str) -> List[Tuple[int, str]]:
    if category in _page_cache:
        return _page_cache[category]

    filename = REGULATION_FILES[category]
    path = _resolve_regulation_path(filename)
    if not path.exists():
        raise FileNotFoundError(
            f"규정 파일을 찾을 수 없습니다: {filename} (searched: {REGULATION_DIR} and {PROJECT_ROOT})"
        )

    reader = PdfReader(path)
    pages: List[Tuple[int, str]] = []
    for idx, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if text:
            pages.append((idx, text))

    _page_cache[category] = pages
    return pages


def _tokenize(text: str) -> List[str]:
    return [t for t in re.split(r"\s+", text.strip()) if len(t) >= 2]


def _make_excerpt(page_text: str, query: str, radius: int = 220) -> str:
    compact = re.sub(r"\s+", " ", page_text)
    q = query.strip()
    if not compact:
        return ""

    pos = compact.lower().find(q.lower()) if q else -1
    if pos < 0:
        tokens = _tokenize(q)
        for token in tokens:
            pos = compact.lower().find(token.lower())
            if pos >= 0:
                break

    if pos < 0:
        return compact[: radius * 2]

    start = max(0, pos - radius)
    end = min(len(compact), pos + radius)
    snippet = compact[start:end]
    if start > 0:
        snippet = "..." + snippet
    if end < len(compact):
        snippet = snippet + "..."
    return snippet


def _search_in_category(category: str, query: str, top_k: int) -> List[Tuple[int, int, str]]:
    pages = _load_pages(category)
    q = query.strip().lower()
    tokens = _tokenize(query.lower())

    scored: List[Tuple[int, int, str]] = []
    for page_no, text in pages:
        lower = text.lower()
        score = 0

        if q and q in lower:
            score += 8

        for token in tokens:
            score += lower.count(token)

        if score > 0:
            scored.append((score, page_no, _make_excerpt(text, query)))

    scored.sort(key=lambda x: (-x[0], x[1]))
    return scored[:top_k]


@mcp.tool()
def list_regulation_sources() -> str:
    """조회 가능한 인사/급여/복리 규정 및 법령 PDF 목록을 반환합니다."""
    lines = ["규정 파일 목록:"]
    for category, filename in REGULATION_FILES.items():
        path = _resolve_regulation_path(filename)
        status = "OK" if path.exists() else "MISSING"
        lines.append(
            f"- {category} ({_category_display_name(category)}): {filename} [{status}] path={path}"
        )
    return "\n".join(lines)


@mcp.tool()
def search_regulations(query: str, category: str = "all", top_k: int = 5) -> str:
    """인사/급여/복리 규정 및 지방공기업법 PDF에서 키워드를 검색합니다.

    Args:
        query: 검색할 키워드 또는 문장
        category: personnel/salary/welfare/law/all 또는 한글 별칭(인사/급여/복리/법령)
        top_k: 반환할 최대 결과 수 (1~10)
    """
    if not query or not query.strip():
        raise ValueError("query는 비어 있을 수 없습니다.")

    top_k = max(1, min(10, top_k))
    resolved = _resolve_category(category)
    categories = list(REGULATION_FILES.keys()) if resolved == "all" else [resolved]

    result_lines = [f"검색어: {query}"]
    found_any = False

    for cat in categories:
        hits = _search_in_category(cat, query, top_k=top_k)
        result_lines.append(f"\n[{_category_display_name(cat)} 규정]")
        if not hits:
            result_lines.append("- 일치 결과 없음")
            continue

        found_any = True
        for rank, (score, page_no, excerpt) in enumerate(hits, start=1):
            filename = REGULATION_FILES[cat]
            result_lines.append(
                f"{rank}. source={filename} page={page_no} score={score}\n   {excerpt}"
            )

    if not found_any:
        result_lines.append("\n도움말: 키워드를 더 짧게 하거나 category를 all로 시도해 보세요.")

    return "\n".join(result_lines)


@mcp.tool()
def get_regulation_page(category: str, page: int) -> str:
    """특정 규정 PDF의 페이지 원문을 반환합니다.

    Args:
        category: personnel/salary/welfare/law 또는 한글 별칭(인사/급여/복리/법령)
        page: 1부터 시작하는 페이지 번호
    """
    resolved = _resolve_category(category)
    if resolved == "all":
        raise ValueError("get_regulation_page에서는 category에 all을 사용할 수 없습니다.")
    if page <= 0:
        raise ValueError("page는 1 이상의 정수여야 합니다.")

    pages = _load_pages(resolved)
    for page_no, text in pages:
        if page_no == page:
            filename = REGULATION_FILES[resolved]
            return f"source={filename} page={page_no}\n\n{text}"

    raise ValueError(f"요청한 페이지를 찾을 수 없습니다: {page}")


@mcp.tool()
def compare_regulation_topic(topic: str) -> str:
    """동일 토픽을 인사/급여/복리/법령 문서에서 각각 1건씩 찾아 비교합니다.

    Args:
        topic: 비교할 주제 키워드 (예: 연차, 수당, 경조사)
    """
    if not topic or not topic.strip():
        raise ValueError("topic은 비어 있을 수 없습니다.")

    lines = [f"토픽 비교: {topic}"]
    for category in ("personnel", "salary", "welfare", "law"):
        hits = _search_in_category(category, topic, top_k=1)
        lines.append(f"\n[{_category_display_name(category)} 규정]")
        if not hits:
            lines.append("- 관련 내용 없음")
            continue

        score, page_no, excerpt = hits[0]
        lines.append(
            f"- source={REGULATION_FILES[category]} page={page_no} score={score}\n  {excerpt}"
        )

    return "\n".join(lines)


if __name__ == "__main__":
    mcp.run(transport="stdio")
