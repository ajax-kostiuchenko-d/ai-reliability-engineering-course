"""Lab 3 custom greet tool for kmcp MCP server."""

from mcp.types import ToolAnnotations

from core.server import mcp


@mcp.tool(
    annotations=ToolAnnotations(
        title="Lab03 Greet",
        readOnlyHint=True,
    ),
)
def lab03_greet(name: str) -> str:
    """Return a short greeting for AI Reliability Engineering lab 3.

    Args:
        name: Person name to greet

    Returns:
        Greeting string
    """
    return f"Hello, {name}! MCP server lab03-mcp-server is running in abox."
