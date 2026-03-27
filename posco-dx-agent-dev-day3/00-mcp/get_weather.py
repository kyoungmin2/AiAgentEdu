"""
MCP Weather Server (Streamable HTTP 전송)

FastMCP로 구현한 날씨 정보 MCP 서버입니다.
Streamable HTTP 전송 방식을 사용하므로, 별도 터미널에서 미리 실행해야 합니다.

실행 방법:
  $ python get_weather.py
  → http://localhost:8000/mcp 에서 MCP 서버가 시작됩니다.

제공 도구:
  - get_weather(location): 지정한 위치의 날씨 정보를 반환
"""
from fastmcp import FastMCP

# "Weather"는 MCP 서버의 이름으로, 클라이언트에서 서버를 식별하는 데 사용됩니다.
mcp = FastMCP("Weather")


@mcp.tool()
async def get_weather(location: str) -> str:
    """지정한 위치의 날씨 정보를 반환합니다."""
    # 데모용 하드코딩 응답 — 실제 서비스에서는 날씨 API를 호출합니다.
    return "It's always sunny in New York"


if __name__ == "__main__":
    # Streamable HTTP 전송: HTTP 서버를 띄워 원격 클라이언트가 접속할 수 있게 합니다.
    # 기본 포트 8000, 엔드포인트 /mcp
    mcp.run(transport="streamable-http")