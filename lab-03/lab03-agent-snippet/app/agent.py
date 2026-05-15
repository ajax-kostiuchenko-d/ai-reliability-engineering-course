"""Lab 3 — ADK agent using custom MCP server (Streamable HTTP).

  export GOOGLE_GENAI_USE_VERTEXAI=FALSE
  export GOOGLE_API_KEY='...'   # https://aistudio.google.com/apikey
  export LAB03_MCP_URL=http://127.0.0.1:3000/mcp
  agents-cli playground
"""

import os

from google.adk.agents.llm_agent import Agent
from google.adk.apps.app import App
from google.adk.models.google_llm import Gemini
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams

MCP_URL = os.getenv(
    "LAB03_MCP_URL",
    "http://lab03-mcp-server.kagent.svc.cluster.local:3000/mcp",
)

root_agent = Agent(
    name="lab03_mcp_agent",
    model=Gemini(model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash")),
    description="Lab 3 agent that calls tools from the kmcp MCP server in abox.",
    instruction="""You are a helpful lab assistant for AI Reliability Engineering.

Use MCP tools when the user asks to greet someone or test the lab03 server.
Always explain which tool you used and summarize the result in Markdown.
If MCP tools are unavailable, say so clearly.""",
    tools=[
        McpToolset(
            connection_params=StreamableHTTPConnectionParams(url=MCP_URL),
        ),
    ],
)

# Required by agents-cli prototype: app/__init__.py does `from .agent import app`
app = App(root_agent=root_agent, name="app")
