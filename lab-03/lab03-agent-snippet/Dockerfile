# Use from agents-cli project root after: agents-cli create + agents-cli install
FROM python:3.12-slim

WORKDIR /app
RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock* ./
COPY app ./app
RUN uv sync --frozen 2>/dev/null || uv sync

ENV ADK_WEB_HOST=0.0.0.0
ENV ADK_WEB_PORT=8080

CMD ["uv", "run", "adk", "web", "--host", "0.0.0.0", "--port", "8080"]
