"""
Chainlit 웹 UI — 이 파일은 수정하지 않아도 됩니다.

agent.py의 create_base_agent()를 호출하여 에이전트를 생성하고,
사용자 메시지를 전달하여 응답을 표시합니다.

실행: uv run chainlit run app.py
"""

import logging
import re
import uuid

# OpenTelemetry의 async 컨텍스트 충돌 경고 억제 (기능에 영향 없음)
logging.getLogger("opentelemetry.context").setLevel(logging.CRITICAL)

import chainlit as cl
from langfuse.langchain import CallbackHandler as LangfuseCallbackHandler

from agent import create_base_agent


def _collect_text_fragments(value: object) -> list[str]:
    """중첩된 tool 출력에서 text 필드를 우선적으로 추출합니다."""
    fragments: list[str] = []

    if value is None:
        return fragments

    if isinstance(value, str):
        fragments.append(value)
        return fragments

    if isinstance(value, dict):
        if isinstance(value.get("text"), str):
            fragments.append(value["text"])
        # text 이외에도 content/data 내부에 텍스트가 있는 경우 재귀적으로 탐색
        for nested_key in ("content", "data", "output", "message", "messages"):
            if nested_key in value:
                fragments.extend(_collect_text_fragments(value[nested_key]))
        return fragments

    if isinstance(value, list):
        for item in value:
            fragments.extend(_collect_text_fragments(item))
        return fragments

    fragments.append(str(value))
    return fragments


def _to_text_output(output: object) -> str:
    """도구 출력 객체를 사람이 읽기 쉬운 단일 문자열로 변환합니다."""
    if hasattr(output, "content"):
        content = output.content
        parts = _collect_text_fragments(content)
        if parts:
            return "\n".join(parts)
        return str(content)

    parts = _collect_text_fragments(output)
    if parts:
        return "\n".join(parts)
    return str(output)


def _trim_preview(text: str, limit: int = 150) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    if not compact:
        return ""
    return compact[:limit] + ("..." if len(compact) > limit else "")


def _extract_evidence_previews(text: str) -> dict[str, list[str]]:
    """tool 출력 텍스트에서 파일별 미리보기 문장을 추출합니다."""
    evidence: dict[str, list[str]] = {}
    known_files = [
        "UlsanPersonnelRegulations.pdf",
        "UlsanSalaryRegulations.pdf",
        "UlsanWalfareRegulations.pdf",
        "LocalPublicEnterprisesAct.pdf",
    ]
    category_to_file = {
        "인사": "UlsanPersonnelRegulations.pdf",
        "급여": "UlsanSalaryRegulations.pdf",
        "복리": "UlsanWalfareRegulations.pdf",
        "지방공기업법": "LocalPublicEnterprisesAct.pdf",
    }

    # search_regulations 출력 예시:
    # 1. source=UlsanSalaryRegulations.pdf page=2 score=9
    #    발췌문...
    for filename, excerpt in re.findall(
        r"source=([^\s]+)\s+page=\d+\s+score=\d+\n\s*(.+)", text
    ):
        preview = _trim_preview(excerpt)
        if preview:
            evidence.setdefault(filename, []).append(preview)

    # get_regulation_page 출력 예시:
    # source=UlsanPersonnelRegulations.pdf page=12
    #
    # 원문...
    for match in re.finditer(r"source=([^\s]+)\s+page=\d+\n\n", text):
        filename = match.group(1)
        body = text[match.end() :]
        preview = _trim_preview(body)
        if preview:
            evidence.setdefault(filename, []).append(preview)

    # retrieve 출력 예시:
    # [UlsanPersonnelRegulations.pdf] 본문...
    for filename, snippet in re.findall(r"\[([^\]]+\.pdf)\]\s*([^\n]+)", text):
        preview = _trim_preview(snippet)
        if preview:
            evidence.setdefault(filename, []).append(preview)
        else:
            evidence.setdefault(filename, [])

    # [인사 규정] / [급여 규정] 같은 섹션 헤더 기반 fallback
    for category, body in re.findall(r"\[(인사|급여|복리|지방공기업법)\s+규정\]\s*\n?([^\n]+)", text):
        filename = category_to_file[category]
        preview = _trim_preview(body)
        if preview:
            evidence.setdefault(filename, []).append(preview)

    # 파일명만 노출되는 변형 포맷 fallback
    compact = re.sub(r"\s+", " ", text)
    for filename in known_files:
        if filename not in compact:
            continue
        idx = compact.find(filename)
        tail = compact[idx + len(filename) : idx + len(filename) + 220]
        preview = _trim_preview(tail)
        if preview:
            evidence.setdefault(filename, []).append(preview)
        else:
            evidence.setdefault(filename, [])

    return evidence


