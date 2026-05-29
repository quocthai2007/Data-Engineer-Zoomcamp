FROM python:3.13.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/ 

WORKDIR /code
ENV PATH="/code/.venv/bin:$PATH"

COPY uv.lock .python-version pyproject.toml ./ 

RUN uv sync --locked

COPY pipeline.py .

ENTRYPOINT ["python", "pipeline.py"]