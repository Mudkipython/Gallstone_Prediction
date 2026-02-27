FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:${PATH}"

WORKDIR /workspace

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir "uv==0.10.0"

COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --extra dev --no-install-project

COPY . .
RUN uv sync --frozen --extra dev

EXPOSE 8888

CMD ["bash", "-lc", "if [ ! -f /workspace/gallstone.csv ] && [ -f /workspace/data/raw/gallstone.csv ]; then ln -s /workspace/data/raw/gallstone.csv /workspace/gallstone.csv; fi && uv run jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --ServerApp.token= --ServerApp.password="]