def _merge_evidence_previews(
    base: dict[str, list[str]],
    new_data: dict[str, list[str]],
    max_per_file: int = 2,
) -> dict[str, list[str]]:
    """파일별 미리보기 문장을 중복 제거하며 누적합니다."""
    for filename, previews in new_data.items():
        existing = base.setdefault(filename, [])
        for preview in previews:
            if preview and preview not in existing:
                existing.append(preview)
            if len(existing) >= max_per_file:
                break
    return base


def _build_side_evidence_view(evidence: dict[str, list[str]]) -> str:
    """우측 사이드 패널에 표시할 파일별 근거 Preview 문자열을 생성합니다."""
    preferred_order = [
        "UlsanPersonnelRegulations.pdf",
        "UlsanSalaryRegulations.pdf",
        "UlsanWalfareRegulations.pdf",
        "LocalPublicEnterprisesAct.pdf",
    ]
    menu_labels = {
        "UlsanPersonnelRegulations.pdf": "인사규정",
        "UlsanSalaryRegulations.pdf": "급여규정",
        "UlsanWalfareRegulations.pdf": "복지규정",
        "LocalPublicEnterprisesAct.pdf": "지방법률규정",
    }

    lines = ["### 근거 파일 Preview", ""]

    def append_line(filename: str, previews: list[str]) -> None:
        summary = previews[0] if previews else "본문 요약을 생성할 수 없습니다."
        label = menu_labels.get(filename, filename)
        lines.append(f"- {label}: {summary}")
        if label != filename:
            lines.append(f"  출처 파일: {filename}")

    shown = set()
    for filename in preferred_order:
        if filename not in evidence:
            continue
        append_line(filename, evidence[filename])
        shown.add(filename)

    for filename in sorted(k for k in evidence if k not in shown):
        append_line(filename, evidence[filename])

    if len(lines) == 2:
        lines.append("- 근거 파일을 아직 추출하지 못했습니다.")
        lines.append("  동일 질문을 한 번 더 요청하거나 키워드를 구체화해 주세요.")

    return "\n".join(lines)


@cl.on_chat_start
async def on_chat_start():
    """새 채팅 세션이 시작될 때 에이전트를 생성합니다."""
    agent = await create_base_agent()
    thread_id = str(uuid.uuid4())

    cl.user_session.set("agent", agent)
    cl.user_session.set("thread_id", thread_id)

    await cl.Message(
        content=(
            "안녕하세요! 울산시설공단 인사/급여/복리/지방공기업법 기반 챗봇입니다.\n\n"
            "질의 예시:\n"
            "1. 경조사 휴가 기준을 인사/복리 규정 기준으로 정리해줘.\n"
            "2. 지방공기업법에서 임원 임면 관련 조항을 찾아줘.\n"
            "3. 연차 규정을 인사/급여/복리/법령 관점으로 비교해줘.\n"
            "4. 규정 파일 상태를 점검해줘."
        )
    ).send()


@cl.on_message
async def on_message(message: cl.Message):
    """사용자 메시지를 에이전트에 전달하고 응답을 스트리밍으로 표시합니다."""
    agent = cl.user_session.get("agent")
    thread_id = cl.user_session.get("thread_id")

    langfuse_handler = LangfuseCallbackHandler()
    config = {
        "configurable": {"thread_id": thread_id},
        "callbacks": [langfuse_handler],
        "recursion_limit": 100,  # 기본값 25에서 100으로 증가 (도구 반복 호출 대비)
    }

    msg = cl.Message(content="")
    tool_steps: dict[str, cl.Step] = {}
    collected_evidence: dict[str, list[str]] = {}

    async for event in agent.astream_events(
        {"messages": [{"role": "user", "content": message.content}]},
        config=config,
        version="v2",
    ):
        kind = event["event"]

        if kind == "on_tool_start":
            step = cl.Step(name=event["name"], type="tool")
            # Tool 입력 정보를 간단하게 표시 (전체 JSON 노출 방지)
            input_data = event["data"].get("input", "")
            if isinstance(input_data, dict):
                input_summary = ", ".join(f"{k}: {str(v)[:50]}" for k, v in input_data.items())
                step.input = f"{{{input_summary}}}"
            else:
                step.input = str(input_data)[:100]
            tool_steps[event["run_id"]] = step

        elif kind == "on_tool_end":
            step = tool_steps.pop(event["run_id"], None)
            output = event["data"].get("output", "")
            output_text = _to_text_output(output)

            # 답변 옆 사이드 패널에 표시할 근거 파일 preview를 누적
            parsed = _extract_evidence_previews(output_text)
            _merge_evidence_previews(collected_evidence, parsed)

            if step:
                # Tool 출력이 매우 길면 축약 (사용자 메시지 간결성 유지)
                step.output = output_text[:200] + ("..." if len(output_text) > 200 else "")
                # ⭐ Step을 보이지 않게 처리: send() 호출 제거 (내부 추적만 유지)
                # await step.send()

        elif kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                await msg.stream_token(content)

    msg.elements = [
        cl.Text(
            name="근거 파일",
            content=_build_side_evidence_view(collected_evidence),
            display="side",
        )
    ]

    await msg.send()