FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends locales \
    && sed -i '/uk_UA.UTF-8/s/^# //g' /etc/locale.gen \
    && locale-gen uk_UA.UTF-8 \
    && rm -rf /var/lib/apt/lists/*
ENV LANG=uk_UA.UTF-8 LC_ALL=uk_UA.UTF-8

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project
COPY . .
RUN uv sync --frozen --no-dev
CMD ["uv", "run", "main.py"]