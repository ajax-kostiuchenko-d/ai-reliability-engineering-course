# Lab 3 — kmcp, agents-cli, MCP Inspector (beginners)

Coursework for **AI Reliability Engineering 2.0**.

## Course objectives (beginners)

| Track           | What to deliver                                                                                                                                  |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Research**    | Real technical and business use cases for **one** of: MCP Sampling / Elicitation / MCP Apps                                                      |
| **Development** | 1) Custom MCP via **kmcp** in **abox** · 2) Agent via **agents-cli** + MCP · 3) Test with **MCP Inspector** `0.21.1` + **agents-cli playground** |

## Prerequisites

- **Lab 2 complete:** cluster `kind-abox` (`kubectl config current-context` → `kind-abox`), `flux get all` Ready, kagent and agentgateway running.
- Tools: Docker, `kubectl`, `helm`, `uv`, Node.js, Python 3.11+, `kind` CLI (for loading images into KinD).
- LLM key: `GOOGLE_API_KEY` for agents-cli / Gemini (see [authentication](https://google.github.io/agents-cli/guide/authentication/)). Lab 2 kagent in abox may still use `OPENAI_API_KEY`.

**abox note:** Do **not** run `helm install kmcp-crds` or `kmcp install` on abox — kagent already ships the `mcpservers.kagent.dev` CRD and `kagent-kmcp-controller-manager`. Use `kmcp deploy --namespace kagent` only.

## Files in this directory

| File                                                                                           | Purpose                                                                |
| ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| [`LAB03-beginners-development.md`](LAB03-beginners-development.md)                             | Development runbook: kmcp → abox → agents-cli → inspector / playground |
| [`LAB03-research.md`](LAB03-research.md)                                                       | Research write-up: MCP Apps (cases + reliability)                      |
| [`LAB03-research-case-datadog-sre-dashboard.md`](LAB03-research-case-datadog-sre-dashboard.md) | Featured research case: SRE dashboard + Datadog                        |
| [`LAB03-research-mcp-extensions.md`](LAB03-research-mcp-extensions.md)                         | Reference: Sampling vs Elicitation vs Apps                             |
| [`ABOX-restart.md`](ABOX-restart.md)                                                           | How to bring abox back up after `make down`                            |
| [`lab03-mcp-server/`](lab03-mcp-server/)                                                       | kmcp project (custom tools under `src/tools/`)                         |
| [`lab03-agent-snippet/`](lab03-agent-snippet/)                                                 | Reference `app/agent.py` — copy after `agents-cli create`              |
| [`k8s/`](k8s/)                                                                                 | Optional: deploy the agent into abox                                   |
| [`screenshots/README.md`](screenshots/README.md)                                               | Evidence checklist for submission                                      |

## Quick map

```text
kmcp init → kmcp build → kind load → kmcp deploy (namespace: kagent)
         ↓
MCP Inspector @0.21.1  ←── kubectl port-forward svc/... 3000:3000
         ↓
agents-cli create → copy agent.py → McpToolset (Streamable HTTP) → playground
         ↓
(optional) docker build + kubectl apply k8s/ → agent pod in abox
```

## Quick start (development)

```bash
# Prerequisites: abox running (see lab-02 or ABOX-restart.md)
kubectl config use-context kind-abox

# MCP server
cd lab03-mcp-server
kmcp build --project-dir . -t lab03-mcp-server:latest
kind load docker-image lab03-mcp-server:latest --name abox
kmcp deploy --file kmcp.yaml --image lab03-mcp-server:latest --namespace kagent --no-inspector

# agents-cli agent (see LAB03-beginners-development.md §C for full steps)
export GOOGLE_GENAI_USE_VERTEXAI=FALSE
export GOOGLE_API_KEY='your-key-here'
# rm -rf lab03-agent && agents-cli create lab03-agent --prototype --yes
# cp ../lab03-agent-snippet/app/agent.py lab03-agent/app/agent.py
# cd lab03-agent && agents-cli install && agents-cli playground
```

Full steps, troubleshooting (429 quota, stale ADK session, missing `lab03_greet`), and screenshots: [`LAB03-beginners-development.md`](LAB03-beginners-development.md).

## Relationship to Lab 2

|               | Lab 2                                                           | Lab 3                                                |
| ------------- | --------------------------------------------------------------- | ---------------------------------------------------- |
| Focus         | Platform: abox, Flux UI, kagent declarative `Agent` + fetch MCP | Custom **kmcp** server + **agents-cli** (Google ADK) |
| MCP deploy    | `kubectl apply` kagent `MCPServer` (e.g. `mcp-server-fetch`)    | `kmcp build` / `kmcp deploy`                         |
| Agent runtime | kagent UI + `Agent` CRD                                         | agents-cli playground (optional k8s deploy)          |
| LLM (typical) | OpenAI via kagent                                               | Gemini via agents-cli                                |

Both labs use the same **abox** cluster; Lab 3 adds your own MCP implementation and a second agent stack.

## Other tracks

- **Experienced:** Beginners development + implement your own **MCP Apps** use case end-to-end.
- **Max:** Experienced + **MCP Sampling** or **Elicitation** use case.

## References

- [kmcp quickstart](https://kagent.dev/docs/kmcp/quickstart)
- [Introducing kmcp (Solo)](https://www.solo.io/blog/introducing-kmcp)
- [agents-cli](https://google.github.io/agents-cli/)
- [ADK MCP tools](https://adk.dev/tools-custom/mcp-tools/)
- [MCP Sampling](https://modelcontextprotocol.io/docs/concepts/sampling)
- [MCP Apps announcement](https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/)
