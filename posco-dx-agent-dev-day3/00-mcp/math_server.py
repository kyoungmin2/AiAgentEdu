"""
MCP Math Server (Stdio 전송)

FastMCP로 구현한 간단한 수학 연산 MCP 서버입니다.
Stdio 전송 방식을 사용하므로, MCP 클라이언트가 이 스크립트를 서브프로세스로 직접 실행합니다.
별도의 서버 시작 명령이 필요하지 않습니다.

제공 도구:
  - add(a, b): 두 정수의 덧셈
  - multiply(a, b): 두 정수의 곱셈
"""
from fastmcp import FastMCP

# "Math"는 MCP 서버의 이름으로, 클라이언트에서 서버를 식별하는 데 사용됩니다.
mcp = FastMCP("Math")


@mcp.tool()
def add(a: int, b: int) -> int:
    """두 정수를 더합니다."""
    return a + b


@mcp.tool()
def multiply(a: int, b: int) -> int:
    """두 정수를 곱합니다."""
    return a * b


if __name__ == "__main__":
    # Stdio 전송: 표준 입출력을 통해 MCP 프로토콜 메시지를 주고받습니다.
    # MultiServerMCPClient가 이 스크립트를 서브프로세스로 실행합니다.
    mcp.run(transport="stdio")